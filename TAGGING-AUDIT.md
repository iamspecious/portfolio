# Tagging Audit Report — Portfolio Index v1

Generated against `portfolio-index.json` schemaVersion 1.  
Date of pass: 2026-06-19.

---

## 1. Coverage

**Total items inventoried: 36**

| # | ID | Type | Domains | Evidence | Context | Dates | Status |
|---|---|---|---|---|---|---|---|
| 1 | spec-solutions-fractional-cos | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 2 | phandroid-tech-writer | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 3 | connection-engine-cos | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 4 | the-nook-community-manager | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 5 | stamped-support-hero | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 6 | can-i-play-that-editor | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 7 | itc-community-manager | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 8 | samebug-developer-advocate | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 9 | learnovate-pm-research | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 10 | coderdojo-support-specialist | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 11 | donnerwood-product-analyst | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 12 | leaguepedia-chief-of-people | work | ✓ | ✓ | ✓ | ✓† | n/a |
| 13 | vodafone-support-specialist | work | ✓ | ✓ | ✓ | ✓ | n/a |
| 14 | stamped-widget-diagnostic | case-study | ✓ | ✓ | ✓ | ✓ | n/a |
| 15 | spec-solutions-support-ops | case-study | ✓ | ✓ | ✓ | ✓ | n/a |
| 16 | learnovate-develop-project | case-study | ✓ | ✓ | ✓ | ✓ | n/a |
| 17 | error-log-interpreter | project | ✓ | ✓ | ✓ | ✓ | live |
| 18 | debug-helper | project | ✓ | ✓ | ✓ | ✓ | live |
| 19 | posthog-cs-health-intelligence | project | ✓ | ✓ | ✓ | ✓ | complete |
| 20 | posthog-csm-copilot | project | ✓ | ✓ | ✓ | ✓ | in-progress |
| 21 | faq-chatbot | project | ✓ | ✓ | ✓ | ✓ | live |
| 22 | lorebyspec-creator-tool | project | ✓ | ✓ | ✓ | ✓ | live |
| 23 | pregvoice | project | ✓ | ✓ | ✓ | ✓ | research |
| 24 | support-triage-tool | project | ✓ | ✓ | ✓ | ✓ | live |
| 25 | kh-lore-checker | project | ✓ | ✓ | ✓ | ✓ | in-progress |
| 26 | date-proposal-website | project | ✓ | ✓ | ✓ | ✓ | in-progress |
| 27 | tiktok-sponsorship-strategy | project | ✓ | ✓ | ✓ | ✓ | complete |
| 28 | business-relocation-expansion | project | ✓ | ✓ | ✓ | ✓ | complete |
| 29 | leadership-coaching-project | project | ✓ | ✓ | ✓ | ✓ | complete |
| 30 | optimising-cs-operations | project | ✓ | ✓ | ✓ | ✓ | complete |
| 31 | niche-market-web-dev-strategy | project | ✓ | ✓ | ✓ | ✓ | complete |
| 32 | technical-writing-portfolio | document | ✓ | ✓ | ✓ | ✓ | sample |
| 33 | saas-integration-diagnostic-guide | document | ✓ | ✓ | ✓ | ✓ | sample |
| 34 | cat-api-documentation | document | ✓ | ✓ | ✓ | ✓ | sample |
| 35 | voice-and-tone-guide | document | ✓ | ✓ | ✓ | ✓ | sample |
| 36 | voice-adaptation-showcase | document | ✓ | ✓ | ✓ | ✓ | sample |

**† Approximation**: `leaguepedia-chief-of-people` dates only given as "2012–2014" in the source. Used `2012-01` / `2014-12` as approximations. Note recorded in item's `notes` field.

**Orphans**: Zero. Every item has all required facets populated.

---

## 2. Vocabulary Compliance

### Domain tags used

All domain values used are from the controlled vocabulary: `customer-support`, `support-ops`, `operations`, `project-management`, `people-hr`, `community`, `strategy`, `ai-engineering`, `frontend-dev`, `technical-writing`, `content-creation`, `data-analysis`, `research`.

**`security` used**: No. Not applied to any item (see §4 below).  
**`implementation-onboarding` used**: No. Not applied to any item (see §4 below).  
**Vocabulary violations**: Zero.

### Evidence tags used

All values are from the controlled vocabulary: `diagnostic-reasoning`, `process-design`, `cross-functional-influence`, `influence-without-authority`, `technical-depth`, `customer-facing`, `writing-range`, `cost-discipline`, `build-in-public`, `scaling`, `self-serve-deflection`, `judgment-restraint`, `accessibility`.

**Vocabulary violations**: Zero.

### New tools added to vocabulary

The following tools were encountered in the portfolio but were absent from the baseline vocabulary. They have been added to `TAXONOMY.md §6`:

| Tool slug | Description | First used in |
|---|---|---|
| `foursquare-api` | Foursquare Places API (restaurant/venue search) | date-proposal-website |
| `eventbrite-api` | Eventbrite API (event discovery) | date-proposal-website |
| `tmdb-api` | The Movie Database API (film metadata) | date-proposal-website |
| `icalendar` | RFC 5545 iCalendar (.ics) format | date-proposal-website |

Tools from the baseline vocabulary **not yet used** in any item: `github-actions`, `n8n`, `asana`, `har-analysis`. These remain in the vocabulary for future use.

---

## 3. Crossover Audit (Items with 2+ Domains)

Every item carrying multiple domains is listed below with a justification. Items are assessed for contamination risk.

| ID | Domains | Justification | Contamination risk? |
|---|---|---|---|
| spec-solutions-fractional-cos | support-ops, people-hr, operations | Three genuinely distinct workstreams within the role: support system build (support-ops), EOR/HR compliance/coaching (people-hr), general ops/events (operations). All demonstrated in bullet points with separate subheadings. | No |
| stamped-support-hero | customer-support, support-ops | The role involved both doing technical support (customer-support) AND improving troubleshooting processes (support-ops). Anti-rule requires both be genuine — confirmed. | No |
| connection-engine-cos | project-management, community, operations | Three explicitly separate workstreams at 30/30/10% split in the source. All demonstrated. | No |
| itc-community-manager | community, operations | Community management as primary; "Created comprehensive operational documentation" and "Formalised roles and responsibilities" crosses into operations. Justified. | No |
| can-i-play-that-editor | operations, content-creation | Executive ops support (operations) and editorial content (content-creation) both clearly demonstrated. Not contaminated. | No |
| samebug-developer-advocate | customer-support, community | Direct platform support (customer-support) and community building/advocacy (community) both present. Short role — two domains at risk of over-tagging, but both are genuinely demonstrated. | Low — monitor on re-run |
| learnovate-pm-research | project-management, research | PM on an EU research project; the "Research Assistant" title confirms research work alongside PM. Both demonstrated. | No |
| leaguepedia-chief-of-people | people-hr, operations | HR/hiring (people-hr) and operational frameworks/SOPs (operations) both clearly evidenced at scale. | No |
| stamped-widget-diagnostic | customer-support, support-ops | Case study explicitly covers doing support AND building a diagnostic process (converting a repeated issue into a 4-branch framework). Both evidenced. | No |
| spec-solutions-support-ops | support-ops, customer-support | Covers building the new support system (support-ops primary) and directly handling customer interactions (customer-support secondary). Both real. | No |
| posthog-cs-health-intelligence | support-ops, data-analysis | Built tooling for CS prioritisation (support-ops) using a data model with threshold scoring logic (data-analysis). Both genuine — the Python script is the data-analysis artefact. | No |
| posthog-csm-copilot | ai-engineering, support-ops | AI tool (ai-engineering) specifically designed for a support/CS workflow (support-ops). The prompt encoding is the support-ops work. | No |
| faq-chatbot | ai-engineering, support-ops | AI tool (ai-engineering) that deflects support tickets (support-ops — self-serve deflection is the core design goal). | No |
| lorebyspec-creator-tool | ai-engineering, content-creation | AI tool (ai-engineering) built for a content creation workflow (content-creation). The tool only exists to serve the YouTube channel. | No |
| support-triage-tool | ai-engineering, support-ops | AI tool (ai-engineering) that does triage for a support queue (support-ops). Genuine overlap. | No |
| kh-lore-checker | ai-engineering, content-creation | AI tool (ai-engineering) built for content prep for a YouTube channel (content-creation). | No |
| tiktok-sponsorship-strategy | content-creation, strategy | Sponsorship strategy (strategy — explicit commercial positioning work) for a creator (content-creation context). Justified. | No |
| business-relocation-expansion | people-hr, strategy | EOR/HR compliance navigation (people-hr) plus market entry strategy (strategy — explicit "market entry strategies" in description). | No |
| date-proposal-website | frontend-dev, research | Client-side build (frontend-dev) plus structured API landscape research (research — booking API gap, patent/regulatory equivalents). The research half is substantial and documented. | No |
| technical-writing-portfolio | technical-writing, support-ops, people-hr | Collection contains: API troubleshooting + escalation playbook (support-ops); EOR payroll explainer (people-hr); all four written as technical writing samples (technical-writing). Three domains, each demonstrated in separate sub-documents. | No |
| saas-integration-diagnostic-guide | technical-writing, support-ops | A technical writing sample (technical-writing) specifically about support enablement/triage (support-ops). Both genuine. | No |

**Contamination findings**: None. All multi-domain items reflect genuine overlap from distinct workstreams or deliverable types.

---

## 4. Flagged for Human Decision

### 4a. `security` domain — not applied

The portfolio header and skills section explicitly position cybersecurity as a current focus ("Consultant · Project Manager · HR & Compliance · Cybersecurity"; "Cybersecurity — In Training" skills block). However, **no content item demonstrates substantive security work** — no case study, project, or role where security was a primary deliverable. The certifications listed (Google Cybersecurity Certificate courses) are in-progress qualifications.

**Recommendation**: Do not apply the `security` domain to any existing item. When a project or role exists that demonstrates actual security work, add `security` at that time and simultaneously add to this flagged list per the anti-rule. The "in training" positioning is accurately represented in skills/certifications metadata but should not contaminate domain tags on work items.

### 4b. `implementation-onboarding` domain — not applied

The portfolio contains EOR/expansion work and some onboarding mentions, but no item shows the primary activity of **configuring or rolling out a product/system for customers**. The closest candidate is `spec-solutions-fractional-cos` (Joocie Tech Support & QA consulting), but the description is too thin to confirm implementation-onboarding as a demonstrated domain rather than a mentioned one.

**Recommendation**: Hold. If the portfolio is expanded with content from the Joocie engagement, revisit at that time.

### 4c. Type classification — consulting deliverables in Projects tab

Five items in the Projects tab (`tiktok-sponsorship-strategy`, `business-relocation-expansion`, `leadership-coaching-project`, `optimising-cs-operations`, `niche-market-web-dev-strategy`) are consulting engagements or deliverables rather than built artifacts. They are typed as `project` because they produced a tangible deliverable and are presented in the Projects tab.

**Recommendation**: These could alternatively be typed as `case-study` (they describe problems solved). If the future chat overlay should treat them differently from tools and prototypes, retype them as `case-study`. If they should appear alongside the built tools, keep as `project`. This decision affects lane membership — `case-study` items would share visibility patterns with the three narrative case studies.

### 4d. Proposed lane: `documentation`

A `documentation` / `technical-writing` lane is coherent given the volume of writing samples: 5 document items plus `technical-writing` as a secondary domain on support-ops items. Currently proposed in `lanes.json` as `_proposed_documentation`.

**Recommendation**: Finalise this lane. It targets a clearly distinct visitor type (hiring for technical writing/docs). No overlap risk with `cs-support` — the technical writing samples are writing-skills evidence, not support-ops evidence.

### 4e. Proposed lane: `people-hr`

Only 4 items carry the `people-hr` domain (`spec-solutions-fractional-cos`, `leaguepedia-chief-of-people`, `business-relocation-expansion`, `leadership-coaching-project`). The lane is semantically coherent but thin.

**Recommendation**: Hold off finalising. Consider whether to surface a `people-hr` lane at all, or whether people-ops visitors are better served by the `ops-strategy` lane (which includes `people-hr` in its include set). A dedicated lane makes sense if the chat overlay is likely to see "HR" or "people ops" as a distinct visitor intent.

### 4f. Content gap — Joocie (Tech Support & QA Consulting)

`spec-solutions-fractional-cos` mentions "Tech Support & QA Consultant for Joocie (via Consultancy) — Remote since Jan 2024" as a sub-engagement, but there is no case study or project entry for this work.

**Recommendation**: If the Joocie engagement produced meaningful work (bug investigations, documentation, process changes), consider adding a case study. It would be the clearest candidate for the `implementation-onboarding` domain.

### 4g. Content gap — LoreBySpec YouTube channel

The portfolio mentions LoreBySpec as an active YouTube channel and two projects reference it (`kh-lore-checker`, `lorebyspec-creator-tool`), but the channel itself is not indexed as a `work` item.

**Recommendation**: Add a `work` item for LoreBySpec if it is an ongoing personal project worth surfacing to hiring managers in the `creator-lore` lane. Type would be `work`, context `personal-project`/`personal`.

### 4h. Content gap — Phandroid/Android Central/Mobile Nations journalism output

The `phandroid-tech-writer` work item covers the role, but individual long-form articles or significant editorial pieces are not linked or indexed.

**Recommendation**: If specific articles represent strong technical writing or content strategy samples, consider adding them as `document` items. Not blocking — the role item covers the work adequately for most lane queries.

### 4i. `date-proposal-website` — `research` domain justification note

The `research` domain on this item may surprise a reader. Justification: the project contains documented, structured research into the restaurant booking API landscape (OpenTable, Resy, Tock, Apify), patent and regulatory analysis, and cinema showtime API coverage — all with documented findings in the README and devlog. This crosses the threshold from "I googled it" to "structured research with documented findings."

**If this feels like over-tagging**: Remove `research` and leave `frontend-dev` only. The item still appears in `builder-technical` and its research value is captured in the `diagnostic-reasoning` and `build-in-public` evidence tags.

---

## 5. Stats

### By type

| Type | Count |
|---|---|
| `work` | 13 |
| `case-study` | 3 |
| `project` | 15 |
| `document` | 5 |
| **Total** | **36** |

### By domain (items per domain; total > 36 due to multi-domain items)

| Domain | Item count |
|---|---|
| `support-ops` | 10 |
| `ai-engineering` | 8 |
| `customer-support` | 6 |
| `technical-writing` | 5 |
| `people-hr` | 4 |
| `community` | 4 |
| `content-creation` | 4 |
| `frontend-dev` | 3 |
| `operations` | 3 |
| `strategy` | 3 |
| `project-management` | 3 |
| `research` | 2 |
| `data-analysis` | 2 |
| `security` | 0 |
| `implementation-onboarding` | 0 |

### By lane (items that would appear in each lane's include query)

| Lane | Matching items | Notes |
|---|---|---|
| `cs-support` | 10 | All items with `customer-support` or `support-ops` |
| `implementation` | 10 | All items with `implementation-onboarding` (0) or `support-ops` (10) — effectively the support-ops set |
| `ops-strategy` | 13 | Items with `operations`, `strategy`, `project-management`, or `people-hr` |
| `builder-technical` | 11 | Items with `ai-engineering` or `frontend-dev` |
| `creator-lore` | 4 | Items with `content-creation` |
| `documentation` _(proposed)_ | 5 | Items with `technical-writing` |
| `people-hr` _(proposed)_ | 4 | Items with `people-hr` |

**Note on `implementation` lane**: Currently returns only `support-ops` items because `implementation-onboarding` is not applied to any item. If this lane is to be meaningful as distinct from `cs-support`, it needs either (a) content with genuine `implementation-onboarding` work, or (b) a revised include query. Flagged in §4b above.

---

## 6. Validation Summary

| Check | Result |
|---|---|
| All items have required facets | ✅ Zero orphans |
| All tags within controlled vocabulary | ✅ Zero violations |
| All `security`-tagged items flagged | ✅ No `security` tags applied |
| New tools documented in TAXONOMY.md | ✅ 4 new tools added |
| No audience labels on items | ✅ Confirmed |
| `lensByAudience` left empty | ✅ Confirmed |
| Stable HTML IDs added | ✅ See index.html edits |

**Status: PASS.** Zero orphans, zero vocabulary violations.
