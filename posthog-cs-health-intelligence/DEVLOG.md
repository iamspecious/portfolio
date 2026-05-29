# DEVLOG — PostHog CS Health Intelligence Project

> This devlog is written as decisions happen, not reconstructed after the fact.
> That's intentional. A CSM who documents their thinking in real time is more
> useful to a team than one who tidies it up at the end.

---

## Entry 001 — Reading the brief properly

**Date:** May 2026  
**Status:** Research & scoping

The job brief is deceptively simple. On first read it looks like a relationship management role with some technical flavour. On closer read, there are two distinct problems hiding inside it:

**Problem 1: The signal problem.**  
25–40 customers, $20k–$100k+ ARR, spread across Slack, support tickets, email, usage data, and Stripe. The explicit success condition in the brief is: *"Your aim is to never be surprised when a customer tells us they are leaving."* That's a leading-indicator problem. You can't solve it by being responsive — you solve it by seeing things before they become conversations.

**Problem 2: The relationship problem.**  
PostHog's ICP is developers and technical teams. They self-serve aggressively, they don't want hand-holding, and they communicate on Slack rather than email. The brief mentions two customer types explicitly: sales-assisted (known to the team) and self-serve (never talked to anyone at PostHog). These two groups need fundamentally different engagement models. Treating them the same is the most common CSM mistake at a PLG company.

The brief also contains an explicit invitation: *"If you want to build automations to help you, go for it."* That's not a nice-to-have. At PostHog, where engineers build their own tooling and the culture values autonomy heavily, that line is a signal about what kind of person they're hiring. They want someone who sees gaps and fills them, not someone who waits for a playbook.

**First decision logged:** This project will be built from the perspective of a CSM designing the automation layer they'd actually want — not a theoretical exercise, not a Vitally clone.

---

## Entry 002 — Understanding the existing stack

**Date:** May 2026  
**Status:** Research

Before designing anything, the right move is to understand what PostHog already uses internally. Their handbook is public. Reading it before an interview or before building anything is basic due diligence — and it changes what's worth building.

**PostHog's actual CS automation stack (from their handbook):**

- **Vitally** — health scores, opportunity/risk indicators, composite metrics. Data synced from Salesforce, PostHog usage, BuildBetter, and Stripe.
- **PostHog pipelines (CDP)** — usage milestone alerts, new product adoption signals, behavioural changes. Outputs to Vitally, Salesforce, or Slack.
- **BuildBetter** — call recording and analysis. Auto-syncs feature requests and pain points to Vitally and a `#feature-request-feed` Slack channel.
- **Zapier** — renewal reminders, stale Slack channel alerts, billing events, failed payment notifications.
- **Pylon** — manages Slack Connect channels per customer. Every customer gets a shared Slack channel; Pylon handles the routing and admin.
- **Salesforce** — CRM backbone that everything syncs into.

**What this tells us:**

The stack is well-designed for *monitoring*. Vitally surfaces signals, Zapier handles triggers, PostHog's own product data feeds back into the health model. The gap isn't in data collection — it's in *prioritisation and action*. A CSM managing 30 accounts who opens Vitally to see 12 indicators, 3 Zapier alerts, and 2 Slack pings still has to make a judgment call about where to start.

The morning question isn't "what happened?" — the tooling covers that. The morning question is **"who needs me today, and why, and what do I actually say?"** That's where human judgment and automation meet, and that's where this project lives.

---

## Entry 003 — Deciding what not to build

**Date:** May 2026  
**Status:** Scoping

This is the most important entry.

It would be easy to build a full customer health dashboard — React frontend, live PostHog API integration, Stripe webhooks, the works. It would also be the wrong call, for several reasons:

1. **It would duplicate Vitally**, which PostHog already pays for. Building a worse version of a tool the company already has is not a good portfolio signal.
1. **It wouldn't be defensible in an interview.** The goal of a portfolio project is to demonstrate thinking, not to demonstrate that you can scaffold a complex app. If asked "walk me through this," the answer should be about *decisions and tradeoffs*, not about explaining framework choices.
1. **Over-engineering is a CS anti-pattern.** A CSM who ships something their team can't understand or maintain is creating a liability. The right tool is the simplest one that solves the actual problem.

**Scope decision:** The prototype will be a structured JSON account model and a short Python script that produces a prioritised morning action list. No framework. No external APIs. No auth layer. The complexity lives in the *design decisions about what signals matter and why* — not in the code.

This decision gets documented because it *is* the decision. Knowing what not to build is the skill.

---

## Entry 004 — The three design decisions that matter

**Date:** May 2026  
**Status:** Design

Before writing any code, three design decisions need to be made explicitly. These are the things someone would ask about in an interview, and the answers need to be reasoned, not post-hoc.

### Decision 1: What signals go in, and why

From the brief, the handbook, and the nature of PostHog's ICP, the candidate signals are:

|Signal                                      |Type    |Notes                                                        |
|--------------------------------------------|--------|-------------------------------------------------------------|
|Days since last contact                     |Leading |Silence before churn, not after                              |
|Days to renewal                             |Leading |Window for intervention narrows fast                         |
|Usage trend (up/flat/down)                  |Leading |PLG churn often starts as usage drift                        |
|Recent support ticket                       |Lagging |Problem already exists                                       |
|Slack channel activity                      |Leading |For PostHog's ICP, Slack silence is louder than email silence|
|Billing/payment status                      |Lagging |Already a crisis                                             |
|Open unresolved issues                      |Lagging |Compounding risk                                             |
|Customer type (self-serve vs sales-assisted)|Baseline|Changes what all other signals mean                          |

**The defensible opinion:** Leading indicators are more valuable than lagging ones for the "never be surprised" success condition. The prototype weights them accordingly.

### Decision 2: No single health score

PostHog's own stack uses Vitally's composite health score. That's a reasonable choice for a tool serving a whole CS team. But composite scores have a specific failure mode: they hide the *shape* of a problem.

A customer with strong usage, an active Slack channel, and a health score of 78 might also have an unanswered renewal conversation from 3 weeks ago. The composite score looks fine. The account is at risk.

**Design choice:** The prototype surfaces signals individually, each with a plain-English reason and a suggested action. The output isn't a number — it's a list of accounts ranked by urgency, with each account showing *which signal triggered it* and *what to do about it*.

That's more useful to a CSM than a score, and it's more honest about what the data actually says.

### Decision 3: Self-serve and sales-assisted need different baselines

A self-serve customer who has never spoken to anyone at PostHog being quiet for 30 days is expected behaviour. They chose not to talk to you. Reaching out unprompted after a month of silence might be the first contact you've ever had.

A sales-assisted customer you personally onboarded being quiet for 14 days is a flag. You built a relationship. The silence means something.

**Design choice:** The account model includes a `customer_type` field (`self_serve` or `sales_assisted`) and the signal thresholds adjust accordingly. This is one of the few places the code makes an explicit behavioural claim — and it's documented here so it's defensible.

---

## Entry 005 — Scope constraint, logged deliberately

**Date:** May 2026  
**Status:** Scoping decision

The prototype is scoped to what can be fully explained and defended in an interview without notes. This is a constraint, not a limitation.

A CSM who ships something they can't explain to a customer or a teammate is creating noise, not value. The same principle applies here. Every function, every field, every threshold in this prototype has a reason that can be stated clearly in plain English.

If a future iteration warrants more complexity — live API integration, a proper frontend, multi-CSM views — the devlog will record why that complexity was added and what problem it solved. Complexity without documented rationale is technical debt.

---

## Entry 006 — What comes next

**Date:** May 2026  
**Status:** Ready to build

The next entries will cover:

- The account data model (field by field, with rationale)
- The signal scoring logic (threshold choices and why)
- The output format (what the morning list actually looks like)
- Any dead ends or adjustments during the build

The prototype will live in `/prototype/` alongside this devlog. The README will frame the project for someone encountering it cold.

---

## Entry 007 — Building the account data model

**Date:** May 2026  
**Status:** Building

Went through each field in `accounts.json` and made explicit decisions about what to include, what to exclude, and why.

**Fields included and why:**

- `account_id` — unique identifier so the script can reference accounts unambiguously; not used in output but useful if this were piped into anything downstream
- `name` — human-readable; what the CSM actually calls the account
- `customer_type` — the most load-bearing field in the model; drives all threshold adjustments; see Entry 004
- `arr` — actual ARR in dollars; used as a tiebreaker within priority tiers (higher ARR ranks first when signal counts are equal)
- `arr_tier` — display string for output ($20k–$50k etc); kept separate from `arr` so the numeric sort uses the real number, not a category
- `days_since_last_contact` — leading indicator; how long since any meaningful touchpoint
- `days_to_renewal` — leading indicator with a hard deadline; the most time-sensitive signal
- `usage_trend` — direction of travel: up, flat, or declining; the direction matters more than the absolute level
- `usage_weeks_declining` — duration of the decline; a one-week dip is noise, four weeks is a signal; this is what the threshold checks use
- `has_open_support_ticket` — boolean gate; ticket age only matters if there is one
- `support_ticket_age_days` — how long the ticket has been open; zero when `has_open_support_ticket` is false
- `slack_channel_active` — tracked but not currently used in threshold logic; it's a leading indicator for PostHog's ICP but the prototype doesn't fire on it independently — included so it's visible in the data and could be added to the script later
- `billing_status` — `current` or `failed`; a failed payment is always urgent regardless of anything else
- `open_unresolved_issues` — tracked in the model but not currently used in threshold logic; included as structural context and to prompt the CSM when they review the raw data
- `expansion_signal` — optional string describing a positive signal (new product adoption, usage growth); not a risk flag, surfaced separately in the OK section
- `notes` — free-text context for the account; not used by the script, there for human review

**Fields deliberately excluded:**

- `champion_name` — relevant context but not needed for the morning priority signal; would add noise without adding logic
- `products_in_use` — matters for health assessment (PostHog CSM Copilot handles that); not needed for the urgency ranking
- `tenure` — useful context but not wired into any threshold; a newer account with a stale ticket is still just a stale ticket

The rule I used: if a field doesn't change the script's output, it only gets included if it's genuinely useful for a CSM reading the raw JSON. Everything else stays out.

---

## Entry 008 — Signal threshold choices

**Date:** May 2026  
**Status:** Building

The thresholds in `morning_priority.py` aren't arbitrary. Here's the reasoning for each.

**Days since last contact:**
- Self-serve: 45 days = WATCH, 60 days = URGENT  
- Sales-assisted: 21 days = WATCH, 30 days = URGENT

Self-serve customers chose not to have a relationship with PostHog. Thirty days of silence is expected, not alarming. Forty-five days is the point where a check-in makes sense before it becomes awkward. Sixty days is late.

Sales-assisted customers have a named relationship with the CSM. Three weeks without contact is noticeable — they'll feel deprioritised. Four weeks is a flag that should have been caught earlier.

**Days to renewal:**
- Both types: 60 days = WATCH, 30 days = URGENT

Renewal threshold is the same for both types because the deadline is the same regardless of how the customer came in. The 60-day mark is where a renewal conversation should open; 30 days is where it should already be in progress. These aren't guesses — they reflect standard enterprise renewal timelines where legal review, budget approval, and stakeholder alignment each take time.

**Usage weeks declining:**
- Self-serve: 2 weeks = WATCH, 4 weeks = URGENT  
- Sales-assisted: 1 week = WATCH, 3 weeks = URGENT

Self-serve accounts have more natural variance in usage — weekends, sprint cycles, seasonal work patterns. Two weeks of decline might be a slow month. Four weeks is a trend.

Sales-assisted accounts are expected to be using the product more deliberately. One week of decline is worth noting, three weeks is a structural change. The shorter tolerance reflects the stronger expectation of active use that comes with a managed relationship.

**Billing failure:**
- Both types: immediate URGENT regardless of anything else

This one doesn't need nuance. A failed payment is a contractual problem that compounds by the day and makes every other conversation harder. It always surfaces first.

**One ranking decision that's worth noting:** within the URGENT tier, failed billing accounts get a scoring boost (effectively +50 to the score) so they always float above accounts flagged only for renewal timing or contact silence. The alternative was pure signal-count ranking, which would let a multi-signal lower-ARR account outrank a billing failure. That felt wrong — a failed payment on a $67k account is more actionable than three soft signals on a $19k self-serve that may already be churning. The boost is explicit in the code and documented here.

---

## Entry 009 — Output format: why text, why these three tiers

**Date:** May 2026  
**Status:** Building

The output is plain terminal text. Not JSON, not a dashboard, not a Slack message (yet). That's deliberate.

**Why text:** The morning list is meant to be read, not processed. A CSM opening their laptop at 8am should be able to scan the list, understand what's happening, and decide on next actions in under two minutes. A well-formatted text output does that. A JSON blob doesn't. A fancy dashboard requires a browser window and a mood.

**Why three tiers instead of a numeric score:**
- URGENT: needs action today
- WATCH: needs a plan this week
- OK: nothing required, but any expansion signals are surfaced here

Three tiers map to three behavioural responses. A numeric score (78, 43, 91) doesn't. The question a CSM asks isn't "is this account an 78?" — it's "do I need to act today, this week, or not at all?" The output answers that question directly.

**Why each account shows triggered signals with a reason and action:**
A list that says "Skyline DevOps — URGENT" is not useful. A list that says "Skyline DevOps — URGENT — 65 days since last contact — for a self-serve customer, silence at 65 days is a late-stage warning sign — reach out today, keep it short" is actionable without requiring the CSM to hold all the context in their head.

The plain-English reason isn't documentation — it's part of the output format. The goal is to reduce the cognitive load between "opening the list" and "sending the first message."

**One format decision that changed during the build:** Initially I planned to render signals in evaluation order (billing → renewal → contact → usage → ticket). But Skyline DevOps evaluates a WATCH signal (renewal) before its three URGENT signals, which produced output where [WATCH] appeared at the top for the most flagged account. Fixed by sorting signals within each account: URGENT first, WATCH second. The sort is one line in `format_account` and it's explained inline.

---

## Entry 010 — Expansion signals: a separate track

**Date:** May 2026  
**Status:** Complete

Panda Analytics is in the OK tier — no flags, all thresholds clear. But they just adopted Session Replay and usage is up 40% week-over-week. That's an expansion signal, not a risk signal. It shouldn't move them into WATCH or URGENT. But it also shouldn't be invisible.

The prototype handles this with an `expansion_signal` field in the account model — a string or null. In the OK section of the output, any account with an expansion signal gets an arrow and the signal description.

The design choice: expansion signals appear in the OK section as informational notes, not as urgency flags. They're conversation starters, not emergencies. A CSM who treats every positive signal as something requiring urgent action creates noise. The morning list should tell you who needs you, not who's doing well.

This keeps the triage logic clean: URGENT and WATCH are risk signals only. Expansion lives in its own track.

---

*This devlog will continue to be updated as the project develops. Entries are written at the time of the decision, not after.*
