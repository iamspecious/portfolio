"""
HiBob API wrapper — used against HiBob's DOCUMENTED PAYLOAD SHAPES, not a
live HiBob account. Like Ashby, HiBob has no public developer sandbox, so
this client is exercised against simulators/hibob_payloads.py fixtures.
The request-building logic is real; there is no live HiBob tenant behind it
in this project. See README.md.

Auth: HTTP Basic, service-user ID and token, base64("id:token").

THE RULE THIS FILE EXISTS TO ENFORCE: on 401 or 403, halt. Never retry.

HiBob's WAF blocks the source IP for five minutes after roughly 50 auth
failures (401/403) arrive from it within a ten-second window. That number
comes from the project brief / operational report, not from HiBob's public
docs — I could not independently verify the exact threshold against
published documentation (see RESEARCH.md), but the shape of the failure
mode is exactly what you'd expect from any WAF fronting an auth-sensitive
API, and the design response is correct regardless of the precise number:
a naive retry-with-backoff loop hitting an expired service-user token would
blow through 50 attempts in well under ten seconds, and the resulting block
doesn't just fail this integration — it blocks every other automation
sharing that source IP for five minutes. A single wrapper that refuses to
retry an auth error is cheap insurance against a failure mode that's
expensive to have caused.
"""

import base64
import json
import urllib.error
import urllib.request

from receiver.config import Config


class HiBobAPIError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"HiBob API error {status}: {body}")


class HiBobAuthError(Exception):
    """
    Raised on 401/403 and NEVER retried by this client. If you're tempted
    to wrap a call to this client in a retry loop upstream, don't — that's
    exactly the pattern that trips the WAF. Fix the credential and restart.
    """


class HiBobClient:
    BASE_URL = "https://api.hibob.com/v1"

    def __init__(self, config: Config):
        self.config = config

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        if not (self.config.hibob_service_user_id and self.config.hibob_service_user_token):
            raise RuntimeError(
                "HIBOB_SERVICE_USER_ID / HIBOB_SERVICE_USER_TOKEN not set — see .env.example."
            )

        url = f"{self.BASE_URL}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")

        creds = f"{self.config.hibob_service_user_id}:{self.config.hibob_service_user_token}"
        basic = base64.b64encode(creds.encode("utf-8")).decode("ascii")
        req.add_header("Authorization", f"Basic {basic}")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                self._log_rate_limit(resp.headers)
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            self._log_rate_limit(e.headers)
            if e.code in (401, 403):
                # NO RETRY. See module docstring.
                raise HiBobAuthError(
                    f"HiBob returned {e.code}. Halting immediately — this "
                    f"client never retries an auth failure. Repeated 401/403 "
                    f"from one IP is what trips HiBob's WAF block."
                ) from None
            raise HiBobAPIError(e.code, e.read().decode("utf-8")) from None

    @staticmethod
    def _log_rate_limit(headers):
        limit = headers.get("X-RateLimit-Limit")
        remaining = headers.get("X-RateLimit-Remaining")
        if remaining is not None:
            print(f"[hibob] rate limit — limit={limit} remaining={remaining}")

    # ---- endpoints used by this project ----

    def get_employee(self, employee_id: str) -> dict:
        return self._request("GET", f"/people/{employee_id}")

    def list_webhooks(self) -> dict:
        return self._request("GET", "/webhooks")
