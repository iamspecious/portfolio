"""
Remote API wrapper — the one platform this project calls for real.

Auth: OAuth2 client-credentials, bearer token. Token is fetched once and
cached in memory for the process lifetime; Remote's tokens are short-lived
enough in the sandbox that a long-running worker should refresh on a 401,
which this class does (once — see _request's retry note below, and
compare against the auth-error rule in hibob_client.py, which never
retries an auth failure. The difference is deliberate: Remote's 401 on an
expired bearer token is routine and self-healing via re-auth; HiBob's 401
is a WAF trip that gets WORSE if you retry it. Same status code, opposite
correct response — see RESEARCH.md, "same status code, three different
verbs.")

Rate limiting: Remote returns x-ratelimit-count / x-ratelimit-remaining /
x-ratelimit-reset on every authenticated response. The limit is 300
requests/minute PER COMPANY — shared across every token issued for that
company, not per-token. A second integration hammering the same company
eats into this integration's headroom with no visibility from here. This
client logs the remaining count on every call specifically so that's
observable rather than a mystery 429 three weeks later.
"""

import json
import time
import urllib.error
import urllib.request

from receiver.config import Config


class RemoteAPIError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"Remote API error {status}: {body}")


class RemoteClient:
    def __init__(self, config: Config):
        self.config = config
        self._token = None
        self._token_expires_at = 0

    # ---- auth ----

    def _get_token(self) -> str:
        if self._token and time.time() < self._token_expires_at - 30:
            return self._token

        self.config.require_remote_credentials()
        url = f"{self.config.remote_base_url}/auth/oauth2/token"
        body = "grant_type=client_credentials".encode("utf-8")
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        import base64
        basic = base64.b64encode(
            f"{self.config.remote_client_id}:{self.config.remote_client_secret}".encode("utf-8")
        ).decode("ascii")
        req.add_header("Authorization", f"Basic {basic}")

        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        self._token = payload["access_token"]
        self._token_expires_at = time.time() + payload.get("expires_in", 3600)
        return self._token

    # ---- request plumbing ----

    def _request(self, method, path, body=None, _retried_auth=False):
        url = f"{self.config.remote_base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self._get_token()}")
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                self._log_rate_limit(resp.headers)
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            self._log_rate_limit(e.headers)
            error_body = e.read().decode("utf-8")

            # A 401 here means an expired/invalid bearer token, not a
            # permissions problem — re-auth once and retry. This is the
            # one place in this codebase that retries after an auth
            # failure, and it's safe specifically because Remote's OAuth2
            # tokens expiring is expected, routine behaviour, unlike
            # HiBob's WAF-triggering 401s (see hibob_client.py).
            if e.code == 401 and not _retried_auth:
                self._token = None
                return self._request(method, path, body, _retried_auth=True)

            raise RemoteAPIError(e.code, error_body) from None

    @staticmethod
    def _log_rate_limit(headers):
        count = headers.get("x-ratelimit-count")
        remaining = headers.get("x-ratelimit-remaining")
        reset_ms = headers.get("x-ratelimit-reset")
        if remaining is not None:
            print(
                f"[remote] rate limit — count={count} remaining={remaining} "
                f"reset_ms={reset_ms} (300/min, shared across every token "
                f"for this company)"
            )

    # ---- endpoints used by this project ----

    def get_country_schema(self, country_code: str) -> dict:
        """
        GET the JSON schema Remote publishes for a country's employment
        payload. Used by flows/hire_flow.py to validate a simulated hire
        before attempting to create an employment, rather than finding out
        a required field is missing from a 422 after the fact.
        """
        return self._request("GET", f"/v1/countries/{country_code}/employment-schema")

    def create_employment(self, employment_payload: dict) -> dict:
        return self._request("POST", "/v1/employments", body=employment_payload)

    def list_webhook_events(self, **filters) -> dict:
        """
        Remote's own record of what it tried to deliver — the only way to
        discover a webhook that was silently dropped, because Remote
        treats 4xx/5xx as "delivered" (see RESEARCH.md / failure_demo.py).
        """
        query = "&".join(f"{k}={v}" for k, v in filters.items())
        path = "/v1/webhook-events" + (f"?{query}" if query else "")
        return self._request("GET", path)

    def replay_webhook_events(self, event_ids: list) -> dict:
        """The only recovery path for a Remote event lost to a 4xx/5xx."""
        return self._request("POST", "/v1/webhook-events/replay", body={"event_ids": event_ids})
