# Routing Map & Missing-Role Diagnostic

Generated against `portfolio-index.json` (38 items), `lanes.json` v2, `front-door.js` current.
Read-only — no files modified.

---

## TASK 1 — Index completeness: work items

All 13 `work` entries confirmed present:

| id | title |
|---|---|
| `spec-solutions-fractional-cos` | Fractional Chief of Staff — Spec Solutions |
| `phandroid-tech-writer` | Contributing Tech Writer & Content Strategist — Phandroid |
| `connection-engine-cos` | Executive Assistant / Chief of Staff — Connection Engine |
| `the-nook-community-manager` | Community Manager — The Nook |
| `stamped-support-hero` | Customer Support Hero (Technical) — Stamped |
| `can-i-play-that-editor` | Editor & Operations Assistant — Can I Play That? |
| `itc-community-manager` | Community Manager — Irish Tech Community |
| `samebug-developer-advocate` | Developer Advocate — Samebug |
| `learnovate-pm-research` | Project Manager & Research Assistant — Learnovate Centre |
| `coderdojo-support-specialist` | Customer Support Specialist — CoderDojo ✓ |
| `donnerwood-product-analyst` | Product Analyst — Donnerwood Media (Meez) |
| `leaguepedia-chief-of-people` | Chief of People (Operations & Communications) — Leaguepedia |
| `vodafone-support-specialist` | Customer Support Specialist — Vodafone ✓ |

Both CoderDojo and Vodafone exist in the index. This is **not a merge drop** — they were never removed. The cause is elsewhere.

---

## TASK 2 — CoderDojo and Vodafone diagnosis

### `coderdojo-support-specialist`

- **domains:** `["customer-support"]`
- **evidence:** `["customer-facing", "process-design"]`
- **dateEnd:** `2016-01`
- **Lane query match:** Yes — `customer-support` is in `cs-support.include.domains`.
- **Boost score vs cs-support signals** (`diagnostic-reasoning`, `self-serve-deflection`, `customer-facing`): 1 (`customer-facing` only)

### `vodafone-support-specialist`

- **domains:** `["customer-support"]`
- **evidence:** `["customer-facing"]`
- **dateEnd:** `2011-09`
- **Lane query match:** Yes — `customer-support` is in `cs-support.include.domains`.
- **Boost score vs cs-support signals:** 1 (`customer-facing` only)

### Why they're not appearing: the cap

Both roles correctly match the `cs-support` query. The issue is `maxItems: 8` in `lanes.json`. There are **13 items** matching `cs-support`; the query returns only 8 after sorting by boost score → `dateEnd` descending. CoderDojo (2016-01) and Vodafone (2011-09) rank 12th and 13th respectively and are sliced off.

The items ahead of them — occupying positions 6, 7, 8 — are three AI/support-ops projects (`posthog-csm-copilot`, `faq-chatbot`, `support-triage-tool`), all with dateEnd `"present"` and a boost score of 1, which pushes them above any older score-1 role with a historical dateEnd.

**Full cs-support ranked list** (all 13 matching items, sorted by score → dateEnd desc):

| Rank | id | score | dateEnd | Shown? |
|---|---|---|---|---|
| 1 | `denim-brand-turnaround` | 3 | 2024-12 | ✓ |
| 2 | `spec-solutions-fractional-cos` | 2 | present | ✓ |
| 3 | `spec-solutions-support-ops` | 2 | present | ✓ |
| 4 | `stamped-support-hero` | 2 | 2020-07 | ✓ |
| 5 | `stamped-widget-diagnostic` | 2 | 2020-07 | ✓ |
| 6 | `posthog-csm-copilot` | 1 | present | ✓ |
| 7 | `faq-chatbot` | 1 | present | ✓ |
| 8 | `support-triage-tool` | 1 | present | ✓ |
| 9 | `posthog-cs-health-intelligence` | 1 | 2026-05 | ✗ hidden |
| 10 | `optimising-cs-operations` | 1 | 2024-09 | ✗ hidden |
| 11 | `samebug-developer-advocate` | 1 | 2017-09 | ✗ hidden |
| **12** | **`coderdojo-support-specialist`** | **1** | **2016-01** | **✗ hidden** |
| **13** | **`vodafone-support-specialist`** | **1** | **2011-09** | **✗ hidden** |
| (14) | `technical-writing-portfolio` | 0 | 2026-05 | ✗ hidden |
| (15) | `saas-integration-diagnostic-guide` | 0 | 2026-05 | ✗ hidden |

**Conclusion for both roles:** Correctly tagged. Not capped by under-tagging or wrong domain — capped by `maxItems: 8` combined with three AI projects holding the score-1 "present" slots above them.

---

## TASK 3 — Full routing map

The `queryLane` function in `front-door.js` filters only on domain match. Note: **`audienceExclude` and `audiencePin` are not implemented in the JS** — these fields exist in the index but the renderer ignores them entirely (see Task 5 finding).

Lanes computed from domain queries only:

### WORK

| id | title | domains | evidence (for reference) | → lanes |
|---|---|---|---|---|
| `spec-solutions-fractional-cos` | Fractional Chief of Staff — Spec Solutions | support-ops, people-hr, operations | process-design, cross-functional-influence, self-serve-deflection, cost-discipline, diagnostic-reasoning | cs-support, ops-strategy, people-hr |
| `phandroid-tech-writer` | Contributing Tech Writer & Content Strategist — Phandroid | content-creation | writing-range, scaling | creator-lore |
| `connection-engine-cos` | Executive Assistant / Chief of Staff — Connection Engine | project-management, community, operations | process-design, cross-functional-influence | ops-strategy |
| `the-nook-community-manager` | Community Manager — The Nook | community | scaling, customer-facing | **none** |
| `stamped-support-hero` | Customer Support Hero (Technical) — Stamped | customer-support, support-ops | diagnostic-reasoning, technical-depth, customer-facing | cs-support |
| `can-i-play-that-editor` | Editor & Operations Assistant — Can I Play That? | operations, content-creation | cross-functional-influence, scaling | ops-strategy, creator-lore |
| `itc-community-manager` | Community Manager — Irish Tech Community | community, operations | scaling, process-design, cross-functional-influence | ops-strategy |
| `samebug-developer-advocate` | Developer Advocate — Samebug | customer-support, community | technical-depth, customer-facing | cs-support |
| `learnovate-pm-research` | Project Manager & Research Assistant — Learnovate | project-management, research | cross-functional-influence, influence-without-authority, process-design | ops-strategy |
| `coderdojo-support-specialist` | Customer Support Specialist — CoderDojo | customer-support | customer-facing, process-design | cs-support (rank 12, capped) |
| `donnerwood-product-analyst` | Product Analyst — Donnerwood Media (Meez) | data-analysis | diagnostic-reasoning, cost-discipline | **none** |
| `leaguepedia-chief-of-people` | Chief of People — Leaguepedia | people-hr, operations | scaling, process-design, cross-functional-influence | ops-strategy, people-hr |
| `vodafone-support-specialist` | Customer Support Specialist — Vodafone | customer-support | customer-facing | cs-support (rank 13, capped) |

### CASE-STUDY

| id | title | domains | evidence | → lanes |
|---|---|---|---|---|
| `stamped-widget-diagnostic` | Diagnosing a Widget That Failed Four Different Ways | customer-support, support-ops | diagnostic-reasoning, technical-depth, customer-facing | cs-support |
| `spec-solutions-support-ops` | Turning a Gmail Inbox Into an Actual Support System | support-ops, customer-support, implementation-onboarding | process-design, self-serve-deflection, diagnostic-reasoning, cost-discipline | cs-support, implementation, people-hr |
| `learnovate-develop-project` | Keeping a €3M Project Aligned Across Borders | project-management | influence-without-authority, cross-functional-influence, process-design | ops-strategy |
| `tiktok-sponsorship-strategy` | Sponsorship Strategy for a TikTok Personality | content-creation, strategy | cross-functional-influence | creator-lore, ops-strategy |
| `business-relocation-expansion` | Business Relocation & Expansion Strategy | people-hr, strategy | cross-functional-influence, process-design | ops-strategy, people-hr |
| `leadership-coaching-project` | Leadership Coaching for a Growing Team | people-hr | cross-functional-influence | ops-strategy, people-hr |
| `optimising-cs-operations` | Optimising Customer Support Operations | support-ops | process-design, self-serve-deflection, cost-discipline | cs-support |
| `niche-market-web-dev-strategy` | Niche Market Strategy for Web Development | strategy | diagnostic-reasoning, cross-functional-influence | ops-strategy |
| `denim-brand-turnaround` | Rebuilding a Denim Brand, Top to Tail | support-ops, customer-support, operations, implementation-onboarding, ai-engineering, content-creation, people-hr, strategy | (9 signals) | cs-support, implementation, ops-strategy, people-hr, builder-technical, creator-lore |

### PROJECT

| id | title | domains | evidence | → lanes |
|---|---|---|---|---|
| `error-log-interpreter` | Error Log Interpreter | ai-engineering, frontend-dev | technical-depth, build-in-public, judgment-restraint | builder-technical |
| `debug-helper` | Debug Helper | ai-engineering, frontend-dev | technical-depth, build-in-public, judgment-restraint | builder-technical |
| `posthog-cs-health-intelligence` | PostHog CS Health Intelligence | support-ops, data-analysis | diagnostic-reasoning, process-design, judgment-restraint, build-in-public, cost-discipline | cs-support |
| `posthog-csm-copilot` | PostHog CSM Copilot | ai-engineering, support-ops | technical-depth, build-in-public, judgment-restraint, diagnostic-reasoning | cs-support, builder-technical |
| `faq-chatbot` | FAQ Chatbot | ai-engineering, support-ops | technical-depth, build-in-public, self-serve-deflection, judgment-restraint | cs-support, builder-technical |
| `lorebyspec-creator-tool` | LoreBySpec Creator Tool | ai-engineering, content-creation | technical-depth, build-in-public | builder-technical (rank 10, capped), creator-lore |
| `pregvoice` | PregVoice | research | accessibility, diagnostic-reasoning, build-in-public, judgment-restraint | **none** |
| `support-triage-tool` | Support Ticket Triage Tool | ai-engineering, support-ops | technical-depth, build-in-public, self-serve-deflection, judgment-restraint | cs-support, builder-technical |
| `kh-lore-checker` | KH Lore Consistency Checker | ai-engineering, content-creation | technical-depth, build-in-public, judgment-restraint | builder-technical, creator-lore |
| `date-proposal-website` | Date Proposal Website | frontend-dev, research | technical-depth, build-in-public, judgment-restraint, diagnostic-reasoning | builder-technical |
| `proj-digital-spec-front-door` | Digital Spec — Portfolio Front Door | frontend-dev | build-in-public, technical-depth, process-design, judgment-restraint | builder-technical |

### DOCUMENT

| id | title | domains | evidence | → lanes (JS actual) |
|---|---|---|---|---|
| `technical-writing-portfolio` | Technical Writing Portfolio | technical-writing, support-ops, people-hr | writing-range, technical-depth, process-design, judgment-restraint | documentation, cs-support, people-hr, **ops-strategy** *(audienceExclude ignored by JS)* |
| `saas-integration-diagnostic-guide` | SaaS Integration Failure Diagnostic Guide | technical-writing, support-ops | writing-range, technical-depth, process-design | documentation, cs-support |
| `cat-api-documentation` | Cat API Documentation | technical-writing | writing-range, technical-depth | documentation |
| `voice-and-tone-guide` | Voice & Tone Guide | technical-writing | writing-range, process-design | documentation |
| `voice-adaptation-showcase` | Voice Adaptation Showcase | technical-writing | writing-range, judgment-restraint | documentation |

---

## TASK 4 — Flagged mismatches

### A. Roles with "support" / "customer" in the title not appearing in cs-support

| Item | In cs-support query? | Cause of non-appearance |
|---|---|---|
| `coderdojo-support-specialist` | ✓ matches | Capped — rank 12 of 13, maxItems 8 |
| `vodafone-support-specialist` | ✓ matches | Capped — rank 13 of 13, maxItems 8 |
| `optimising-cs-operations` | ✓ matches | Capped — rank 10, hidden |
| `samebug-developer-advocate` | ✓ matches (customer-support domain) | Capped — rank 11, hidden |

No under-tagging in this group. All four match the query; all four are hidden by the cap.

### B. Implementation / onboarding items

`implementation` lane currently has 2 items: `spec-solutions-support-ops` and `denim-brand-turnaround`. Neither is capped (maxItems 6). The lane is thin but correctly tagged. No gap here.

### C. People / HR / EOR roles

| Item | In people-hr query? | Cause of non-appearance |
|---|---|---|
| `leadership-coaching-project` | ✓ matches (people-hr domain) | Capped — rank 7, maxItems 6. Hidden from people-hr |
| `spec-solutions-support-ops` | ✓ matches (implementation-onboarding) | Shown at rank 5 |
| `technical-writing-portfolio` | ✓ matches (people-hr domain) | Shown at rank 6 — this is marginal (documentation item, not a people-hr output) |

`leadership-coaching-project` — a genuine people-hr item — is displaced from the people-hr lane by `technical-writing-portfolio` ranking one slot above it.

### D. Items routing to no lane

| Item | Domains | Why unrouted | Type |
|---|---|---|---|
| `the-nook-community-manager` | community | `community` is in no lane | work |
| `donnerwood-product-analyst` | data-analysis | `data-analysis` is in no lane | work |
| `pregvoice` | research | `research` is in no lane | project |

These were flagged and accepted in the prior audit. No action implied here; flagged for completeness.

### E. `audienceExclude` not enforced — structural bug

`technical-writing-portfolio` has `audienceExclude: ["ops-strategy"]` set in the index, but `front-door.js` does not check this field. As a result the item appears in the ops-strategy lane at rank 7, displacing `business-relocation-expansion` and `connection-engine-cos` which do not make the cut. The `audienceExclude` field is currently an intent-only annotation with no rendering effect.

---

## TASK 5 — Display cap

### Cap mechanism

`front-door.js` `queryLane()` (lines 397–422) applies a per-lane `maxItems` limit as a hard slice:

```js
var max = lane.maxItems || 8;
// …
return items.slice(0, max).map(function (x) { return x.item; });
```

Items are first filtered by domain match, then sorted by evidence boost score (descending) then `dateEnd` (descending, `"present"` → `"9999-99"`). The top `maxItems` are returned; everything else is silently dropped.

There is **no `audiencePin` or `audienceExclude` logic anywhere in the file**. Both override fields are parsed out of `portfolio-index.json` but never read by the renderer. This is a separate bug from the capping issue.

### Items currently hidden per lane

**`cs-support`** (maxItems 8, 15 candidates, 7 hidden):

| Rank | id | Reason hidden |
|---|---|---|
| 9 | `posthog-cs-health-intelligence` | Score 1, 2026-05 — below three "present" score-1 AI tools |
| 10 | `optimising-cs-operations` | Score 1, 2024-09 |
| 11 | `samebug-developer-advocate` | Score 1, 2017-09 |
| 12 | `coderdojo-support-specialist` | Score 1, 2016-01 |
| 13 | `vodafone-support-specialist` | Score 1, 2011-09 |
| 14 | `technical-writing-portfolio` | Score 0 (no cs-support boost signals) |
| 15 | `saas-integration-diagnostic-guide` | Score 0 |

**`ops-strategy`** (maxItems 8, 13 candidates, 5 hidden):

| Rank | id | Reason hidden |
|---|---|---|
| 9 | `business-relocation-expansion` | Score 2, 2024-12 — displaced by `technical-writing-portfolio` which should be excluded |
| 10 | `can-i-play-that-editor` | Score 2, 2020-02 |
| 11 | `tiktok-sponsorship-strategy` | Score 1, 2025-01 |
| 12 | `leadership-coaching-project` | Score 1, 2024-12 |
| 13 | `niche-market-web-dev-strategy` | Score 1, 2023-02 |

Note: `technical-writing-portfolio` appears at rank 7 in ops-strategy only because `audienceExclude` is not implemented. If it were enforced, `business-relocation-expansion` and `connection-engine-cos` would both fit within the cap.

**`people-hr`** (maxItems 6, 7 candidates, 1 hidden):

| Rank | id | Reason hidden |
|---|---|---|
| 7 | `leadership-coaching-project` | Score 1, 2024-12 — displaced by `technical-writing-portfolio` at rank 6 |

**`builder-technical`** (maxItems 8, 10 candidates, 2 hidden):

| Rank | id | Reason hidden |
|---|---|---|
| 9 | `denim-brand-turnaround` | Score 3, 2024-12 — all 8 slots taken by score-3 "present" projects |
| 10 | `lorebyspec-creator-tool` | Score 2, present |

**`implementation`** (maxItems 6, 2 candidates): No items hidden.

**`creator-lore`** (maxItems 6, 6 candidates): No items hidden — exactly fills the cap.

**`documentation`** (maxItems 6, 5 candidates): No items hidden.

---

## Recommendations (diagnose only — no fixes applied)

### 1. Raise `cs-support` maxItems (or type-restrict the cap)

**Root cause of CoderDojo and Vodafone not appearing:** three AI projects with `support-ops` domain and `dateEnd: "present"` occupy score-1 positions that should belong to the two historical support roles. The projects are legitimately in the lane (they demonstrate support-ops work) but they crowd out the proven employment track record.

**Options (ranked by simplicity):**
- Raise `maxItems` from 8 to 10 or 12 in `lanes.json`. This is a one-line change and surfaces all hidden work roles.
- Alternatively, add `diagnostic-reasoning` or `self-serve-deflection` to `coderdojo-support-specialist` evidence if the work genuinely shows it (knowledge base contribution and trend analysis could support `diagnostic-reasoning`). This lifts the score to 2 and pushes it above the AI tools.
- Alternatively, implement `audienceExclude`-style type filtering so `project` items don't compete with `work` items for cs-support slots — but this is a more substantial JS change.

### 2. Implement `audienceExclude` in `front-door.js`

The field is set on `technical-writing-portfolio` with `ops-strategy` excluded, but the renderer ignores it. A two-line filter addition to `queryLane()` would make it effective and fix the displacement of `business-relocation-expansion` from ops-strategy and `leadership-coaching-project` from people-hr.

### 3. `leadership-coaching-project` disappears from `people-hr`

Displaced by `technical-writing-portfolio` at rank 6. Fixing recommendation 2 (audienceExclude enforcement) will resolve this indirectly, since `technical-writing-portfolio` would be excluded from people-hr only if you also add `people-hr` to its `audienceExclude`. Currently it's only excluded from ops-strategy. If you want it out of people-hr too, add that; or raise `people-hr` maxItems to 7.

### 4. `denim-brand-turnaround` hidden from `builder-technical`

Eight score-3-present projects fill all builder-technical slots. `denim-brand-turnaround` ranks 9th (same score 3 but older dateEnd). Raise maxItems from 8 to 9 or 10, or add `audiencePin: ["builder-technical"]` to `denim-brand-turnaround` once audiencePin is implemented.

### 5. `technical-writing-portfolio` in `cs-support`

It currently matches cs-support via `support-ops` domain but has no boost signal overlap with that lane — score 0. It will only appear if the cap is raised high enough (it's rank 14 of 15). No action needed for now; it's not displacing anything meaningful at position 14.

### 6. `audiencePin` / `audienceExclude` implementation (structural)

Both fields are dead in the current renderer. Until implemented, all `audiencePin` and `audienceExclude` entries in the index are documentation-only. A single guard in `queryLane()` handles both:

```js
// After the domain-match filter, before scoring:
items = items.filter(function (item) {
  return !item.audienceExclude || item.audienceExclude.indexOf(laneId) < 0;
});
// After slicing, for audiencePin:
// (requires a separate pass before slicing to guarantee pinned items survive the cut)
```
