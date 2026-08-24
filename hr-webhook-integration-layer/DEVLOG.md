# DEVLOG — HR Webhook Integration Layer

Written as decisions happen, not reconstructed after the fact.

---

## Entry 001 — Reading the brief, and what "real" would actually mean here

**Date:** August 2026
**Status:** Scoping

The brief for this project is a demonstration piece for a People Ops Automation role, built around three HR platforms whose webhook failure semantics genuinely disagree with each other. Before writing anything, the question that mattered most: what does "real" mean when only one of the three platforms has a public sandbox?

The honest answer, decided here and not revisited: Remote gets real API calls, because it's the only one that can receive them. Ashby and HiBob get wrappers that are real code, exercised against payloads built from their own published docs. Nowhere does the project get to blur that line for effect — a demo built for a People Ops audience is exactly the audience that would notice, and exactly the audience where getting caught overstating an integration's realness would cost more than the demo is worth.

---

## Entry 002 — Research first, and where the docs went dark

**Date:** August 2026
**Status:** Research

Started by trying to fetch each platform's developer docs directly. `developer.remote.com`, `developers.ashbyhq.com`, and `apidocs.hibob.com` are all blocked by this environment's egress proxy — direct fetches failed outright. Fell back to search, which worked and actually produced better-organized findings than raw doc scraping would have, since search summaries pulled the exact header names and behaviors out of long doc pages.

What that means for `RESEARCH.md`: everything in it is sourced from what search results surfaced from those domains, not from having read the full doc pages top to bottom. I'm noting that here rather than letting the citations imply more direct access than there was — a URL cited in RESEARCH.md means "this is where the claim traces back to," not "I browsed this page personally."

One thing search couldn't confirm at all: the specific HiBob WAF lockout numbers (50 failures, 10 seconds, 5-minute block) from the brief. General WAF/rate-limit behavior for HiBob is documented; that specific threshold isn't, at least not anywhere search surfaced. Flagged in RESEARCH.md and in `hibob_client.py` rather than presented as confirmed.

---

## Entry 003 — The shared-signature-helper instinct, and why it didn't get built

**Date:** August 2026
**Status:** Design

Before writing `signatures.py`, the natural shape to reach for is one function: `verify_signature(algorithm, raw_body, secret, header, ...)`, dispatching on a platform argument. It would have been maybe 15 lines shorter.

Didn't build it, for a specific reason rather than a vague "keep it simple" instinct: the three schemes don't just use different algorithms, they sign different *things*. Remote signs `raw_body + ":" + timestamp` — a concatenation that doesn't exist for the other two. Ashby's header carries an algorithm prefix (`sha256=`) that has to be stripped before comparison; HiBob's doesn't. A shared function ends up either with a pile of `if platform == "remote"` branches inside it — which is just the three separate functions with extra indirection — or, worse, with a generic `signed_payload` parameter that quietly assumes every scheme signs some derivable transform of `(body, secret)`, which is the exact assumption that would make it easy to plug in the wrong construction for the wrong platform and not notice until a real signature failed to verify in production. Three named functions, each with a docstring citing its actual source, cost 15 lines and bought back "you cannot mix these up without the mistake being visible in a diff."

---

## Entry 004 — Building the fan-out test before trusting the fan-out logic

**Date:** August 2026
**Status:** Building

`receiver/queue.py`'s two-level dedup (event-ID primary key, `fan_out_key` for Ashby's three-events-one-hire case) was straightforward to write. Trusting it was a different matter — the failure mode if it's wrong is quiet: three events queue instead of one, a downstream flow runs three times, and nothing about the *code* looks broken.

So `tests/test_queue_dedupe.py::test_ashby_fan_out_collapses_to_one_run` runs the actual three-event payloads from `simulators/ashby_payloads.py` — not a hand-simplified stand-in — through the actual `queue.enqueue()`, and asserts on the row count in each state (3 total rows recorded, exactly 1 `queued`). Ran it before wiring the receiver's HTTP layer to the queue at all, specifically so a bug here would show up as a failing assertion with a clear name, not as a mysterious triple-run three files later.

When the full receiver smoke test ran later (Entry 006), the fan-out behaved exactly as the unit test predicted — `candidateStageChange` queued, `applicationUpdate` and `candidateHire` both came back `fan_out_skip`, in that order, matching the order Ashby actually sends them. Good sign, but the unit test is what I'd have trusted regardless of how the smoke test looked; a smoke test that happens to pass once tells you less than an assertion that names exactly what it's checking.

---

## Entry 005 — Auth errors halt. Writing that rule down cost more than writing the retry logic would have.

**Date:** August 2026
**Status:** Design

The single most consequential line in this codebase is arguably the *absence* of a line: there is no retry-with-backoff wrapped around any call in `hibob_client.py` or `ashby_client.py`. Every other kind of failure in this project gets some form of resilience thinking — the queue is durable, the idempotency key protects against double-writes, the failure-philosophy demo exists specifically to reason about retry behavior. Auth failures get none of that, on purpose, and it's worth being explicit about why the asymmetry is correct rather than an oversight.

A 401/403 from an expired token or a wrong key doesn't get fixed by trying again — the same bad credential goes out again and fails again. For most APIs that's just wasted requests. For HiBob specifically, per the brief, it's worse: enough of those in a short enough window trips a WAF-level IP block that takes down every automation sharing that source IP for five minutes, not just the one that caused it. I couldn't independently confirm the exact numbers (Entry 002), but the shape of the failure — an auth-sensitive API behind a WAF that blocks on repeated 401/403 — is exactly what you'd expect from any API taking security seriously, and the correct response doesn't depend on knowing the precise threshold.

So both platform clients raise a dedicated `AuthError` subclass on 401/403 that nothing catches and retries. Remote's client is the deliberate exception — it retries exactly once on a 401, and the docstring explains why that's a different situation: an OAuth2 bearer token expiring is routine, self-healing behavior, not a credential problem. Same status code, opposite correct response, and I wanted that contrast written down somewhere obvious rather than left as an inconsistency someone has to reverse-engineer later.

---

## Entry 006 — First real end-to-end smoke test, and a nuance I hadn't planned for

**Date:** August 2026
**Status:** Testing

Ran the receiver for real: started it as a subprocess, sent it actual HTTP requests with correctly-computed signatures for all three platforms (including the full Ashby fan-out and a deliberately-wrong signature for each platform to confirm rejection), and inspected the resulting SQLite state. All of it worked on the first full run — the fan-out collapsed as expected, the invalid signatures got 401s, the ping events were acknowledged and correctly treated as no-ops rather than queued.

Then tested `hire_flow.py`'s dry-run/idempotency interaction and found a real nuance I hadn't thought through at design time: running the same event through `run_hire_flow()` twice in dry-run mode prints "would send" *both* times, not "would send" then "already done." That's because the idempotency ledger (`idempotent_calls`) is only written on an actual create call — dry-run never writes to it, since dry-run doesn't do anything the ledger would need to protect against a repeat of. On reflection this is the correct behavior, not a bug: idempotency exists to stop a duplicate *write*, and a dry run has nothing to duplicate. But it's a real design detail that wasn't obvious until the test surfaced it, and worth naming here rather than letting the README claim the idempotency check "just works" without saying which mode it actually applies to.

---

## Entry 007 — What the failure-philosophy demo can and can't show live

**Date:** August 2026
**Status:** Design / building

The brief asks for a script that returns HTTP 500 to each platform's delivery and shows what each does next. The honest version of that script can't fully deliver on "shows what each does" for all three platforms live — doing so for Ashby or HiBob would mean driving a real webhook subscription on a real account into a disabled or deactivated state, which isn't something a portfolio demo should be doing to anyone's real tenant even if one were available. And for Remote, fully demonstrating it live would need a provisioned sandbox company with an actual registered webhook and a real triggering event, which is more sandbox setup than this project assumes anyone running it will have done.

So `failure_demo.py` does the part that's genuinely demonstrable — a real local server that returns a real 500 to a real request, for all three platforms' request shapes — and labels the rest DOCUMENTED, sourced from RESEARCH.md, printed inline rather than hidden in a comment. When `REMOTE_CLIENT_ID`/`REMOTE_CLIENT_SECRET` are set, it also makes one real authenticated call against the sandbox (`list_webhook_events`) to prove connectivity, clearly marked OBSERVED. Ran it without credentials configured first, to make sure the no-credentials path degrades honestly instead of pretending — it does; it says plainly that the live section is being skipped and why.

---

## Entry 008 — What's still not built

**Date:** August 2026
**Status:** Scoping, logged deliberately

Three things intentionally left out, named here rather than left implicit:

A real queue worker. `next_queued()` exists and is tested, but there's no long-running process consuming it — the demos in this repo call the flow logic directly rather than through a worker loop. The receiver and the processing logic are decoupled specifically so that worker can be added without touching either side, but it isn't written yet.

A pre-invite guard for Remote's write-window close. The hire flow in this project never reaches the post-invite state, so it never needed one — but a fuller build would, and RESEARCH.md says why plainly rather than letting the gap go unmentioned.

The n8n workflows are committed but not run against a live instance in this repo. They're real, importable workflow JSON describing the intended orchestration shape — the receiver as trust boundary, n8n downstream of an already-verified event — not something with a recorded live execution behind it yet. Said so directly in the README rather than letting committed JSON imply more than it's shown.
