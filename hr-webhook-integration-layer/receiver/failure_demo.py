"""
The centerpiece: what actually happens when delivery fails.

A naive integration treats "the webhook fired" and "the downstream system
knows about it" as the same fact. They aren't, and the gap between them is
different for all three platforms:

  Remote  — a 4xx/5xx response is recorded as DELIVERED. The event is gone
            from the receiver's perspective. The only way back is the
            replay endpoint, and only if you know to look.
  Ashby   — a single response >= 400 (including the initial ping) disables
            the webhook subscription outright. Every future event stops
            arriving until a human re-enables it in the admin UI.
  HiBob   — retries with exponential backoff for up to 3 days, emailing
            admins at intervals, and deactivates only after three
            consecutive days with no successful delivery.

Same failure (a 500 from the receiver). Three different outcomes: silent
loss, an immediate full outage, and a three-day grace period. A receiver
built to one of these models and pointed at the other two is wrong for at
least two of them.

What this script actually does, honestly:
  1. Starts a real local HTTP server that always returns 500 — the
     "broken receiver" — and sends it a real request per platform, so the
     500 you see below is a genuine response to a genuine request, not a
     printed string.
  2. If REMOTE_CLIENT_ID/REMOTE_CLIENT_SECRET are set, it also makes a
     real call against the Remote sandbox (fetching an OAuth2 token and
     listing webhook-events) to demonstrate the parts of Remote's failure
     model that ARE observable without a fully provisioned sandbox company
     and a live registered subscription. This is marked OBSERVED.
  3. Everything about what Ashby and HiBob do next, and what Remote does
     to an event once its delivery attempt fails, is DOCUMENTED — sourced
     from each platform's public developer docs (see RESEARCH.md) — not
     something this script can trigger live, because doing so would mean
     driving a real company's real webhook subscription into a failure
     state, which is out of scope for a portfolio demo regardless of
     which platform it targeted. The distinction is printed inline, not
     hidden in a comment.

Run:
  python -m receiver.failure_demo
"""

import json
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

from receiver.config import load_config
from receiver.platforms.remote_client import RemoteClient, RemoteAPIError


class _AlwaysFiveHundred(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(length)
        body = b'{"error": "simulated downstream failure"}'
        self.send_response(500)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _start_flaky_receiver():
    server = HTTPServer(("127.0.0.1", 0), _AlwaysFiveHundred)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{port}"


def _deliver_and_observe(url: str, label: str, sample_payload: dict) -> None:
    body = json.dumps(sample_payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=5)
        print(f"    OBSERVED — unexpected 2xx from the flaky receiver (shouldn't happen).")
    except urllib.error.HTTPError as e:
        print(f"    OBSERVED — {label} delivery attempt hit the flaky local receiver "
              f"and got back HTTP {e.code}. This part is real: an actual request "
              f"was sent and an actual 500 came back.")


def _section(title: str):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def run():
    config = load_config()
    server, flaky_url = _start_flaky_receiver()
    print(f"Local flaky receiver up at {flaky_url} — every request gets a real HTTP 500.")

    try:
        # ---------------------------------------------------------------
        _section("REMOTE")
        _deliver_and_observe(flaky_url, "Remote", {"id": "evt_demo", "type": "employment.created"})

        if config.remote_client_id and config.remote_client_secret:
            print("    Credentials present — attempting a live sandbox call ...")
            try:
                client = RemoteClient(config)
                events = client.list_webhook_events()
                print(f"    OBSERVED (live sandbox) — list_webhook_events returned "
                      f"{len(events.get('data', []))} record(s). This confirms the API "
                      f"is reachable and authenticated; it does not by itself prove a "
                      f"failed delivery, because that requires a subscribed webhook and "
                      f"a real triggering event in this sandbox company, which this demo "
                      f"does not provision.")
            except RemoteAPIError as e:
                print(f"    Live sandbox call failed: {e}")
        else:
            print("    REMOTE_CLIENT_ID / REMOTE_CLIENT_SECRET not set — skipping the live "
                  "sandbox call. Set them in .env to see this section make a real request.")

        print()
        print("    DOCUMENTED (developer.remote.com/docs/verifying-webhooks, "
              "developer.remote.com/docs/working-with-webhooks):")
        print("    A response of 4xx or 5xx is recorded as a delivered attempt, same as a")
        print("    2xx. There is no automatic retry and no automatic alert. The event is")
        print("    findable afterward only via list_webhook_events, and recoverable only")
        print("    via the replay endpoint — both of which require knowing to look.")
        print("    Silent loss is the failure mode: nothing breaks loudly, nothing pages")
        print("    anyone, the event is just gone unless someone goes looking for it.")

        # ---------------------------------------------------------------
        _section("ASHBY")
        _deliver_and_observe(flaky_url, "Ashby", {"action": "candidateHire", "data": {}})

        print()
        print("    DOCUMENTED (developers.ashbyhq.com/docs/authenticating-webhooks, "
              "developers.ashbyhq.com/docs/retries):")
        print("    Ashby retries with exponential backoff (starting at 10s, up to 10")
        print("    attempts) — EXCEPT for a specific set of status codes, 401/403/404/")
        print("    405/410, which are not retried at all. And if the endpoint is")
        print("    unreachable or returns >= 400 on the very first delivery (including")
        print("    the initial ping sent when the webhook is created), Ashby disables the")
        print("    webhook subscription outright. Not this one event — every future event")
        print("    on this webhook, until a human re-enables it by hand in Admin >")
        print("    Integrations > Webhooks. A transient 500 during a deploy can end an")
        print("    integration's entire event stream with no further attempts and no")
        print("    further warning.")

        # ---------------------------------------------------------------
        _section("HIBOB")
        _deliver_and_observe(flaky_url, "HiBob", {"type": "employee.hired", "payload": {}})

        print()
        print("    DOCUMENTED (apidocs.hibob.com/reference/getting-started-webhooks, "
              "apidocs.hibob.com/docs/migrate-to-webhooks-v2):")
        print("    HiBob retries with exponential backoff for up to 3 days. Bob Admins")
        print("    (and anyone else configured to receive delivery-issue notifications)")
        print("    get an email when delivery starts failing, so a human finds out fast —")
        print("    unlike Remote. If there is no successful delivery across 3 consecutive")
        print("    days, the webhook is deactivated. The brief that shaped this project")
        print("    also names a related, separate failure mode worth stating plainly: on")
        print("    the AUTH side (not delivery — a receiver holding a bad/expired")
        print("    credential and calling HiBob's API), HiBob's WAF blocks the source IP")
        print("    for five minutes after roughly 50 401/403 responses arrive from it")
        print("    within a ten-second window. That specific number is asserted, not")
        print("    verified against HiBob's public docs (see RESEARCH.md) — but a retry")
        print("    loop on an auth error will find it either way, and the block hits")
        print("    every automation sharing that source IP, not just the one that caused")
        print("    it. This is why hibob_client.py never retries a 401/403 (see")
        print("    receiver/platforms/hibob_client.py).")

        # ---------------------------------------------------------------
        _section("SUMMARY")
        print("    Same failure. Three different outcomes:")
        print()
        print(f"    {'Platform':<10}{'On 4xx/5xx':<45}{'Recovery'}")
        print(f"    {'-'*10}{'-'*45}{'-'*20}")
        print(f"    {'Remote':<10}{'Delivered anyway; event silently lost':<45}{'Replay endpoint, if you look'}")
        print(f"    {'Ashby':<10}{'Webhook disabled after one failure':<45}{'Manual re-enable in admin UI'}")
        print(f"    {'HiBob':<10}{'Retried up to 3 days; admins emailed':<45}{'Automatic, until deactivation'}")
        print()
        print("    A receiver written against any one of these models and pointed at the")
        print("    other two is silently wrong for both of them.")

    finally:
        server.shutdown()


if __name__ == "__main__":
    run()
