"""
The webhook receiver.

Three routes, three signature schemes, one shared rule: verify before you
parse, and return 200 the instant the signature checks out — everything
after that (parsing, dedup, queueing) happens after the platform has
already been told "got it." A slow database write or a bug in the fan-out
logic should never turn into a webhook timeout, because a webhook timeout
looks identical to a dropped event to every one of these three platforms
in a slightly different, unhelpful way (see RESEARCH.md).

Routes:
  POST /webhooks/remote
  POST /webhooks/ashby
  POST /webhooks/hibob

Run:
  python -m receiver.app
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from receiver import db, queue, signatures
from receiver.config import load_config
from receiver.simulators import ashby_payloads, hibob_payloads


class WebhookHandler(BaseHTTPRequestHandler):
    config = None  # set by serve() before the server starts

    # Silence the default per-request stderr line in favour of our own.
    def log_message(self, fmt, *args):
        pass

    def do_POST(self):
        if self.path == "/webhooks/remote":
            self._handle_remote()
        elif self.path == "/webhooks/ashby":
            self._handle_ashby()
        elif self.path == "/webhooks/hibob":
            self._handle_hibob()
        else:
            self._respond(404, {"error": "unknown route"})

    # ---- Remote ----

    def _handle_remote(self):
        raw_body = self._read_body()
        signature = self.headers.get("X-Remote-Signature")
        timestamp = self.headers.get("X-Remote-Timestamp")

        try:
            valid = signatures.verify_remote(
                raw_body, timestamp, signature, self.config.remote_webhook_secret
            )
        except signatures.SignatureError as e:
            print(f"[remote] rejected — {e}")
            self._respond(400, {"error": str(e)})
            return

        if not valid:
            print("[remote] rejected — signature mismatch")
            self._respond(401, {"error": "invalid signature"})
            return

        # Signature verified. Respond 200 now, before doing anything else —
        # Remote treats a 4xx/5xx as "delivered" either way (see
        # RESEARCH.md), so there is no reliability upside to holding the
        # response open while we parse and queue. There is only downside:
        # a slow queue write turning into a timeout, which reads to Remote
        # exactly like a rejection.
        self._respond(200, {"received": True})

        event = json.loads(raw_body)
        if event.get("type") == "ping":
            print("[remote] ping/validation event received — no-op")
            return

        event_id = event.get("id")
        event_type = event.get("type", "unknown")
        result = queue.enqueue(
            self.config.db_path, event_id, "remote", event_type, raw_body.decode("utf-8")
        )
        print(f"[remote] {event_type} ({event_id}) -> {result}")

    # ---- Ashby ----

    def _handle_ashby(self):
        raw_body = self._read_body()
        sig_header = self.headers.get("Ashby-Signature")

        try:
            valid = signatures.verify_ashby(raw_body, sig_header, self.config.ashby_webhook_secret)
        except signatures.SignatureError as e:
            print(f"[ashby] rejected — {e}")
            self._respond(400, {"error": str(e)})
            return

        if not valid:
            print("[ashby] rejected — signature mismatch")
            self._respond(401, {"error": "invalid signature"})
            return

        # Respond 200 immediately. This one matters even more than Remote's:
        # Ashby DISABLES the webhook subscription entirely on a >=400
        # response (including from the very first ping). There's no retry
        # tier to fall back on — a slow or buggy handler here doesn't just
        # lose one event, it silently turns off every future one until a
        # human notices and re-enables it in the Ashby admin UI.
        self._respond(200, {"received": True})

        event = json.loads(raw_body)
        if event.get("action") == "ping":
            print("[ashby] ping/validation event received — no-op")
            return

        event_id = ashby_payloads.extract_event_id(event)
        fan_out_key = ashby_payloads.extract_fan_out_key(event)
        event_type = event.get("action", "unknown")
        result = queue.enqueue(
            self.config.db_path, event_id, "ashby", event_type,
            raw_body.decode("utf-8"), fan_out_key=fan_out_key,
        )
        print(f"[ashby] {event_type} ({event_id}, fan_out={fan_out_key}) -> {result}")

    # ---- HiBob ----

    def _handle_hibob(self):
        raw_body = self._read_body()
        sig_header = self.headers.get("Bob-Signature")

        try:
            valid = signatures.verify_hibob(raw_body, sig_header, self.config.hibob_webhook_secret)
        except signatures.SignatureError as e:
            print(f"[hibob] rejected — {e}")
            self._respond(400, {"error": str(e)})
            return

        if not valid:
            print("[hibob] rejected — signature mismatch")
            self._respond(401, {"error": "invalid signature"})
            return

        # Respond 200 immediately, same reasoning as the other two — and
        # HiBob is the platform most tolerant of a slow receiver (3 days of
        # retries before deactivation, see RESEARCH.md), but there's no
        # reason to rely on that tolerance when it costs nothing to not.
        self._respond(200, {"received": True})

        event = json.loads(raw_body)
        if event.get("type") == "webhook.ping":
            print("[hibob] ping/validation event received — no-op")
            return

        event_id = hibob_payloads.extract_event_id(event)
        event_type = event.get("type", "unknown")
        result = queue.enqueue(
            self.config.db_path, event_id, "hibob", event_type, raw_body.decode("utf-8")
        )
        print(f"[hibob] {event_type} ({event_id}) -> {result}")

    # ---- plumbing ----

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def _respond(self, status: int, body: dict):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def serve():
    config = load_config()
    db.init_db(config.db_path)
    WebhookHandler.config = config

    server = ThreadingHTTPServer((config.receiver_host, config.receiver_port), WebhookHandler)
    print(
        f"Receiver listening on {config.receiver_host}:{config.receiver_port} "
        f"(REMOTE_ENV={config.remote_env}, DRY_RUN={config.dry_run})"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
