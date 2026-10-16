# Specious Coda-Bishop — Portfolio

**Live site:** [iamspecious.github.io/portfolio](https://iamspecious.github.io/portfolio)

Operations professional with over a decade across people operations, strategic HR, community management, and technical support — drawn to the places where things aren't quite working and the structural reason why. Also genuinely technically curious: working knowledge of network analysis, log review, and vulnerability scanning sits alongside the operations background. Tech writer and YouTube creator ([LoreBySpec](https://www.youtube.com/@lorebyspec)).

---

## Projects

The live site organises projects by category (AI Tools, Engineering, Hardware, Research, Writing & Docs, Operations, Strategy, Consulting) with filter buttons in the Projects tab; a project can sit in more than one. Projects are listed newest first, with a toggle to flip to oldest first. Sorting uses each project's start date, never its latest dev log entry: every `project-block` in `index.html` carries a `data-date="YYYY-MM-DD"` for when the project began, and the page sorts by it (a block without one counts as newest). Give every new project a `data-date`, and don't change it when the project gets new work.

### AI Tools & Engineering

| Project | What it does | Status |
|---|---|---|
| [Digital Spec — Portfolio Front Door](https://iamspecious.github.io/portfolio) | Branching, visual-novel-style visitor guide built as an overlay on the static portfolio — routes visitors by what brought them (hiring, curious, browsing) and curates content via a tagged portfolio index. No AI: every path is pre-programmed. Collapses to a docked tab, never traps anyone | Live |
| [Portfolio Search](https://iamspecious.github.io/portfolio) | Header search bar, on every tab — type a tool ("PostHog"), a discipline ("writing," "HR"), or a project name and jump straight to every matching work role, case study, project, and document. Queries the same tagged portfolio index Digital Spec routes through. No backend, no AI, no fuzzy matching | Live |
| [Error Log Interpreter](https://iamspecious.github.io/portfolio/error-interpreter.html) | Paste a browser console error, build failure, or stack trace — get a plain-English breakdown that separates where the error surfaces from where it actually originated, with concrete steps and error-handling coaching | Live |
| [Debug Helper](https://iamspecious.github.io/portfolio/debug-helper.html) | Structured debugging coach for three modes: you have an error, code runs but does the wrong thing, or total silence — specifically addresses hidden failure cases like swallowed catch blocks and missing await | Live |
| [LoreBySpec Creator Tool](https://iamspecious.github.io/portfolio/creator-tool.html) | Two-mode content assistant for the YouTube channel: Video Ideas (paste a topic, get five titled angles with hooks) and Comment Reply (paste a viewer comment, get a drafted reply in a lore-nerd voice) | Live |
| [PostHog CSM Copilot](https://iamspecious.github.io/portfolio/posthog-cs-copilot.html) | Customer Success copilot for managing a 25–40 account portfolio: signal triage, response drafting, escalation strategy, and health assessment — encoded with PostHog's product suite, billing model, and customer type dynamics | In Progress |
| [PostHog CS Health Intelligence](./posthog-cs-health-intelligence/) | Research-backed prototype for the CS prioritisation gap: a structured account model and Python script that produces a ranked morning action list — signals individually surfaced with plain-English reasons and suggested actions, thresholds differentiated by customer type | Complete |
| [FAQ Chatbot](https://iamspecious.github.io/portfolio/faq-chatbot.html) | Paste docs, ask a question, get a grounded answer — or "not in our docs" when it's not there. No hallucination, no backend | Live |
| [Support Ticket Triage Tool](https://iamspecious.github.io/portfolio/support-triage.html) | Paste a customer message or error log, get a category, colour-coded urgency level, and a ready-to-send draft reply | Live |
| [KH Lore Consistency Checker](https://iamspecious.github.io/portfolio/lore-checker.html) | AI theory stress-tester for Kingdom Hearts canon — paste a theory, supply wiki links, get structured contradictions, weaknesses, and a verdict | In Progress |
| [Date Proposal Website](https://iamspecious.github.io/portfolio/date-proposal/) | Recreation and technical deconstruction of a viral date-proposal website — running No button, progressive preference questions, live restaurant/event/cinema discovery via three APIs, and a downloadable calendar invite | In Progress |
| Role Fit Watcher | Scheduled morning agent that pulls ~24 companies' public ATS feeds (Ashby, Greenhouse, Workable, Teamtailor), filters every posting on company/role/location gates, judges the survivors against a written fit matrix, dedups against a state file, and posts a reasoned digest of only the new, remote-from-Germany roles worth acting on. No scraping, no backend | Live (private) |
| Role-Fit Evaluator | Decision matrix for whether a role is worth the hours of curating a CV: scores a job description against a fixed profile across seven weighted dimensions behind a dealbreaker gate, and returns a verdict (Strong / Stretch / Weak / No-go) with the bridges to lead with and the real gaps. A five-tab spreadsheet engine plus a runbook | Internal tool |
| KH Description Optimizer | Rewrites old LoreBySpec video descriptions for YouTube search in one pass: a rewritten description, 3–5 lore-aware hashtags, and backend tags trimmed to YouTube's 500-character limit, with a built-in Kingdom Hearts lore dictionary. Runs as a Cowork artifact | Live (private) |
| YouTube A/B Testing Tool | Paste a video script, get three title and thumbnail variants built on different levers (Curiosity, Bold Claim, List/Authority), with thumbnail concept briefs and an over-promise flag. Runs as a Cowork artifact | Live (private) |
| KH Title & Thumbnail Audit | Visual audit of all 69 LoreBySpec videos against a 22-point rubric, turned into a redo list ranked by weakness × views, plus finished reference thumbnails for the priority videos | Complete |
| [HR Webhook Integration Layer](./hr-webhook-integration-layer/) | Webhook receiver and integration layer across HiBob, Ashby and Remote, built around the fact that the three platforms disagree about what a failed delivery means. Python (standard library), SQLite, and n8n in Docker; real calls against the Remote sandbox, documented-payload simulators for HiBob and Ashby | Complete |
| [SQL 90: learning Postgres in public](https://github.com/iamspecious/sql-90) | 90-day SQL challenge (Oct 2026 to Jan 2027) going from foundational SQL to complex Postgres queries for Support Engineer roles. Every query is my own, wrong attempts stay as written, with a weekly devlog, a mistake log, and a day-0 baseline | In Progress |
| [Tarot Machine](./tarot-machine/) | First hardware build: a pocket tarot-draw gadget on an M5StickS3 (ESP32-S3), inspired by Finbarre Snarey's TAROTRON 2000. Press a button and it draws a random card from my own 78 meanings, shows 1-bit card art tinted by suit, and flips to the meaning with tap/hold controls on one button. Sound and voice are next | In Progress |

### Writing & Docs

Portfolio samples demonstrating technical writing across different audiences, domains, and registers.

| Project | What it does | Status |
|---|---|---|
| [Technical Writing Portfolio](https://iamspecious.github.io/portfolio/technical-writing-portfolio.html) | Four reference-quality playbooks across ops and HR systems: API troubleshooting (Zendesk→Slack), SQL missing data audit, EOR payroll explainer for non-technical stakeholders, and tiered support escalation logic | Complete |
| [SaaS Integration Failure Diagnostic Guide](https://iamspecious.github.io/portfolio/support-guide.html) | Support enablement document for Tier 1/2 agents covering webhook delivery failures, API authentication breakdowns, and HRIS sync errors — structured to reduce unnecessary escalations | Complete |
| [Cat API Documentation](https://iamspecious.github.io/portfolio/cat-api-documentation.html) | Professional API reference documentation covering authentication, parameters, response schema, error states, and pagination — structured to Stripe/Twilio standards | Complete |
| [Voice & Tone Guide](https://iamspecious.github.io/portfolio/voice-and-tone-guide.html) | Internal contributor guide defining voice, tone, and writing standards for technical documentation teams — principled definitions, tone-by-context frameworks, and a contributor checklist | Complete |
| [Voice Adaptation Showcase](https://iamspecious.github.io/portfolio/voice-adaptation-showcase) | The same how-to content written three times — calibrated to Apple, Mailchimp, and PostHog's documented voice principles — with reflections on what required the most deliberate adjustment in each | Complete |
| [PostHog First-Run Audit](https://iamspecious.github.io/portfolio/posthog-first-run-audit.html) | Field report from installing PostHog cold on this site as a genuine first-time user: seven findings documented live (a wizard with no exit, an ambiguous SDK label, an OAuth redirect with no success state), four GitHub issues and a docs PR filed | Complete |
| [The Small Studio Crisis Playbook](https://iamspecious.github.io/portfolio/crisis-management-playbook.html) | Openly licensed (CC BY 4.0) crisis communications and moderation kit for studios, open-source projects, and community teams — a six-class incident taxonomy, a five-role command structure, eight response templates, and a standalone printable [one-page quick reference](https://iamspecious.github.io/portfolio/crisis-response-one-page.html). Every structural choice traced to a cited source (CDC CERC, Coombs' SCCT, NIST SP 800-61r3, aviation checklist human-factors research) | Complete |

### Research

| Project | What it does | Status |
|---|---|---|
| [PregVoice](https://iamspecious.github.io/portfolio/pregvoice.html) | Accessibility project: independent pregnancy test result reading for blind and visually impaired users via on-device ML, audio, and haptics | Research & Planning |

### Case Studies

Four narrative case studies in their own tab — each one shows the actual diagnostic thinking behind a real engagement, not just the outcome.

| Case Study | Context |
|---|---|
| Diagnosing a Widget That Failed Four Different Ways | Stamped.io · Technical Support · 2020 |
| Turning a Gmail Inbox Into an Actual Support System | Spec Solutions · Customer Support Operations |
| Keeping a €3M Project Aligned Across Borders, Without Authority | Learnovate Centre, Trinity College Dublin · Project Management · 2016–2017 |
| Rebuilding a Denim Brand, Top to Tail | Customer Experience & Operations · client anonymised |

### Consulting

Five consulting engagements covering sponsorship strategy, business relocation, leadership coaching, support ops optimisation, and niche market development — visible in the Projects tab on the live site.

---

## Dev Logs

Every AI tool and engineering project has a running dev log embedded directly in the portfolio: build notes recording decisions, dead ends, pivots, and constraints as they happened. The log is the artefact. Projects with their own folder (`date-proposal/`, `hr-webhook-integration-layer/`, `posthog-cs-health-intelligence/`, `tarot-machine/`) also keep a `DEVLOG.md` and `README.md` there.

**See the dev logs on the live site** → [iamspecious.github.io/portfolio](https://iamspecious.github.io/portfolio) (Projects tab)

---

## Stack

The site and its browser tools are static and client-side: no backend of my own, no database, no hosting cost.

- **Languages:** HTML, CSS, JavaScript; Python for the prototypes and the webhook layer; C++ (Arduino) for the Tarot Machine
- **AI:** Claude API (Anthropic): Haiku 4.5 by default, Sonnet 4.6 selectable in the UI
- **Claude calls from the browser:** a small Cloudflare Worker ([`proxy/worker.js`](./proxy/worker.js)) that only adds CORS headers; visitors supply their own API key
- **External APIs:** Foursquare (venues), Eventbrite (events), TMDB (films)
- **URL fetching:** Jina Reader (`r.jina.ai`) for client-side page fetching
- **Analytics:** PostHog on the portfolio page
- **Hosting:** GitHub Pages (free, static)

The exceptions run outside the browser on purpose: the HR Webhook Integration Layer (Python, SQLite, n8n in Docker, run locally), the PostHog CS Health Intelligence prototype (a Python script), Role Fit Watcher (a scheduled agent), and the Tarot Machine (firmware on an ESP32-S3).

---

## How the site fits together

- **`index.html`** holds every tab: About, Work Experience, Case Studies, Projects, Working with Spec. Projects-tab blocks carry `data-date` (start date, for sorting) and `data-category` (filter buttons).
- **`portfolio-index.json`** is the tagged index of every work role, case study, project and document. Both Digital Spec and Portfolio Search read it. Tags come only from the controlled vocabulary in [`TAXONOMY.md`](./TAXONOMY.md).
- **`lanes.json`** defines Digital Spec's audience lanes as queries over those tags; **`front-door-config.json`** holds the dialogue that leads to them.
- **`portfolio-search.js`** searches titles, tags and summaries in the same index, plus a short synonym list.

Adding a project means: a block in `index.html` with an `id`, `data-date` and `data-category`; an entry in `portfolio-index.json` following the checklist in `TAXONOMY.md` §12; a row in this README; and expected search words in `tools/search-lexicon.json`.

## Auditing

[`audits/`](./audits/) has the audit runbook and dated reports. Two checks run from the repo root:

- `python3 tools/audit.py` checks the index against the taxonomy and the page, the Digital Spec config and lanes, the search lexicon, local links, and this README.
- `node tools/smoke-test.js` drives the page in a headless browser: every Digital Spec lane and card, a search for every item, and every filter. Serve the repo first with `python3 -m http.server 8765`.

---

## Background

**Writing:** Tech articles for Phandroid, Android Central, and Mobile Nations — reviews, guides, and feature coverage on consumer electronics and games.

**Consulting:** HR, operations, and business development. Employer of Record (EOR) solutions, market analysis, leadership coaching, support ops optimisation.

**Earlier:** Project Manager on a €3M EU-funded research project (Learnovate), Chief of People at Leaguepedia, Community Manager at Irish Tech Community.

**Contact:** work.specious@gmail.com
