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
| `project` | A built artifact — tool, app, prototype, or concrete deliverable. |
| `document` | A standalone written sample (documentation, guide, playbook). |

---

## 3. Facet: `domain` (1–3 per item)

Apply a domain only where the item **demonstrates substantive work** in it — not where the domain is mentioned in passing or where a tool associated with that domain is named.

| Value | Inclusion test |
|---|---|
| `customer-support` | Doing front-line or technical support directly with customers/users. |
| `support-ops` | Building or optimising a support system — tooling, processes, deflection, training. Distinct from doing the support. |
| `implementation-onboarding` | Configuring, rolling out, or onboarding customers onto a product or system. |
| `operations` | General business/process operations not better covered by a more specific domain. |
| `project-management` | Running projects: milestones, cross-org delivery, resourcing, stakeholder comms. |
| `people-hr` | HR, compliance, EOR, hiring frameworks, leadership coaching, people systems. |
| `community` | Community management, engagement, moderation, and growth. |
| `strategy` | Positioning, market entry, org/commercial strategy — explicit strategic work, not just thinking strategically. |
| `ai-engineering` | Building AI/LLM-backed tools: prompt architecture, model integration, output design. |
| `frontend-dev` | Client-side build work: HTML/CSS/JS, browser APIs, static site deployment. |
| `technical-writing` | Documentation, guides, playbooks, style/voice standards. |
| `content-creation` | YouTube, journalism, creator output, editorial content strategy. |
| `data-analysis` | SQL, product analytics, churn/LTV/retention modelling, dashboards. |
| `research` | Structured research and feasibility work with documented findings. |
| `security` | Cybersecurity work. **Flag rule**: any item tagged `security` must also appear in the audit's `flagged` list with note "in-training positioning — human review required." |

### Anti-rules (enforced strictly)

1. `people-hr` work is **never** `ai-engineering` or `frontend-dev`, even if a tool or platform is named.
2. `community` is **never** `strategy` by default. Only add `strategy` if the item shows explicit org/commercial strategy work.
3. `customer-support` (doing the support) and `support-ops` (building the system) are separate domains. Apply both only when the item genuinely shows both activities.
4. A passing mention of a tool or skill does not earn a domain tag. Demonstrated work does.

---

## 4. Facet: `evidence` (1–4 per item)

What does this item prove the person can do?

| Value | Inclusion test |
|---|---|
| `diagnostic-reasoning` | Traces a symptom to a structural cause rather than treating the surface. |
| `process-design` | Designed or redesigned how work flows — not just followed a process. |
| `cross-functional-influence` | Aligned multiple teams or functions toward a shared outcome. |
| `influence-without-authority` | Drove meaningful outcomes without formal power over the parties involved. |
| `technical-depth` | Demonstrates real technical capability: APIs, code, debugging, integration. |
| `customer-facing` | Direct relationship/communication with customers or external parties. |
| `writing-range` | Register or voice adaptation across different audiences or contexts. |
| `cost-discipline` | Explicit, documented attention to cost/efficiency trade-offs. |
| `build-in-public` | Transparent dev-log or decision documentation as it happened — not retrospective polish. |
| `scaling` | Grew an organisation, community, or audience materially (with evidence). |
| `self-serve-deflection` | Reduced demand on human effort by enabling people to help themselves. |
| `judgment-restraint` | Explicitly chose not to build or do something, with documented rationale. |
| `accessibility` | Accessibility-driven design or decisions — not just mentioning accessibility. |

---

## 5. Facet: `context`

Three independent sub-axes, applied where known:

**Stage** (where the work happened organisationally):
`startup` · `scaleup` · `enterprise` · `nonprofit-academic` · `agency-consulting` · `personal-project`

**Level** (the seniority/scope of the work):
`ic` · `lead` · `strategic`

**Engagement** (the nature of the relationship):
`employment` · `consulting` · `volunteer` · `personal`

---

## 6. Facet: `tools`

Controlled but extensible. New tools must be added here before use in `portfolio-index.json`, and noted in the audit's "New tools added" section.

### Baseline vocabulary (as of schema v1)

`zendesk` · `intercom` · `freescout` · `postman` · `api-debugging` · `har-analysis` · `sql` · `python` · `github-actions` · `n8n` · `asana` · `coda` · `claude-api` · `prompt-engineering` · `jina-reader` · `cloudflare-workers` · `tensorflow-js` · `html-css-js`

### Added in this pass (v1 initial tagging)

| Tool slug | Description | Added for |
|---|---|---|
| `foursquare-api` | Foursquare Places API — venue/restaurant search | date-proposal-website |
| `eventbrite-api` | Eventbrite API — event discovery | date-proposal-website |
| `tmdb-api` | The Movie Database API — film metadata | date-proposal-website |
| `icalendar` | RFC 5545 iCalendar format (.ics) — calendar invite generation | date-proposal-website |

---

## 7. Facet: `status` (projects and documents only)

| Value | Inclusion test |
|---|---|
| `live` | Deployed and publicly accessible. |
| `in-progress` | Active build; functional but not complete. |
| `research` | In research/planning phase; no shipped artifact yet. |
| `sample` | A portfolio writing sample rather than a shipped product. |
| `complete` | Finished; no longer actively maintained or extended. |

`status` is `null` for `work` and `case-study` type items.

---

## 8. Structured Fields

| Field | Type | Rules |
|---|---|---|
| `id` | string | Stable kebab-case slug derived from title. **Never rename after assignment.** |
| `schemaVersion` | integer | Increment when the schema shape changes. Currently `1`. |
| `type` | string | One of the four type values above. |
| `title` | string | The display title of the item. |
| `dateStart` | string | ISO `YYYY-MM` or `"present"`. Required for `work`, `case-study`, `project`. |
| `dateEnd` | string | ISO `YYYY-MM` or `"present"`. Required for `work`, `case-study`, `project`. |
| `status` | string or null | Required for `project` and `document`; `null` for `work` and `case-study`. |
| `domains` | array | 1–3 domain values. |
| `evidence` | array | 1–4 evidence values. |
| `context` | object | `{ stage, level, engagement }`. Fill all three sub-axes where known. |
| `tools` | array | Zero or more tool slugs from the controlled list. |
| `summary` | string | Reuses existing copy from the site. Do not rewrite. |
| `anchor` | string | In-page `#id` fragment or relative URL for standalone pages. |
| `relatedIds` | array | IDs of genuinely related items (role → case study, tool → case study it came from). |
| `audiencePin` | array | Lane names where this item is force-included regardless of facet query. Rare — document in `notes`. |
| `audienceExclude` | array | Lane names where this item is force-excluded. Rare — document in `notes`. |
| `lensByAudience` | object | Reserved for Phase 2; leave as `{}` in this pass. |
| `notes` | string | Free text for audit flags, classification rationale, or human-review prompts. |

---

## 9. Lane Query Definitions

Lanes are defined in `lanes.json`. This section is the human-readable reference.

| Lane | Include domains | Boost evidence | Max items |
|---|---|---|---|
| `cs-support` | `customer-support`, `support-ops` | `diagnostic-reasoning`, `self-serve-deflection`, `customer-facing` | 8 |
| `implementation` | `implementation-onboarding`, `support-ops` | `process-design`, `technical-depth`, `self-serve-deflection` | 6 |
| `ops-strategy` | `operations`, `strategy`, `project-management`, `people-hr` | `cross-functional-influence`, `influence-without-authority`, `process-design`, `cost-discipline` | 8 |
| `builder-technical` | `ai-engineering`, `frontend-dev` | `technical-depth`, `build-in-public`, `judgment-restraint` | 8 |
| `creator-lore` | `content-creation` | `writing-range`, `scaling`, `build-in-public` | 6 |
| `documentation` _(proposed)_ | `technical-writing` | `writing-range`, `technical-depth`, `process-design` | 6 |
| `people-hr` _(proposed)_ | `people-hr` | `process-design`, `cross-functional-influence`, `scaling` | 6 |

Proposed lanes are defined in `lanes.json` under `_proposed_*` keys and must not be surfaced until a human approves them. See `TAGGING-AUDIT.md §Flagged for decision`.

---

## 10. How to Tag a New Item

1. **Read this document first.** Confirm you understand the anti-rules before tagging.
2. **Assign `type`** — one value only. If ambiguous, see the `flagged` section in `TAGGING-AUDIT.md` for precedent.
3. **Assign `domain`** — 1 to 3 values. Apply only where the item _demonstrates_ work, not where a domain is mentioned. Re-read the anti-rules.
4. **Assign `evidence`** — 1 to 4 values. Be conservative. Over-tagging is a failure.
5. **Assign `context`** — fill all three sub-axes. Use `personal-project` for solo personal builds.
6. **Assign `tools`** — only tools actually used in the work. If a new tool is needed, add it to section 6 of this document first.
7. **Set `status`** — required for `project` and `document`; `null` for `work` and `case-study`.
8. **Set dates** — ISO `YYYY-MM`. If only a year is known, use `YYYY-01` and note the approximation in `notes`.
9. **Set `anchor`** — add a stable `id` attribute to the corresponding HTML element if one does not exist. No other HTML changes.
10. **Write `summary`** — copy the existing site description verbatim. Do not rewrite.
11. **Set `relatedIds`** — link to genuinely related items only.
12. **Update `TAGGING-AUDIT.md`** — re-run the validation pass and update stats.
13. **If anything is ambiguous** — add to `notes` and the audit's `flagged` list. Never guess silently.

---

## 11. Idempotency Contract

Re-running the tagging process on updated content must:
- **Extend** the index with new items.
- **Preserve** existing `id` values unchanged.
- **Never overwrite** `lensByAudience`, `audiencePin`, or `audienceExclude` values that have been set.
- **Flag** any item whose `id` would conflict with an existing entry for human resolution.
