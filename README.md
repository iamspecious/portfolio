# Specious Coda-Bishop — Portfolio

**Live site:** [iamspecious.github.io/portfolio](https://iamspecious.github.io/portfolio)

Operations professional with over a decade across people operations, strategic HR, community management, and technical support — drawn to the places where things aren't quite working and the structural reason why. Also genuinely technically curious: working knowledge of network analysis, log review, and vulnerability scanning sits alongside the operations background. Tech writer and YouTube creator ([LoreBySpec](https://www.youtube.com/@lorebyspec)).

---

## Projects

The live site organises projects by category (AI Tools, Writing & Docs, Research, Consulting) with filter buttons in the Projects tab.

### AI Tools

| Project | What it does | Status |
|---|---|---|
| [Error Log Interpreter](https://iamspecious.github.io/portfolio/error-interpreter.html) | Paste a browser console error, build failure, or stack trace — get a plain-English breakdown that separates where the error surfaces from where it actually originated, with concrete steps and error-handling coaching | Live |
| [Debug Helper](https://iamspecious.github.io/portfolio/debug-helper.html) | Structured debugging coach for three modes: you have an error, code runs but does the wrong thing, or total silence — specifically addresses hidden failure cases like swallowed catch blocks and missing await | Live |
| [LoreBySpec Creator Tool](https://iamspecious.github.io/portfolio/creator-tool.html) | Two-mode content assistant for the YouTube channel: Video Ideas (paste a topic, get five titled angles with hooks) and Comment Reply (paste a viewer comment, get a drafted reply in a lore-nerd voice) | Live |
| [PostHog CSM Copilot](https://iamspecious.github.io/portfolio/posthog-cs-copilot.html) | Customer Success copilot for managing a 25–40 account portfolio: signal triage, response drafting, escalation strategy, and health assessment — encoded with PostHog's product suite, billing model, and customer type dynamics | In Progress |
| [PostHog CS Health Intelligence](./posthog-cs-health-intelligence/) | Research-backed prototype for the CS prioritisation gap: a structured account model and Python script that produces a ranked morning action list — signals individually surfaced with plain-English reasons and suggested actions, thresholds differentiated by customer type | Complete |
| [FAQ / Knowledge Base Chatbot](https://iamspecious.github.io/portfolio/faq-chatbot.html) | Paste docs, ask a question, get a grounded answer — or "not in our docs" when it's not there. No hallucination, no backend | Live |
| [Support Ticket Triage Tool](https://iamspecious.github.io/portfolio/support-triage.html) | Paste a customer message or error log, get a category, colour-coded urgency level, and a ready-to-send draft reply | Live |
| [KH Lore Consistency Checker](https://iamspecious.github.io/portfolio/lore-checker.html) | AI theory stress-tester for Kingdom Hearts canon — paste a theory, supply wiki links, get structured contradictions, weaknesses, and a verdict | In Progress |
| [Date Proposal Website](https://iamspecious.github.io/portfolio/date-proposal/) | Recreation and technical deconstruction of a viral date-proposal website — running No button, progressive preference questions, live restaurant/event/cinema discovery via three APIs, and a downloadable calendar invite | In Progress |

### Writing & Docs

Portfolio samples demonstrating technical writing across different audiences, domains, and registers.

| Project | What it does | Status |
|---|---|---|
| [Technical Writing Portfolio](https://iamspecious.github.io/portfolio/technical-writing-portfolio.html) | Four reference-quality playbooks across ops and HR systems: API troubleshooting (Zendesk→Slack), SQL missing data audit, EOR payroll explainer for non-technical stakeholders, and tiered support escalation logic | Complete |
| [SaaS Integration Failure Diagnostic Guide](https://iamspecious.github.io/portfolio/support-guide.html) | Support enablement document for Tier 1/2 agents covering webhook delivery failures, API authentication breakdowns, and HRIS sync errors — structured to reduce unnecessary escalations | Complete |
| [Cat API Documentation](https://iamspecious.github.io/portfolio/cat-api-documentation.html) | Professional API reference documentation covering authentication, parameters, response schema, error states, and pagination — structured to Stripe/Twilio standards | Complete |
| [Voice & Tone Guide](https://iamspecious.github.io/portfolio/voice-and-tone-guide.html) | Internal contributor guide defining voice, tone, and writing standards for technical documentation teams — principled definitions, tone-by-context frameworks, and a contributor checklist | Complete |
| [Voice Adaptation Showcase](https://iamspecious.github.io/portfolio/voice-adaptation-showcase) | The same how-to content written three times — calibrated to Apple, Mailchimp, and PostHog's documented voice principles — with reflections on what required the most deliberate adjustment in each | Complete |

### Research

| Project | What it does | Status |
|---|---|---|
| [PregVoice](https://iamspecious.github.io/portfolio/pregvoice.html) | Accessibility project: independent pregnancy test result reading for blind and visually impaired users via on-device ML, audio, and haptics | Research & Planning |

### Consulting

Five consulting engagements covering sponsorship strategy, business relocation, leadership coaching, support ops optimisation, and niche market development — visible in the Projects tab on the live site.

---

## Dev Logs

Every AI tool and engineering project has a running dev log embedded directly in the portfolio — real build notes recording decisions, dead ends, pivots, and constraints as they happened. Not a polished write-up after the fact: the log is the artefact.

**See the dev logs on the live site** → [iamspecious.github.io/portfolio](https://iamspecious.github.io/portfolio) (Projects tab)

---

## Stack

All interactive tools are client-side only. No backend, no database, no server, no hosting cost.

- **Languages:** HTML, CSS, JavaScript
- **AI:** Claude API (Anthropic) — Haiku 4.5 default, model-selectable in UI
- **External APIs:** Foursquare (venues), Eventbrite (events), TMDB (films)
- **CORS workaround:** Jina Reader (`r.jina.ai`) for client-side URL fetching
- **Hosting:** GitHub Pages (free, static)

The consistent no-backend architecture across all tools is intentional: same delivery mechanism, different problems solved.

---

## Background

**Writing:** Tech articles for Phandroid, Android Central, and Mobile Nations — reviews, guides, and feature coverage on consumer electronics and games.

**Consulting:** HR, operations, and business development. Employer of Record (EOR) solutions, market analysis, leadership coaching, support ops optimisation.

**Earlier:** Project Manager on a €3M EU-funded research project (Learnovate), Chief of People at Leaguepedia, Community Manager at Irish Tech Community.

**Contact:** work.specious@gmail.com
