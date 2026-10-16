# Portfolio audit runbook

A recurring audit checks three things: everything **works** (functional), every item can be **found** through Digital Spec, Portfolio Search and the Projects tab (findable), and every item is described, tagged and routed accurately (fitting). Each run leaves a dated report in this folder.

## Before you start

- Read the previous report in this folder and its "Open decisions" list. Don't re-raise a decision that was made; check whether it was applied.
- Read `TAXONOMY.md`. It is the authority for every tag, and new tags are proposed there before use.

## 1. Automated checks

From the repo root:

```sh
python3 tools/audit.py                     # structure, tags, lanes, lexicon, links, README
python3 -m http.server 8765 &              # serve the site
node tools/smoke-test.js                   # drive the real page in headless Chromium
```

`audit.py` exits 1 on any FAIL. Warnings are judgment calls: carry each one into the report as a finding, a known exception, or a decision for the owner. `smoke-test.js` needs Playwright. If the Bootstrap CDN is unreachable, point `BOOTSTRAP_JS` / `BOOTSTRAP_CSS` at local copies (`npm pack bootstrap@<version>`).

What they cover:

| Area | Check | Tool |
|---|---|---|
| Index | Required fields, controlled vocabulary, status/date rules, anti-rules, override rationale, related ids | audit.py §1 |
| Anchors | Every index item resolves on the page; every page block is indexed; section sub-anchors exist | audit.py §2 |
| Projects tab | `data-date` and `data-category` on every block; every filter button matches something | audit.py §3, smoke-test |
| Digital Spec | Every node, lane, deep link and `find-project` id resolves; which items each lane shows and hides; items in no lane | audit.py §4–5 |
| Digital Spec, live | Every lane reachable by clicking; every card lands on a visible target | smoke-test |
| Search | Every item found by its own title and the click lands; expected words per item (`tools/search-lexicon.json`) | audit.py §6, smoke-test |
| Links | Local links, images and scripts resolve; external links with `--external` | audit.py §7 |
| README | Every Projects-tab item has a README row and vice versa | audit.py §8 |
| Phone width | No sideways scroll at 375px | smoke-test |

## 2. Manual review, per project and document

For each item, record what it has and what it lacks:

- **Card:** status badge matches the index `status`; date line matches `dateStart`/`dateEnd`; a Constraints section (the About tab promises one on every project); a dev log for built projects; a link to the live tool, repo or document, or a badge saying it's private.
- **Index entry:** domains and evidence earned by the card's content, not just mentioned (TAXONOMY §3–4); tools actually used; summary in present tense and accurate.
- **Digital Spec:** which lanes it shows in. If none, is that deliberate and written in `notes`?
- **Search lexicon:** the words a recruiter, peer or hiring manager would type. Add them to `tools/search-lexicon.json`. When a word misses, decide between the summary, a synonym in `portfolio-search.js`, or dropping the expectation.
- **README:** the row matches the card.

## 3. Wider checks

- Accessibility: run axe-core against each tab with Digital Spec open and closed; check keyboard use of the overlay and search.
- Standalone pages: title, back link, no broken local links.
- Stale docs: older audit files that no longer describe the code get a banner pointing to the current report.

## 4. Report and fixes

Write `audits/YYYY-MM-DD.md` covering what was checked, findings by severity, what was fixed, per-item notes, and **open decisions** (anything that changes tags, lanes, copy or design is the owner's call). Fix clear bugs on a branch. Add a dev log entry on the affected card when a fix changes how something behaves.
