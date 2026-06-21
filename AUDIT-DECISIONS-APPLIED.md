# Audit Decisions Applied

This file records the targeted metadata edits applied per the four approved decisions. No visual or copy changes were made. No ids, lensByAudience, audiencePin, or audienceExclude values were altered.

---

## Decision 1 — Five consulting deliverables retyped from `project` to `case-study`

**Rationale:** In this portfolio, `project` means a built, clickable artifact. These five items are narrative consulting outputs — they produced deliverables but not running artifacts. `case-study` is the correct type.

**Items changed** (all facet tags, dates, anchors, and relatedIds preserved):

| id | Previous type | New type | status change |
|---|---|---|---|
| `tiktok-sponsorship-strategy` | `project` | `case-study` | `"complete"` → `null` |
| `business-relocation-expansion` | `project` | `case-study` | `"complete"` → `null` |
| `leadership-coaching-project` | `project` | `case-study` | `"complete"` → `null` |
| `optimising-cs-operations` | `project` | `case-study` | `"complete"` → `null` |
| `niche-market-web-dev-strategy` | `project` | `case-study` | `"complete"` → `null` |

`status` is set to `null` because the schema requires `null` for `work` and `case-study` type items (TAXONOMY.md §7).

**Facet validation post-retype:**

| id | domains | evidence | context | dates |
|---|---|---|---|---|
| `tiktok-sponsorship-strategy` | `content-creation`, `strategy` | `cross-functional-influence` | startup/lead/consulting | 2025-01 / 2025-01 ✓ |
| `business-relocation-expansion` | `people-hr`, `strategy` | `cross-functional-influence`, `process-design` | agency-consulting/lead/consulting | 2024-12 / 2024-12 ✓ |
| `leadership-coaching-project` | `people-hr` | `cross-functional-influence` | agency-consulting/strategic/consulting | 2024-11 / 2024-12 ✓ |
| `optimising-cs-operations` | `support-ops` | `process-design`, `self-serve-deflection`, `cost-discipline` | agency-consulting/lead/consulting | 2024-06 / 2024-09 ✓ |
| `niche-market-web-dev-strategy` | `strategy` | `diagnostic-reasoning`, `cross-functional-influence` | agency-consulting/lead/consulting | 2023-01 / 2023-02 ✓ |

Zero facet tags dropped. Zero ids changed.

---

## Decision 2 — Standalone `people-hr` lane removed; domain absorbed by `ops-strategy`

**What changed in `lanes.json`:**
- Removed `_proposed_people_hr` lane definition entirely.
- Confirmed `ops-strategy` already includes `"people-hr"` in its `include.domains` array — no change required there.
- Added `"tier": "primary"` to all five primary lanes for explicit tier marking.

**What did not change:**
- The `people-hr` domain tag on any item. All four items carrying `people-hr` continue to do so.
- The `ops-strategy` lane's existing `include`, `boost`, `sort`, and `maxItems` values.

---

## Decision 3 — `documentation` lane finalised as secondary + cross-cutting

**What changed in `lanes.json`:**
- Renamed from `_proposed_documentation` to `documentation` (removing the proposed prefix).
- Removed the `_status` and `_note` fields.
- Added `"tier": "secondary"`.
- Added `"crossCutting": true` with a `_crossCuttingNote` explaining the intent: every primary hiring lane should additionally surface this lane's top 1–2 `technical-writing` items as supporting evidence, without those items leaving their home lane.

**What did not change:**
- No content retagged. Lane config change only.
- The `include`, `boost`, `sort`, and `maxItems` values are identical to the proposed version.

---

## Decision 4 — Security/tagline: reported, not edited

**Finding:**

> **File:** `index.html`, **line 14**
> **Exact text:** `<p>Consultant · Project Manager · HR &amp; Compliance · Cybersecurity</p>`

**Flag:** The `Cybersecurity` claim in the header tagline is not backed by any item in `portfolio-index.json` carrying the `security` domain. Per the tagging audit (§4a), no content demonstrates substantive security work — only in-training certifications and skills listed under a "Cybersecurity — In Training" label. This is an unbacked claim. **Human decision required:** cut `· Cybersecurity` from the tagline, or back it with a security artifact that earns the `security` domain tag.

No edit was made to `index.html`.

---

## Validation summary

| Check | Result |
|---|---|
| Zero ids changed | ✓ |
| Zero facet tags dropped on retyped items | ✓ |
| `implementation` lane untouched | ✓ |
| `people-hr` domain on all items preserved | ✓ |
| `ops-strategy` absorbs `people-hr` domain | ✓ (was already present) |
| `documentation` lane active (no `_proposed_` prefix) | ✓ |
| Tagline reported, not edited | ✓ |
| No visual/copy changes | ✓ |
| No `lensByAudience`, `audiencePin`, `audienceExclude` overwritten | ✓ |
