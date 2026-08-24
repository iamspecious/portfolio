# HR Webhook Integration Layer

A webhook receiver and integration layer across three HR platforms — HiBob, Ashby, and Remote — built to demonstrate one specific thing: these three platforms disagree about what a failed webhook delivery means, and an integration built against any one of their failure models is silently wrong for the other two.

---

## The honesty note (read this first)

**Only Remote provides a public sandbox.** This project makes real API calls against it — `gateway.remote-sandbox.com` — for OAuth2 auth, fetching a country's live employment JSON schema, and creating an employment record (gated behind a dry-run flag that's on by default).

**HiBob and Ashby have no public sandbox.** Neither exposes a hosted environment an outside developer can register against. For both, the request-building and response-checking logic in this repo (`receiver/platforms/ashby_client.py`, `receiver/platforms/hibob_client.py`) is real and unit-tested — it is exercised against payloads built from each platform's own published webhook and API documentation (`receiver/simulators/`), not against a live account.

Nowhere in this project is a simulated call presented as a live one. If you're reading the code and it's not obvious which is which from the file it's in, that's a bug in the comments — file an issue against yourself and fix it. See `RESEARCH.md` for exactly what's sourced from where.

---

## What it does

- **Verifies three different webhook signature schemes correctly, separately.** Remote (HMAC-SHA256, hex, over `raw_body + ":" + timestamp`), Ashby (HMAC-SHA256, hex, `sha256=` prefix, over raw bytes), HiBob (HMAC-SHA512, base64). No shared "generic HMAC verifier" — see `receiver/signatures.py`'s docstring for why that abstraction was tried and reverted.
- **Dedupes by event ID, and separately, by fan-out.** A durable SQLite queue means a literal redelivery is a no-op. A second layer handles Ashby's `candidateHire` also firing `applicationUpdate` and `candidateStageChange` for the same hire — three event IDs, one `applicationId`, one downstream run.
- **Resolves identity through one table, never by email.** `receiver/person_mapping.py` — canonical ID, one row per human, every platform ID hangs off it, with a `merged_into` chain for the case where two records turn out to be the same person.
- **Talks to each platform through a wrapper that encodes what actually breaks integrations.** Ashby's `success: false`-inside-a-200. HiBob's WAF lockout on retried auth errors. Remote's per-company (not per-token) rate limit.
- **Runs one real end-to-end flow.** Simulated hire → fetch Remote's live country JSON schema → validate → create the employment in the sandbox. Dry-run by default; an idempotency key derived from `(event_id, target_system, operation)` stops a crashed-and-retried flow from creating the same employment twice.
- **Demonstrates the failure-philosophy disagreement directly.** `receiver/failure_demo.py` sends a real request to a real local server that always returns 500, then lays out — clearly labeled OBSERVED vs. DOCUMENTED — what each platform actually does next. Run it; the terminal output is the point.

---

## Wins

**Three signature schemes, implemented separately on purpose.** The temptation to write one `verify_signature(algorithm, ...)` helper is real and was deliberately not acted on — see the DEVLOG entry on why. Each platform signs a different thing over a different encoding; collapsing that into one function hides exactly the detail an integration engineer needs to see.

**The Ashby fan-out is handled and tested, not just described.** `tests/test_queue_dedupe.py::test_ashby_fan_out_collapses_to_one_run` sends all three real event shapes through the actual queue and asserts exactly one comes out `queued`. The other two are recorded (for audit — nothing is silently dropped) and marked as fan-out skips.

**Auth errors halt. They never retry.** `hibob_client.py` and `ashby_client.py` both raise a dedicated `*AuthError` on 401/403 that nothing in this codebase catches and retries. This is the one design decision repeated in three places (the two clients, and the DEVLOG entry explaining why) because getting it wrong doesn't just fail one call — a retry loop against a WAF-fronted auth failure can lock out every automation sharing that source IP.

**The failure-philosophy demo does something real.** It doesn't just print a table — it starts an actual local HTTP server, sends it real requests, and shows the real 500 that comes back, before explaining what each platform's real infrastructure does with that response. The distinction between what was just observed and what's documented from public sources is printed inline, not buried in a comment.

**16 unit tests, stdlib only.** Signature verification (valid, tampered, missing-header cases for all three platforms), queue dedup (exact redelivery, fan-out collapse, independent events), and person-mapping (creation, lookup by any platform ID, merge-chain resolution). `python -m unittest discover -s tests` — no install step.

---

## Constraints

**HiBob's exact WAF lockout number is asserted, not verified.** The 50-failures-in-10-seconds / 5-minute-block figure comes from the project brief, not from HiBob's public docs, which don't publish that specific threshold. Stated plainly in `RESEARCH.md` and in `hibob_client.py`'s docstring — the defensive design (never retry an auth failure) is correct regardless of the exact number, but the number itself isn't independently confirmed.

**The n8n workflow JSON is committed, not continuously run.** `n8n/workflows/*.json` are real, importable workflow definitions describing how the pieces are meant to connect — the receiver as the trust boundary (signature verification, dedup), n8n as the orchestration layer downstream of an already-verified event. They have not been executed against a live n8n instance as part of this repo; the logic that actually needed to be provably correct (signatures, dedup, person-mapping, the hire flow, the failure demo) is implemented and tested in the Python layer instead. Running the workflows for real means `docker compose up` plus real platform credentials — see below.

**The JSON Schema validator in `hire_flow.py` is a deliberate subset.** It checks `required` fields and top-level `type` matches — no `$ref`, no nested composition, no format validators. A full implementation is a solved problem (the `jsonschema` package); reimplementing it badly would be worse than reimplementing a known-partial version and saying so.

**Remote's write window isn't modeled with its own guard yet.** The hire flow creates an employment before any invite step exists in this project, so it never hits the "can't edit after invite" wall in practice — but a fuller build would need its own "has this person already been invited" check before calling update, because Remote's API error on a post-invite change doesn't explain why it failed. Documented in `RESEARCH.md`, not yet built.

**No live demo for Ashby or HiBob, by design, not by omission.** There's nothing to point a browser at for either — see the honesty note above.

---

## Roadmap

1. **A queue worker.** `receiver/queue.py` has `next_queued()` ready to be polled; there's no long-running worker process consuming it yet — the demos in this repo call the flow logic directly. A real worker loop is the natural next piece.
2. **The Remote pre-invite guard.** Check person-mapping status before attempting any post-creation update, and fail with a clear message rather than relying on Remote's error text.
3. **Execute the n8n workflows against a live local instance** and record the actual run, closing the gap named in Constraints above.
4. **A `jsonschema`-backed validator**, if this project ever needs to validate against a Remote schema with real composition or `$ref` — flagged here rather than added quietly, since it'd be the first external dependency in the receiver.

---

## Running it

### The receiver + tests (no external dependencies)

```bash
cd hr-webhook-integration-layer
cp .env.example .env   # fill in what you have; every var is documented inline

python3 -m unittest discover -s tests -v      # 16 tests, stdlib only
python3 -m receiver.failure_demo               # the centerpiece — run this first
python3 -m receiver.app                         # starts the receiver on :8787
```

The receiver and every platform wrapper are pure Python standard library — `http.server`, `hmac`, `hashlib`, `sqlite3`, `urllib` — the same "no external dependencies" choice made in `posthog-cs-health-intelligence/`. Nothing to `pip install`.

### The hire flow, live against the Remote sandbox

Requires real `REMOTE_CLIENT_ID` / `REMOTE_CLIENT_SECRET` from the Remote sandbox partner dashboard in your `.env`. With `DRY_RUN=true` (the default), it fetches the real schema and validates against it, then logs the employment payload it *would* send without sending it. Set `DRY_RUN=false` only once you're deliberately ready to write to the sandbox.

### n8n (self-hosted, Docker)

```bash
export N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)
docker compose up -d
# UI at http://localhost:5678 — import n8n/workflows/*.json
```

To register a webhook URL with any of the three platforms during development, tunnel n8n's webhook endpoint with ngrok. **Free ngrok is fine for local development only.** Its URLs are unauthenticated by default and rotate on restart — pointing a real HR data flow at one, even briefly, is a real exposure, not a shortcut. Don't use it against anything production-adjacent.

### Fixtures

`fixtures/*.json` are static, synthetic copies of what `receiver/simulators/` generates — useful for manually posting a signed request with `curl` without writing Python, or for importing directly into an n8n workflow as test data. No real person, company, or job posting appears anywhere in this repository.

---

## Stack

- **Receiver + platform wrappers:** Python 3, standard library only.
- **Workflow layer:** n8n, self-hosted via Docker, workflow JSON committed to this repo.
- **Storage:** SQLite (durable queue, person-mapping table, idempotency ledger).
- **Local tunnelling:** ngrok, dev-only.
- **Live integration:** Remote's public sandbox. Ashby and HiBob are documented-payload simulators — see the honesty note above and `RESEARCH.md`.
