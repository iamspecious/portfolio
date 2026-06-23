# Portfolio Taxonomy — Controlled Vocabulary & Maintenance Guide

This document is the authoritative reference for the portfolio metadata system. All future content must be classified through this document. No tag may be used that is not defined here. If a new value is needed, propose it here first — do not add it silently to `portfolio-index.json`.

---

## 1. Core Principle: Audience Routing Is Derived, Not Stored

Each content item is tagged only on **objective facets**: domain, evidence, context, dates, tools, type, status.

Audience lanes are defined as **queries over those facets** in `lanes.json`. A lane result is computed at query time from the tags — it is never stamped onto an item. The only per-item override mechanism is `audiencePin` and `audienceExclude` (arrays of lane names), reserved for genuine edge cases and always documented in `notes`.

---

## 2. Facet: `type` (exactly one per item)

| Value | Inclusion test |
|---|---|
| `work` | A paid or volunteer role held over time. |
| `case-study` | A narrative deep-dive into a specific problem solved and how. |
| `project` | A built, deployable artifact — a tool, site, or prototype. Must be demonstrable. |
| `document` | A standalone written deliverable: documentation, guide, playbook, or API reference. |

**Schema rule:** `status` must be `null` for `work` and `case-study` items. Only `project` and `document` carry a `status` value.

---

## 3. Facet: `domain` (1–3 per item; apply only where the item *demonstrates substantive work*)

| Value | Inclusion test |
|---|---|
| `customer-support` | Delivering direct support to end users — handling, resolving, communicating. |
| `support-ops` | Building or running the systems and processes that support teams operate within. |
| `implementation-onboarding` | Configuring, rolling out, or onboarding onto a product/system. |
| `operations` | Cross-functional operational work: workflows, processes, logistics, coordination. |
| `project-management` | Formal project management: planning, tracking, partner coordination, delivery. |
| `people-hr` | Hiring, HR compliance, EOR, team structure, retention, coaching, labour law. |
| `community` | Building, managing, or growing a community of people around a shared interest. |
| `strategy` | Strategic advisory or positioning work with documented real-world impact. |
| `ai-engineering` | Building AI-powered tools with real model integration (prompt, API, inference). |
| `frontend-dev` | Writing production-level HTML/CSS/JS with demonstrable shipped UI. |
| `technical-writing` | Writing documentation, guides, API references, or standards for technical audiences. |
| `content-creation` | Creating audience-facing content: articles, videos, scripts, editorial strategy. |
| `data-analysis` | Analysing data to generate insight — SQL, metrics, reporting, visualisation. |
| `research` | Structured research producing outputs (reports, designs, findings, literature reviews). |
| `security` | Substantive security work — threat modelling, incident response, pentesting. **Do not apply.** |
| `vendor-management` | *(proposed — not yet applied)* Negotiating, selecting, or managing third-party vendors or partners across multiple stakeholders; includes contract negotiation, supplier evaluation, and ongoing vendor relationships. |
| `events` | *(proposed — not yet applied)* Planning, coordinating, or executing events — in-person or virtual; includes logistics, venue, speaker/sponsor management, and attendee experience. |

### Anti-rules (enforced; violations are audit failures)
- `people-hr` is never `ai-engineering` or `frontend-dev`, even if a tool is named.
- `community` is not `strategy` by default — strategy requires documented advisory output.
- `customer-support` (doing support) ≠ `support-ops` (building the support system).
- A passing mention of a tool or skill earns no domain tag.
- `security` may not be applied to any current item — certifications are in-training only (flag in audit).

---

## 4. Facet: `evidence` (1–4 per item; what the item *proves* the person can do)

| Value | Inclusion test |
|---|---|
| `diagnostic-reasoning` | Traced a non-obvious root cause, structured a multi-branch diagnosis, or identified the real problem vs. the presented symptom. |
| `process-design` | Designed or rebuilt a workflow, system, or operational process. |
| `cross-functional-influence` | Coordinated across teams or stakeholders without direct authority. |
| `influence-without-authority` | Drove outcomes through relationship, visibility, or facilitation rather than reporting line. |
| `technical-depth` | Demonstrates substantial hands-on technical work — not just tool familiarity. |
| `customer-facing` | Substantive direct customer interaction: support, advocacy, communication. |
| `writing-range` | Shows breadth of register — technical, non-technical, or voice-adapted writing for different audiences. |
| `cost-discipline` | Made a decision informed by cost trade-offs, or optimised for cost without sacrificing outcome. |
| `build-in-public` | Documented the build process openly — decisions, pivots, constraints — not polished after the fact. |
| `scaling` | Grew something measurably: audience, team, process capacity. |
| `self-serve-deflection` | Reduced inbound volume by enabling users to answer their own questions. |
| `judgment-restraint` | Chose not to build, include, or act — scope discipline demonstrated explicitly. |
| `accessibility` | Demonstrated work on accessibility: design, assistive tech, inclusive practice. |

---

## 5. Facet: `context` (object; all three sub-fields required)

### `stage`
| Value | Inclusion test |
|---|---|
| `startup` | Early-stage company: pre-product-market-fit to Series A. |
| `scaleup` | Growth-stage company: Series A+, rapid hiring, scaling systems. |
| `enterprise` | Large, established organisation. |
| `nonprofit-academic` | Non-profit organisation or academic institution. |
| `agency-consulting` | Agency or consulting firm. |
| `personal-project` | Personal or self-directed work outside employment. |

### `level`
| Value | Inclusion test |
|---|---|
| `ic` | Individual contributor — did the work hands-on. |
| `lead` | Led a function, project, or small team with direct output responsibility. |
| `strategic` | Set direction, defined scope, or made decisions at an organisational level. |

### `engagement`
| Value | Inclusion test |
|---|---|
| `employment` | Salaried or contracted employment role. |
| `consulting` | External consulting engagement. |
| `volunteer` | Unpaid community or civic contribution. |
| `personal` | Self-directed personal project. |

---

## 6. Facet: `tools` (controlled; log additions in the audit)

Current approved values:
`zendesk` · `intercom` · `freescout` · `postman` · `api-debugging` · `har-analysis` · `sql` · `python` · `github-actions` · `claude-api` · `prompt-engineering` · `jina-reader` · `cloudflare-workers` · `tensorflow-js` · `html-css-js` · `coda` · `foursquare-api` · `eventbrite-api` · `tmdb-api` · `icalendar` · `scheduled-agent` · `ats-api` · `web-fetch` · `grep-parsing` · `excel-openpyxl` · `weighted-scoring-matrix` · `dealbreaker-gate` · `ai-assisted-scoring`

To add a new tool: add it here first, then use it in the index. Document in TAGGING-AUDIT.md under "New tools added."

---

## 7. Facet: `status` (projects and documents only; null for work and case-study)

| Value | Inclusion test |
|---|---|
| `live` | Deployed, accessible, and in active use. |
| `in-progress` | Actively being built; not yet at a stable release. |
| `research` | In research or planning phase; no shipped code or deliverable yet. |
| `sample` | A portfolio sample demonstrating skill — not a production deployment. |
| `complete` | Finished; not actively maintained or iterable. |

---

## 8. Dates

- `dateStart` / `dateEnd`: `YYYY-MM` format, or `"present"` for ongoing.
- Required for `work`, `case-study`, `project`. Optional but encouraged for `document`.
- When only the year is known, approximate with `YYYY-01` / `YYYY-12` and document in `notes`.

---

## 9. Audience Lanes (queries over facets — never stamped on items)

Defined in `lanes.json`. Summary:

| Lane | Tier | Matches domains |
|---|---|---|
| `cs-support` | primary | `customer-support`, `support-ops` |
| `implementation` | primary | `implementation-onboarding` |
| `ops-strategy` | primary | `operations`, `strategy`, `project-management`, `people-hr` |
| `people-hr` | primary | `people-hr`, `implementation-onboarding` |
| `builder-technical` | primary | `ai-engineering`, `frontend-dev` |
| `creator-lore` | primary | `content-creation` |
| `documentation` | secondary / cross-cutting | `technical-writing` |

`documentation` is cross-cutting: every primary lane should surface its top 1–2 `technical-writing` items as supporting evidence without those items leaving their home lane.

Items with `people-hr` domain will appear in **both** `ops-strategy` and `people-hr` lanes — this is intentional. The lanes are distinct hiring contexts with different boost signals.

---

## 10. `lensByAudience` and `sectionsByLane`

- `lensByAudience`: an object keyed by lane name. Value is a one-line framing of why this item is relevant for that lane's audience. Leave `{}` unless the item needs a custom framing.
- `sectionsByLane`: an object keyed by lane name. Value is an array of integer section numbers (for case studies with numbered sections) indicating which sections are most relevant for that lane.

Both fields are idempotent — re-running must extend, never overwrite, values already set.

---

## 11. Override fields

- `audiencePin: []` — array of lane names. Forces the item to appear in those lanes even if the query doesn't match.
- `audienceExclude: []` — array of lane names. Suppresses the item from those lanes even if the query matches.
- Both must be documented in `notes` with a rationale when non-empty.

---

## 12. How to tag a new item (checklist)

1. Assign a unique kebab-case `id` that won't clash with existing ids.
2. Choose `type` (one only).
3. Set `dateStart` / `dateEnd`. Use `"present"` if ongoing; approximate with `YYYY-01`/`YYYY-12` if only year is known.
4. Set `status` — `null` for `work` and `case-study`; one of the five values for `project` and `document`.
5. Apply `domains`: 1–3 maximum. Check anti-rules. If uncertain, use fewer tags and flag.
6. Apply `evidence`: 1–4 maximum. Each tag must be directly demonstrated, not implied.
7. Set `context`: all three sub-fields required.
8. List `tools` used. Add any new tools to §6 of this document first.
9. Write `summary`: one sentence, present tense, what it demonstrates.
10. Set `anchor`: `#id-attr` for page items; filename for standalone documents (use `pageAnchor` as secondary for the in-page entry).
11. Set `relatedIds`: other items in the index that substantiate or extend this one.
12. Leave `lensByAudience`, `sectionsByLane`, `audiencePin`, `audienceExclude` as empty defaults unless there's a specific reason to populate them.
13. Cross-check every tag against this document. If something doesn't fit, flag it in TAGGING-AUDIT.md — never invent a new tag mid-pass.
