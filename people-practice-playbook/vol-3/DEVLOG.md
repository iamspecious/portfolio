# People Practice Playbook, Vol. 3: Dev log

### 2026-11-11: Groundwork

- Started from a conversation in a People Ops community about an organisation wanting to vibe code its whole HRIS instead of paying for one. The guide is written for anyone in that position, not for one person or one community, and names none.
- Outline set: the four ways people use AI, the sandcastle analogy, tokens, the all-in cost of building, why an HR system is a hard first build, prompting, guardrails for people who build anyway, a decision table and a glossary.
- Decision: tokens are the way in, but the argument widens to total cost of ownership. On flat-rate seats the token bill alone can look small, so leaning only on it would be easy to dismiss.

### 2026-11-12: Research and first draft

- Researched current Claude pricing and plan limits, Veracode's AI code security research, IBM's breach costs, and the definitions of vibe coding from Fowler and Willison. Drafted every section.
- Every cost is labelled as an example, with links to live pricing.
- Added a planning exercise for one module (leave requests) to show the hidden decisions under a "simple" feature without scaring people off trying.
- Second research pass: what Anthropic, OpenAI and Google recommend, GitHub Spec Kit, METR's 2025 trial and its 2026 follow-up, the Thoughtworks VibeSec case, and ethics (fairness, privacy by design, accessibility).
- Correction during research: the METR follow-up changed the story. The guide no longer implies AI makes people slower; it says how fast AI feels is a poor guide to how fast it is.

### 2026-11-12: Restructure into the series

- Rebuilt as People Practice Playbook, Vol. 3, following Vol. 1's conventions: version and date at the top, CC BY-SA 4.0 at top and bottom, numbered sections with "last reviewed" dates, "Who this is for, and what it isn't" first with a "This will change" list, sources and changelog last. No review cadence promised.
- Legal detail cut back to principles plus a "check locally" pointer, in line with the series.
- Added a disclosure that the volume was researched and drafted with AI, which is also why pricing examples use Claude.

### 2026-11-12: Integrity audit and v0.1.1

- Independent audit by a separate agent that saw only the playbook: PASS WITH FIXES. 78 claims; none fabricated; 4 major and 14 minor findings.
- Fixes: section 7 rewritten to practice only; Thoughtworks example corrected to match the source; CV sorting replaced with expense receipts as the low-stakes example (it contradicted the fairness section); buy-vs-build table softened and breach row corrected; smaller wording fixes.
- Corrections route: pull request on github.com/iamspecious/portfolio or email to work.specious@gmail.com.
- v0.1 was never published, so only v0.1.1 goes live. The changelog records both.
