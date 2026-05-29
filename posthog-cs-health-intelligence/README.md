# PostHog CS Health Intelligence

A thought exercise and research-backed prototype built to demonstrate understanding of the problem space for a Technical CSM role at PostHog. The audience is a hiring team. Every decision in this project should be explainable in plain English without notes.

---

## Introduction

PostHog's CS tooling stack is well-designed for monitoring. Vitally surfaces composite health scores, PostHog's own CDP pipes usage signals into Salesforce and Slack, Zapier handles renewal reminders and billing alerts, and BuildBetter auto-syncs call notes and feature requests. A CSM using these tools has a lot of data.

The gap isn't in data collection — it's in prioritisation and action.

A CSM managing 30 accounts who opens Vitally to find 12 indicators, 3 Zapier alerts, and 2 Slack pings still has to decide where to start. The morning question isn't "what happened?" — the tooling covers that. The question is: **who needs me today, why, and what do I actually say?**

This prototype addresses that gap. It's a structured JSON account model and a Python script that reads it and produces a prioritised morning action list. For each flagged account, the output shows: which signal triggered the flag, a plain-English reason it matters, and a specific suggested action.

**What PostHog context informed this:**

- Their ICP communicates on Slack, not email. Slack silence is a stronger signal for their customers than it would be for most.
- Two distinct customer types — self-serve and sales-assisted — need fundamentally different engagement models and different signal thresholds. Treating them the same is the most common CSM mistake at a PLG company.
- PLG churn is typically silent. It starts as usage drift, not as a conversation. The "never be surprised" success condition in the brief requires leading indicators, not just lagging ones.
- PostHog already has Vitally's composite health score. Building a worse version of that wasn't useful. Building the prioritisation layer that sits on top of it was.

The full decision trail is in [DEVLOG.md](./DEVLOG.md). Every threshold, field, and design choice is documented there with rationale.

---

## Wins

**The signal weighting model reflects a defensible position on leading vs lagging indicators for PLG churn.**  
Days since last contact, usage trend, and days to renewal are leading indicators. Support tickets and failed payments are lagging. The script weights leading indicators by firing on them before they become obvious — which is the whole point of the "never be surprised" success condition.

**Self-serve and sales-assisted thresholds are implemented throughout, not just noted.**  
A self-serve customer going quiet for 30 days is expected. A sales-assisted customer going quiet for 21 days is a WATCH flag. This distinction runs through every contact and usage signal in the script, not just mentioned in a comment.

**No composite health score, and that's a deliberate design decision with a documented reason.**  
Composite scores hide the shape of a problem. An account with strong usage and a failed billing payment looks fine on a composite score. It's at risk. The prototype surfaces signals individually so the shape of the problem is visible.

**Failed payment gets a ranking boost that's explicit and explainable.**  
Within the URGENT tier, billing failures float to the top. The reason: a failed payment on a high-ARR account is more actionable than three soft signals on a lower-ARR self-serve account that may already have churned. The boost is one line in the code and one paragraph in the devlog.

**The output format is designed for human decision-making, not for further processing.**  
Plain text, three tiers, reason and action per signal. A CSM should be able to read the list and know what their first three messages are before their second coffee.

**Expansion signals are a separate track, not a risk flag.**  
Panda Analytics adopted Session Replay this month and usage is up 40%. That's a conversation starter, not an emergency. It appears in the OK section with a note rather than moving the account into WATCH. Treating positive signals as urgency creates noise.

**Under 130 lines of Python that a non-developer hiring manager could follow.**  
The complexity in this project is in the design decisions, not the code. That's intentional. See Entry 003 in the devlog.

---

## Constraints

**No live data integration.**  
The account model is manually maintained JSON. In practice, this data would flow from Vitally, Salesforce, and PostHog's CDP. The prototype demonstrates the logic layer; the plumbing would depend on what data the team already has structured.

**No frontend.**  
The output is terminal text. That's the right format for a morning triage tool used by one CSM. If this were team-wide, a Slack-formatted digest or a lightweight web view would be the next step.

**Slack channel activity is tracked but not used in threshold logic.**  
`slack_channel_active` is in the account model because Slack silence is a meaningful signal for PostHog's ICP. It's not currently wired into the WATCH/URGENT logic because it would need per-account baseline data to be useful — a channel that's always quiet is different from one that went quiet. The field is there for a future iteration.

**Open unresolved issues are tracked but not scored.**  
`open_unresolved_issues` is in the model as contextual data. It doesn't trigger a flag on its own because the severity of an issue matters more than the count. A CSM reviewing the raw JSON can see it; the script doesn't act on it without more signal.

**Fictional accounts only.**  
The 10 accounts in `accounts.json` are representative of real situations but aren't real data. The prototype demonstrates the model; populating it from live sources is a separate and straightforward engineering problem.

**This is a prototype, not a production tool.**  
It demonstrates that the problem space is understood and that there's a coherent approach to solving it. A production version would need authentication, a data pipeline, error handling for missing fields, and probably a more sophisticated ranking model. Those aren't hard problems — but adding them here would obscure the actual thinking, which is what this project is meant to show.

---

## Running it

```
cd prototype/
python3 morning_priority.py
```

Requires Python 3.6+ and no external dependencies. `sample_output.txt` shows what the output looks like.
