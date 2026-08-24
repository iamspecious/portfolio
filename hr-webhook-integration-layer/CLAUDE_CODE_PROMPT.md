# CLAUDE_CODE_PROMPT.md

This file is a new convention — no other project in this portfolio has one. It exists because the kickoff prompt below is, itself, an artifact worth being honest about: this project was scaffolded by handing Claude Code the brief reproduced verbatim here, with an explicit Phase 0 discovery-and-confirm step before anything got written. What follows is that prompt, unedited.

---

## Phase 0 — Discovery (do this first, write nothing)

Read the repository and report back on the portfolio's taxonomy and data tagging, the "Digital Spec" front-door overlay, per-project file conventions, prose style, layout/styling, and the closest structurally-similar existing project. Output: a written summary of the conventions found, plus a proposed file manifest with exact paths and metadata values drawn from the existing vocabulary — flagging, not inventing, anywhere the vocabulary had no suitable term. Then stop and wait for confirmation.

*(Phase 0 ran as its own conversation turn — full discovery findings and the resulting flags are in the session transcript, not reproduced here. The short version: no `RESEARCH.md` or `CLAUDE_CODE_PROMPT.md` convention existed anywhere in the portfolio before this project; PostHog CS Health Intelligence was identified as the closest structural analogue; new `tools` vocabulary terms were flagged as needed. The follow-up instruction that resolved those flags — "Anything that's not there please add and make the changes where they make sense to" — is what authorized this file, the new tool tags, and the language choice below.)*

## Phase 1 — Build spec

**What this is:** A webhook receiver and integration layer demonstrating correct handling of three HR platforms whose failure semantics are mutually incompatible. The point is that the three platforms disagree about what a failed delivery means, and a naive integration is silently wrong for at least two of them.

**Honesty constraint (non-negotiable):** Only Remote provides a public sandbox. Real API calls against the Remote sandbox; documented-payload simulators for HiBob and Ashby, built from their public developer docs. Stated plainly in the README and the write-up. Never present simulated integrations as live, and never soften the distinction.

**Components specified:**

1. **Webhook receiver** — three signature verification schemes, each correct and separate: Remote (HMAC-SHA256, base16, over `raw_body + ":" + timestamp`, header `X-Remote-Signature` / `X-Remote-Timestamp`, constant-time comparison); Ashby (HMAC-SHA256, hex, `sha256=<hex>` in `Ashby-Signature`, over raw bytes, constant-time comparison after stripping the prefix); HiBob (HMAC-SHA512, base64, `Bob-Signature`). Verify before parsing; return 200 immediately on valid signature; hand off to a queue; handle each platform's ping/validation event.

2. **Deduplication and queue** — durable (SQLite is fine), dedupe by event ID, and survive Ashby's fan-out case: `candidateHire` also fires `applicationUpdate` and `candidateStageChange`, so one hire arriving as three events must produce one downstream run.

3. **Person-mapping table** — one row per human: canonical ID, HiBob employee ID, Ashby candidate ID, Ashby application ID, Remote employment ID, work email, personal email, employment type, country, start date, status, `merged_into`. Identity resolution goes through this table only — never by email inside a workflow.

4. **Platform request wrappers** — one per platform, centralizing auth (Remote OAuth2 bearer; Ashby Basic with API key as username, blank password; HiBob Basic with service-user credentials), rate-limit awareness from response headers, the Ashby `success: false` check (Ashby can return HTTP 200 with a failure body — status code alone is not sufficient), and the rule that auth errors halt and never retry (HiBob's WAF blocks the source IP for five minutes after 50+ 401s/403s in ten seconds; a retry loop on a permission error locks out every automation on that IP).

5. **One end-to-end flow** — simulated hire → fetch the live country JSON schema from Remote → validate the payload against it → create employment in the Remote sandbox. Dry-run flag on by default, logging intended calls without making them. Idempotency key derived from `(event ID + target system + operation)`.

6. **The failure-philosophy demonstration** — a script that returns HTTP 500 to each platform's delivery and shows what each does: Remote treats 4xx/5xx as delivered (event silently lost, recoverable only via the replay endpoint); Ashby disables the webhook entirely on a response ≥ 400; HiBob retries with backoff for up to 3 days, emailing admins at 1h/24h/48h, deactivating at 72h. Runnable, legible output — the centerpiece.

**Stack:** n8n (self-hosted, Docker) for the workflow layer, workflow JSON committed to the repo. Node or Python for the receiver and wrappers, matching whatever the rest of the portfolio uses. ngrok for local tunnelling during development, with a note that free ngrok must not be used against production.

**Environment:** `.env.example` documenting every required variable, no real credentials anywhere. Remote sandbox base URL `gateway.remote-sandbox.com`; production `gateway.remote.com`. The environment switch explicit and hard to get wrong.

## Phase 2 — Portfolio integration

Produce the full standard file set identified in Phase 0: `RESEARCH.md` (what the three platforms' docs actually say — auth models, rate-limit scoping including that Remote's 300/min is per company not per token, permission models, webhook contracts, and the constraint that Remote's write window effectively closes at invite), `DEVLOG.md` (a build log in the existing voice — what actually broke and surprised, not a tidy narrative: the WAF lockout on retried auth errors, the write window closing at invite, Ashby's 200-with-failure-body, the three-way retry disagreement), `README.md` (what it is, how to run it, the honesty note), a portfolio index entry using the confirmed schema and controlled vocabulary, and a project page matching the existing layout conventions, routed through the Digital Spec overlay.

## Working rules

Stop and ask before introducing any dependency not already used in the portfolio. Stop and ask before creating a new taxonomy term, tag, or metadata field. Commit in logical units with clear messages. No credentials, tokens, or real employee data anywhere, including example payloads — synthetic data only. Where this prompt conflicts with an existing portfolio convention, the existing convention wins, flagged and asked about rather than silently overridden.

---

*Five new `tools` vocabulary terms this project needed that weren't in `TAXONOMY.md` before it (n8n, docker, sqlite, ngrok, webhook-signature-verification) were added there directly, per the follow-up authorization above, and logged in `TAGGING-AUDIT.md` per that document's own instruction.*
