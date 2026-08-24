# RESEARCH — HR Webhook Integration Layer

There's no existing RESEARCH.md convention elsewhere in this portfolio — the closest precedent is the research phase folded into the first few DEVLOG.md entries on PostHog CS Health Intelligence. This project keeps it as its own file because there's a specific claim resting on it: the honesty split between what's live and what's simulated only holds up if the simulated parts are built from what the platforms' docs actually say, not from guesswork. This is that grounding, with sources.

A separate note on scope: some of this project's design constraints (the exact HiBob WAF lockout numbers) come from the project brief, not from anything published. That distinction is called out explicitly everywhere it applies, below and in the code.

---

## Remote

**Auth.** OAuth2 client-credentials flow. `POST /auth/oauth2/token` with `Authorization: Basic base64(client_id:client_secret)` and `Content-Type: application/x-www-form-urlencoded`, body `grant_type=client_credentials`. Returns a bearer token with an `expires_in`. Sandbox and production are separate hostnames, not a header flag: `gateway.remote-sandbox.com` vs `gateway.remote.com`. That's a deliberate design choice on Remote's part — you cannot accidentally hit production by mistyping a parameter, only by hardcoding the wrong host. `config.py` in this project makes the same mistake structurally impossible to make quietly: `REMOTE_ENV` defaults to `sandbox`, so an unset variable fails toward the safe side.

**Rate limits.** Three headers on every authenticated response: `x-ratelimit-count`, `x-ratelimit-remaining`, `x-ratelimit-reset` (milliseconds until the window resets). The limit is 300 requests/minute — **per company, not per token.** That scoping matters more than the number: if this integration and some other automation both hold tokens for the same Remote company, they're drawing from the same 300, and neither one can see the other's usage without reading these headers. `remote_client.py` logs the remaining count on every call specifically so a shrinking budget is visible before it becomes a 429, not after.

**Webhook signatures.** `X-Remote-Signature` (HMAC-SHA256, base16/hex) and `X-Remote-Timestamp`. The signed string is `raw_body + ":" + timestamp`. The timestamp is the time of Remote's *first* delivery attempt — a retried webhook for an event keeps its original timestamp, so a receiver can tell "this is an old retry" from "this is a genuinely new event for the same entity" by comparing timestamps, not by inventing its own tracking. ([developer.remote.com/docs/verifying-webhooks](https://developer.remote.com/docs/verifying-webhooks))

**Delivery failure semantics — the one that surprised me most.** A 4xx or 5xx response to a webhook delivery is recorded as *delivered*. Not retried, not flagged, not distinguished from a 200 in any way that surfaces automatically. Remote does retry — but only in the sense that if *you* ask again, via `list_webhook_events` and then `replay_webhook_events`, it will resend. There is no push notification that something failed; the pull is entirely on the integration. This is the platform where a broken receiver loses data with the least ceremony of the three. ([developer.remote.com/docs/working-with-webhooks](https://developer.remote.com/docs/working-with-webhooks))

**The write window closes at invite.** An employment record is editable through the API only up to the point the invitation is sent to the employee. After that, the update endpoint stops accepting changes to core fields — because post-invite changes are treated as contract amendments the employee themselves has to agree to, not backend data cleanup. Practically: this project's hire flow validates against the live country schema and creates the employment *before* any invite step exists in the flow, and doesn't attempt to patch a record after the fact. A production version of this integration would need its own "have we already invited this person" check before ever calling update, because Remote's error on a post-invite update attempt won't explain the *reason*, just that it's rejected. ([developer.remote.com/docs/update-and-invite-employment](https://developer.remote.com/docs/update-and-invite-employment), [developer.remote.com/docs/creating-employees-with-remote-api](https://developer.remote.com/docs/creating-employees-with-remote-api))

**Sandbox.** `gateway.remote-sandbox.com` is real, public, and what this project's live calls (schema fetch, employment creation) actually run against — see README's honesty note.

---

## Ashby

**Auth.** HTTP Basic. API key as the username, password left blank — `Authorization: Basic base64(api_key:)`. Keys are scoped per-module (`organizationRead`, `candidatesWrite`, etc.) at creation time in the Ashby admin. No OAuth flow, no token refresh to manage — which also means there's no self-healing "token expired, get a new one" path; a bad key is bad until a human rotates it in the admin UI. ([developers.ashbyhq.com/docs/authentication](https://developers.ashbyhq.com/docs/authentication))

**Rate limits.** 1,000 requests/minute per API key, sliding window, applied per endpoint family. List endpoints (`candidate.list`, `application.list`) carry tighter limits than single-item reads. Exceeding it returns 429 with `Retry-After`.

**Webhook signatures.** `Ashby-Signature: sha256=<hex>`. The digest is HMAC-SHA256 over the **exact raw request bytes** — not the JSON after it's been parsed and would-be re-serialized, which can differ in whitespace and key order from what Ashby actually signed. This is the reason `ashby_client.py`'s equivalent on the receiving side, `signatures.verify_ashby`, takes `raw_body: bytes` and nothing downstream is allowed to touch it before verification runs. ([developers.ashbyhq.com/docs/authenticating-webhooks](https://developers.ashbyhq.com/docs/authenticating-webhooks))

**The `success: false` trap.** Ashby's API can return HTTP 200 with `{"success": false, "errors": [...]}` in the body. A wrapper written to the usual "status < 400 means it worked" assumption reads that as success and moves on. `ashby_client.py`'s `_request` checks `parsed.get("success") is False` on every single call, unconditionally — there's no endpoint in this wrapper that gets to skip the check, because there was no way to know in advance which one would be the exception.

**Webhook disable-on-failure.** If the receiving endpoint is unreachable or returns ≥ 400 — including on the *very first* ping delivery sent when the webhook is created — Ashby disables the subscription. Not the one event: the whole webhook, until a human finds it in Admin → Integrations → Webhooks and manually re-enables it. Retries do happen for events that make it past that point — exponential backoff starting at 10s, up to 10 attempts — but 401/403/404/405/410 are excluded from retry entirely, on the reasoning that those are "this will never succeed by trying again" codes. ([developers.ashbyhq.com/docs/setting-up-webhooks](https://developers.ashbyhq.com/docs/setting-up-webhooks), [developers.ashbyhq.com/docs/retries](https://developers.ashbyhq.com/docs/retries))

**Event fan-out.** A single hire produces at least three webhook deliveries: `candidateStageChange` (the move into the Hired stage), `applicationUpdate`, and `candidateHire` — each with a distinct `webhookId` but the same `data.application.id`. This is the case `receiver/queue.py`'s `fan_out_key` exists for.

**No public sandbox.** Confirmed by the absence of one anywhere in Ashby's docs or developer portal, and by every third-party integration guide describing testing against a real (non-demo) Ashby org. This is the reason `ashby_client.py` is exercised against `simulators/ashby_payloads.py`, not a live account.

---

## HiBob

**Auth.** HTTP Basic with a *service user*, not a personal API token. `Authorization: Basic base64(service_user_id:service_user_token)`. HiBob deprecated the older API-access-token method entirely (cutover October 2024) — the service-user model is now the only supported path, which matters for anyone reading older integration guides that still describe the retired method. ([apidocs.hibob.com/reference/authorization](https://apidocs.hibob.com/reference/authorization), [apidocs.hibob.com/docs/transition-from-api-access-tokens](https://apidocs.hibob.com/docs/transition-from-api-access-tokens))

**Rate limits.** `X-RateLimit-*` headers on responses; HiBob's own docs don't publish an exact per-minute number as plainly as Remote's do — third-party integration guides estimate 10–100 requests/minute depending on the endpoint and plan. `hibob_client.py` logs `X-RateLimit-Limit` / `X-RateLimit-Remaining` on every call so the actual figure is observable in practice rather than assumed.

**Webhook signatures.** `Bob-Signature`, HMAC-SHA512, base64-encoded, computed over the raw request body — no algorithm prefix to strip, unlike Ashby's `sha256=` header. ([apidocs.hibob.com/reference/getting-started-webhooks](https://apidocs.hibob.com/reference/getting-started-webhooks))

**Delivery retry semantics.** Webhooks v2 retries with exponential backoff for up to 3 days. Admins (and anyone else configured to receive delivery-issue notifications) get emailed when delivery starts failing. If there's no successful delivery across 3 consecutive days, the webhook deactivates. This is the most forgiving — and the most observable — of the three failure models: a human finds out by email, not by absence. ([apidocs.hibob.com/docs/migrate-to-webhooks-v2](https://apidocs.hibob.com/docs/migrate-to-webhooks-v2))

**The WAF lockout — asserted, not verified.** The project brief this was built from states: HiBob's WAF blocks the source IP for five minutes after 50+ 401/403 responses arrive from it within a ten-second window. I could not find that specific threshold published in HiBob's public developer docs — general rate-limiting and WAF behavior is documented, but not this exact number. I'm stating that plainly rather than presenting it as verified, because the whole point of this project is not doing that. What I *can* verify independently: any API sitting behind a WAF with auth-failure-based blocking will behave in roughly this shape, and the correct defensive response — never retry a 401/403, halt and surface it to a human — is correct regardless of whether the real threshold is 50-in-10-seconds or something else. `hibob_client.py` is written to that principle, not to the specific number.

**No public sandbox.** Same situation as Ashby — no hosted demo environment for outside developers. `hibob_client.py` is exercised against `simulators/hibob_payloads.py`.

---

## Cross-platform: same status code, three different verbs

The single finding that shaped this whole project. Send a webhook delivery to a receiver returning a plain HTTP 500, and:

| Platform | What happens to *that event* | What happens to *future events* |
|---|---|---|
| Remote | Marked delivered. Recoverable only via `replay_webhook_events`, if you know to call it. | Nothing changes — delivery continues normally. |
| Ashby | Retried (backoff, up to 10 attempts) — unless the failure code is 401/403/404/405/410, in which case not retried at all. | If the webhook was in a failed state (unreachable, or ≥400 on the first ping), it's **disabled** until a human re-enables it. |
| HiBob | Retried with backoff for up to 3 days; admins emailed. | Deactivated only after 3 consecutive days with zero successful deliveries. |

A receiver built and tested against any one of these — "of course it retries," "of course a failure just gets flagged," whichever assumption came from wherever the engineer's last webhook integration happened to be — is silently wrong for at least two of the other platforms. `receiver/failure_demo.py` demonstrates this directly.

---

## What's genuinely live vs. documented-simulation in this project

Stated once here in full, and repeated in short form everywhere it's relevant (README, code comments, DEVLOG):

- **Remote** — real API calls against `gateway.remote-sandbox.com`: OAuth2 token fetch, country schema fetch, employment creation (dry-run gated). This is the one platform with a public sandbox, so it's the one this project actually calls.
- **Ashby and HiBob** — no public sandbox exists for either. Every request-building and response-checking code path (`ashby_client.py`, `hibob_client.py`) is real and exercised against payloads shaped from each platform's own published documentation (`simulators/ashby_payloads.py`, `simulators/hibob_payloads.py`), not against a live account. Nowhere in this project does simulated output get presented as if it came from a real API call.
