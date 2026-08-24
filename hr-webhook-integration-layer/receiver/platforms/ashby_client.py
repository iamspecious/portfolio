"""
Ashby API wrapper — used against Ashby's DOCUMENTED PAYLOAD SHAPES, not a
live Ashby account. Ashby has no public sandbox, so this client is exercised
against the fixtures in simulators/ashby_payloads.py, not a real API. The
request-building and response-checking logic below is real; the server on
the other end of it, in this project, is not. See README.md.

Auth: HTTP Basic, API key as the username, password left blank.

The one rule every method in this class obeys: check response_body["success"]
before trusting a 200. Ashby can — and per its own docs, routinely does —
return HTTP 200 with {"success": false, "errors": [...]} in the body for a
failed request. A wrapper that only checks status_code < 400 will read that
as a success and move on, silently. Every method here raises AshbyAPIError
on success: false exactly as it would on a 4xx, so nothing downstream has to
remember to check twice.
"""

import base64
import json
import urllib.error
import urllib.request

from receiver.config import Config


class AshbyAPIError(Exception):
    def __init__(self, status, errors):
        self.status = status
        self.errors = errors
        super().__init__(f"Ashby API error (http {status}): {errors}")


class AshbyAuthError(Exception):
    """Raised on 401/403. Callers must NOT retry — see the module docstring
    in hibob_client.py for why a retry loop on an auth error is the
    dangerous move across all three of these platforms, not just HiBob's."""


class AshbyClient:
    def __init__(self, config: Config):
        self.config = config

    def _request(self, path: str, body: dict) -> dict:
        if not self.config.ashby_api_key:
            raise RuntimeError("ASHBY_API_KEY is not set — see .env.example.")

        url = f"https://api.ashbyhq.com{path}"
        data = json.dumps(body or {}).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")

        basic = base64.b64encode(f"{self.config.ashby_api_key}:".encode("utf-8")).decode("ascii")
        req.add_header("Authorization", f"Basic {basic}")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise AshbyAuthError(
                    f"Ashby returned {e.code} — halting, not retrying. "
                    f"An auth error means the key is wrong or scoped wrong; "
                    f"retrying sends the same bad credential again."
                ) from None
            status = e.code
            raw = e.read().decode("utf-8")

        parsed = json.loads(raw) if raw else {}

        # THE check. Status can be 200 and this can still be a failure.
        if status >= 400 or parsed.get("success") is False:
            raise AshbyAPIError(status, parsed.get("errors", parsed))

        return parsed

    # ---- endpoints used by this project ----

    def get_application(self, application_id: str) -> dict:
        return self._request("/application.info", {"applicationId": application_id})

    def get_candidate(self, candidate_id: str) -> dict:
        return self._request("/candidate.info", {"id": candidate_id})

    def list_webhooks(self) -> dict:
        return self._request("/webhook.list", {})
