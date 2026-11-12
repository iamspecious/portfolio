# Surviving Cancellation: A Crisis Playbook

Version 1.0 · 12 November 2026 · By Specious Coda-Bishop · Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 1. Who this is for, and how to use it

A communications and moderation response kit for studios, open-source projects and community teams: the ones who discover they have no crisis procedure on the day they need one. It isn't only for a public pile-on. The same six incident classes in section 2 cover a broken build, a compromised dependency, a pricing backlash, a conduct complaint and a governance failure just as directly.

**If something is happening right now, skip straight to section 2.** It is four checklists and one table. Come back for the reasoning later: sections 5 to 9 will still be there at 3am next Tuesday.

There is also a standalone, printable [one-page version of section 2](one-page.html), designed to be pinned somewhere visible before you need it, not found by searching for it mid-incident.

**How this document is built.** Section 2 is action only. Section 3 is the modules, each of which opens with a checklist and puts the reasoning underneath. Section 4 is copy-paste templates. Sections 5 to 8 are the evidence, the failure modes, the case files and the post-incident review. Nothing in sections 5 to 8 is needed to act.

## 2. Act

Do these in order. Do not skip 1 or 2.

### 2.1 First 60 minutes

- [ ] **1. Name a Decision Maker and a Comms Owner.** Two different people. The Comms Owner does nothing else until this is over.
- [ ] **2. Open a decision log.** One document. Every decision gets a timestamp, a name and a basis. Start now, not later.
- [ ] **3. Classify the incident** using the table in 2.2. Two minutes. Write the class in the log.
- [ ] **4. Answer: is there anything a user must do right now to protect themselves?** If yes, that goes at the top of your first message. If no, say so explicitly.
- [ ] **5. Identify what you cannot legally say.** Ask before you promise, not after.
- [ ] **6. Take precautionary containment action** if this is a code or access incident. Suspend access, pull the artefact, revoke the key. Frame it as precautionary, not as a verdict.
- [ ] **7. Post the first acknowledgement.** Template 4.1. You do not need answers. You need to show that someone competent is awake.
- [ ] **8. Pick one channel as the source of truth.** Everything else links to it. Nothing gets restated.
- [ ] **9. Tell staff and moderators not to discuss it publicly**, and give them the line to use instead. Template 4.6.
- [ ] **10. Set the next update time and put it in the first post.** Specific time. Timezone included.

### 2.2 Classify: two minutes

Find the row that matches. It tells you which module to open.

| If the situation is… | Class | The question people are really asking | Open module | Who must speak |
|---|---|---|---|---|
| Broken build, outage, data loss, bad patch | **A** Product failure | "Will it be fixed, and did I lose anything?" | 3.2, 3.3 | Engineering lead |
| Malicious, compromised or covertly harmful code in your product or ecosystem | **B** Security | "Is my machine safe right now?" | **3.5** first | Senior engineer |
| Pricing, terms, DRM, account requirements, monetisation, licence change | **C** Commercial | "Do you see us as players or as revenue?" | **3.8** | Studio principal |
| Conduct by a staff member, contractor or prominent community figure | **D** Conduct | "Is this person a danger, and do you agree it was wrong?" | **3.6** | Principal + HR |
| Leadership knew, concealed, misled, or made the call and hid it | **E** Governance | "Can we trust anything you tell us?" | **3.7** | Principal only |
| Factional fighting, moderation dispute, harassment spilling outward | **F** Community | "Is this space safe and are the rules real?" | **3.4** | Community lead |

**Three rules about classes:**

1. **Classes compound.** A Class B handled with silence becomes a Class E within seventy-two hours. Assume compounding is the default.
2. **If leadership knew, it is already Class E.** Run it as one regardless of what it started as.
3. **When two classes are live at once, run both tracks separately and say publicly that you are doing so.** Their timelines conflict, and mixing them makes the fast track look like stonewalling on the slow one.

### 2.3 Hours 1 to 24

- [ ] Assign the remaining roles: Technical Lead, Moderation Lead, Scribe (see 2.5)
- [ ] Publish the moderation rules for this incident **before** enforcing them (Template 4.5)
- [ ] Brief volunteer moderators privately, with permitted lines and permission to step back (Template 4.6)
- [ ] Publish the refund routing notice (Template 4.7)
- [ ] Consolidate discussion into one pinned thread per topic; do not lock anything
- [ ] Begin the fact-finding the second update will need
- [ ] **Hit your stated update time.** Post even if nothing has changed (Template 4.2)
- [ ] Set the ongoing cadence and publish it (12 hours for active security, 24 to 48 for slower matters)
- [ ] Start tracking refund volume daily as your real sentiment metric
- [ ] Rotate anyone who has been reading the firehose for more than four hours

### 2.4 Do not

Short list. These are the moves that reliably make it worse.

- **Do not go silent.** Silence is filled by the least charitable available theory, which then frames everything you say afterwards.
- **Do not lock or purge channels.** It reads as concealment and relocates the conversation somewhere you have no voice.
- **Do not lead with intent.** People have already judged the act. Intent arguments read as excuses.
- **Do not let anyone freelance.** One message, every channel, or silence until the message exists.
- **Do not put junior staff in front.** If it needs a face, it needs the most senior available person.
- **Do not miss a deadline you set yourself.** It is the only thing you are actually building.
- **Do not use euphemism for a deliberate act.** It will be treated as a second deception.
- **Do not promise transparency you are legally unable to deliver.**

### 2.5 Roles card

| Role | Owns | Cannot also be |
|---|---|---|
| **Decision Maker** | Final call on what is said and done | Comms Owner |
| **Comms Owner** | Every outbound word. Drafts, approves, sequences. Full-time. | Decision Maker or Technical Lead |
| **Technical Lead** | Establishing facts. Remediation. Feeds verified findings to Comms. | Comms Owner |
| **Moderation Lead** | Channel policy, moderator briefing, escalations | Anyone with a public voice on this |
| **Scribe** | The decision log | - |

In a small team one person can hold two roles. Never those two pairings.

## 3. Modules

Each module: what to do, then why. Take only what applies.

### 3.1 Command structure

**Do**

- [ ] Name the five roles in 2.5 and tell the team who holds what
- [ ] Free the Comms Owner from all other duties for the duration
- [ ] Start the decision log (Template 4.8)
- [ ] Designate one channel as the source of truth
- [ ] Send the staff line: *During this incident, don't discuss it publicly. Point people to [channel]. This isn't about trust. Inconsistency is what hurts us.*

**Why**

The Comms Owner role is the one that gets skipped and it is the one that matters most. It cannot be bolted onto someone who already has a full-time crisis job, because the moment their primary job demands attention, communication stops, and communication stopping is what turns a bad week into a bad quarter. If you genuinely cannot spare a person, the Decision Maker takes comms and delegates their operational work, not the reverse.

This role separation is the standard structure in mature incident response practice. Established incident response documentation consistently separates command, technical work, communication and record-keeping into distinct roles precisely because one person cannot hold both the technical picture and the external narrative under load.

The decision log exists for three reasons: it prevents contradictory statements across channels, it makes the post-incident review possible, and if any of this becomes a legal matter it is the difference between a defensible process and a reconstruction from memory.

### 3.2 The first statement

**Do, in this order. No reordering.**

- [ ] **Instructing information.** What should a user do right now? If nothing, say so explicitly.
- [ ] **Adjusting information.** Acknowledge the effect on people, not the intent.
- [ ] **What you know**, stated as verified fact. Short.
- [ ] **What you don't know**, stated as open. Be specific.
- [ ] **Next update time.** Exact, with timezone.
- [ ] **Who owns this.** A name and a role.

Use Template 4.1. Do not include: intent, defensiveness, comparisons to other companies, or any promise about an outcome you don't control.

**Why**

The order is not stylistic. The gold-standard framework in emergency communication is the CDC's Crisis and Emergency Risk Communication model, which sets out six principles: be first, be right, be credible, express empathy, promote action, show respect. Two of those bear directly on the order above. On being right, the guidance is to give facts in increments: tell people what you know when you know it, tell them what you don't know, and tell them if you expect to know more later. On credibility, the guidance is blunt: tell the truth, don't withhold to avoid embarrassment, and recognise that uncertainty is worse than bad news because rumour does more damage than hard truth.

The action-first ordering has the same evidential basis. Giving people something specific to do restores a sense of control in circumstances that feel out of control, which is why instructing information outranks everything including the apology.

The same conclusion arrives from the crisis communications literature by a different route. Coombs' Situational Crisis Communication Theory is the most replicated framework in the field, and one of the most common misapplications of it is skipping what he calls the ethical base response (instructing and adjusting information) and jumping straight to reputational strategy. That base response comes first in any crisis regardless of type.

Translated: **tell people what to do and acknowledge the harm before you say anything about yourselves.** Any response that opens with an explanation of the company's intentions has already lost.

**On timing.** For an inbound vulnerability report, the international standard sets meaningful acknowledgement at within seven calendar days. That is the floor for a private report, not a benchmark for a public incident already in progress. For a live incident your window is measured in hours.

### 3.3 Cadence and channel discipline

**Do**

- [ ] Publish a cadence: 12 hours for active security, 24 to 48 for slower matters
- [ ] Hold it without exception, including when there is nothing to report
- [ ] One channel is the source of truth; everywhere else links, never restates
- [ ] No staff member comments independently, including in DMs and side channels
- [ ] Every channel carries the identical message or stays silent until the message exists

**Why**

A published "no change, next update Thursday 18:00" costs nothing and buys real credibility, because it proves the channel is alive. Missing a self-set deadline destroys the only asset you are building.

The restatement rule matters more than it sounds. The moment the same information exists in three slightly different forms, the differences become the story. A well-meaning developer answering honestly in a side channel with detail the official statement doesn't contain will be screenshotted within four minutes and reframed as a leak or a contradiction.

The clearest recent demonstration of what happens without this discipline is the Helldivers 2 account-linking controversy, where the game's own community-facing staff publicly encouraged players to leave negative reviews and file refund requests to pressure the publisher. The commercial consequence was severe: the title accumulated over 369,000 negative reviews at peak and briefly became the most negatively reviewed paid game on the platform.

That is not a story about a bad community manager. It is a story about a team with no comms owner, no agreed message, and a staff member left to improvise a position on a decision they disagreed with and did not control. Give people a script and they don't have to invent one.

### 3.4 Moderation under load (Class F)

**Do**

- [ ] Keep channels open. Consolidate into one pinned thread per topic instead.
- [ ] Publish the moderation rules for this incident before enforcing them (Template 4.5)
- [ ] Remove only: personal information, threats and incitement, content targeting family or uninvolved third parties
- [ ] Log every removal with the rule invoked
- [ ] Never remove a post a reasonable observer would call fair criticism
- [ ] Name and defend the second-order victims explicitly and early
- [ ] Protect the individual at the centre from pile-on, whatever they did

**Why**

Locking is the most common instinct and the most reliably damaging one. It does not stop the conversation. It moves it somewhere you have no presence, no context and no right of reply, and it confirms the concealment theory for everyone watching.

Consolidation achieves the volume control that locking was meant to achieve, is visibly not censorship, and is easy to defend. The removal log is your answer when you are accused of censorship anyway, which you will be.

The credibility of the entire response rests on never removing fair criticism. One wrongly deleted post, screenshotted, undoes a week of good handling.

**Second-order victims** are the people this playbook exists to protect and the ones teams routinely forget: the third party falsely blamed, the uninvolved contributor caught in a boycott, the moderator accused of complicity. Naming and defending them is cheap, correct, and one of the very few actions in a crisis that generates goodwill rather than merely limiting loss.

**Protecting the person at the centre** is not in tension with holding them accountable. Doxxing, threats, contacting family or employers, and harassment of uninvolved people who share a name all get removed and logged, regardless of how justified the underlying grievance is. State it as policy, not as a defence of the person.

### 3.5 Security and supply chain (Class B)

**Do**

- [ ] Contain first: suspend access, pull the artefact, revoke keys. Precautionary, not punitive.
- [ ] Establish and publish, in this order:
  - [ ] Affected artefacts and exact version ranges, with availability dates
  - [ ] Observed behaviour and trigger conditions
  - [ ] **Scope of impact: explicitly state whether anything beyond the observed behaviour occurred.** Files, network calls, credentials, persistence. If nothing, say so. If unknown, give a date for when you'll know.
  - [ ] Detection and timeline: introduced, first observable, reported, confirmed, contained
  - [ ] Remediation done and user action required
  - [ ] Audit scope, reviewer, and publication date
- [ ] Commit to publishing the audit result before you know what it says
- [ ] Use third-party review if you can afford it
- [ ] Never call a deliberate act a bug, an oversight or a compatibility issue

Use Template 4.3.

**Why**

The community's real question is not who did this or whether they'll be punished. It is **"is the code on my machine safe right now."** Answer that and you buy the time to handle everything else properly.

**Crash-only versus data-touching is the single most consequential thing you will publish.** Users cannot assess their own risk until you state it, and until they can, every other message you send is noise.

Run it as an incident, not as PR. The current baseline reference is NIST SP 800-61 Revision 3, published April 2025, which superseded the long-standing Revision 2 handling guide entirely and reorganised incident response around the six functions of the Cybersecurity Framework 2.0. You are not going to implement a NIST profile mid-crisis, but it gives you defensible structure that wasn't invented on the spot. One of its useful shifts is treating improvement as continuous throughout the incident rather than as an end-of-incident retrospective. If you can fix something now, fix it now.

**Self-attestation is worth very little** to an audience that has just discovered it was deceived by someone inside the tent. External review with published scope converts "trust us" into "trust the method."

**On the "it only targeted bad actors" defence.** This surfaces in essentially every incident of this kind and it survives neither ethical nor technical scrutiny. The clearest documented parallel is the 2022 node-ipc case, where a maintainer of a widely-depended-upon package shipped code that damaged files on machines geolocated to particular countries, framed by its author as protest rather than malware. Security analysts described it as destructive corruption of files by a maintainer along with attempts to conceal and restate the sabotage in different forms, and treated the protest motivation as irrelevant to the classification. It followed the colors and faker sabotage weeks earlier and prompted direct questions about whether that maintainer should retain publishing rights at all.

The transferable point: **the ecosystem judged the act, not the intent, and the trust consequence attached to the person's future access rather than to the specific artefact.** Any statement leading with intent is arguing a case the audience has already closed.

### 3.6 Individual conduct (Class D)

**Do**

- [ ] Say plainly that you cannot discuss an individual's employment, **and explain why** (Template 4.4)
- [ ] Move every commitment you can onto the non-personnel track: access controls, review requirements, audit scope and date, policy change, vetting change
- [ ] Separate historic conduct (for investigation) from present conduct: cooperation, remediation, honesty, observable now
- [ ] Run a proper process: investigate, put the allegations, hear them, decide, document
- [ ] Decide internally, early: if the outcome is that they stay, can you defend it publicly with reasons, and will they say something themselves?

**Why**

This is the module where good instincts do the most damage, because the transparency reflex that serves you in Class B is actively harmful here. You cannot discuss an individual's employment status or process publicly while it is running. That is not corporate evasiveness. It is a constraint that exists in most jurisdictions partly to protect the accused's right to a fair process, which is worth defending even when it's inconvenient.

**The move that costs nothing and changes everything is explaining the silence.** "We're not commenting" reads as protection. "We can't discuss any individual's employment while a process is running, that applies whatever the outcome turns out to be, and it exists to make the process fair. Here's what we can talk about" reads as procedure.

**Then convert "trust this person" into "you don't have to trust any individual, including us."** A community demanding someone's removal is usually, underneath, demanding a guarantee. Removal is one way to provide it. Structural control is a better one, because it survives the next person and it doesn't depend on an outcome you can't promise.

If the honest answer to the last checkbox is no, the outcome is already decided and the only remaining variable is how many weeks you spend discovering it. Negotiated exits exist for exactly this configuration and are almost always reached later than they should be.

### 3.7 Governance failure (Class E)

**Do**

- [ ] Disclose it yourselves, first, in full, before anyone else finds it
- [ ] All four parts: what was known, when and by whom; what the reasoning was; why it was wrong; what has structurally changed
- [ ] The principal speaks, in their own voice, by name
- [ ] Do not moderate the rumour. Answer it with dated specifics or accept that it becomes permanent.

**Why**

This is the most damaging class and it has the fewest options. A self-disclosed governance failure is a serious problem. An exposed one is a terminal credibility event, because every prior statement you made retroactively becomes a lie.

Three parts out of four reads as spin. All four or don't bother.

**Unfalsifiable rumours are a governance problem, not a moderation problem.** When a community starts theorising that leadership knew, silence cannot disprove it and moderating it away confirms it. The only thing that touches it is a direct, dated, specific factual statement from the principal. If you can't make that statement, understand clearly that the theory is now permanent.

There is a decent illustration of the named-human effect in the Helldivers case: an earlier formal acknowledgement that simply redirected players to publisher support failed to slow the reviews at all. What began the recovery was the studio CEO publicly accepting that the backlash was warranted and apologising for how it had unfolded. The formal redirect failed. The named person accepting the criticism as legitimate worked.

### 3.8 Commercial decision backlash (Class C)

**Do**

- [ ] Decide within 24 hours, honestly: would you reverse this under enough pressure?
- [ ] If yes, **reverse now**, not in week four
- [ ] If genuinely no, name the actual constraint and stop defending the decision on its merits
- [ ] Do not argue that the change was in the terms

**Why**

Class C is the only class where reversal is on the table, which changes the entire calculus. The most common error is treating a reversible decision as a matter of principle.

A reversal in week one is a company listening to its players. The identical reversal in week four is a company that had to be forced. You pay the full reputational price for a decision you ended up unmaking anyway.

**The evidence that reversal works is strong.** In the Helldivers case the publisher dropped the account-linking requirement within days of the peak. Players then reversed their own reviews at scale: over 200,000 positive reviews in a single day. The title moved off the most-negatively-reviewed position it had briefly held. The damage was almost entirely recoverable because the underlying decision was.

"We are legally entitled to do this" is true and irrelevant. The community is not making a legal claim. "We don't have a choice and here's why" is survivable. "This is actually good for you" is not.

### 3.9 Refunds and commerce

**Do**

- [ ] Publish refund routing on day one (Template 4.7)
- [ ] Honour your own published policy at its most generous reading
- [ ] Process fast, no case-by-case argument
- [ ] Track daily volume as your primary sentiment metric
- [ ] Get legal advice on your specific policy wording. Do not resolve it yourself under pressure.

**Why**

The refund exposure is almost always small. The reputational cost of appearing to renege is not. A refusal becomes the story; a refund is a transaction.

**Routing is the cheap win.** If most sales run through third-party storefronts, those platforms' policies govern those purchases, and a large slice of your inbound anger will be from people who believe they're being stonewalled when they're actually in the wrong queue. One paragraph removes a whole category of grievance.

**Discretionary language is still a representation.** Wording along the lines of *you can ask outside the normal limits and we'll take a look* is a promise to consider, not an unconditional guarantee, but it creates an expectation, and the gap between the expectation and your behaviour is what gets screenshotted. Departing from your own published commitments once customers have relied on them also raises unfair-practice questions under UK and EU consumer regimes.

**You do not control the refund perimeter.** In sufficiently visible incidents, storefronts have extended eligibility well beyond their normal windows independently of the developer. Valve did exactly that during the Helldivers episode.

**Refunds beat vibes as a metric.** Discord temperature measures the loudest twenty people. Refunds measure decisions.

### 3.10 Your people

**Do**

- [ ] Brief volunteer moderators before the public statement (Template 4.6)
- [ ] Give them permitted lines and explicit permission to say "I don't have that information"
- [ ] Tell them they can step back at any point with no consequence
- [ ] Give them a private channel to a named staff member
- [ ] Rotate anyone in the mentions every four hours
- [ ] Keep junior staff off the front line

**Why**

Volunteer moderators are the most exposed and least supported people in the entire event. They are unpaid, publicly identified, and absorbing abuse for decisions they didn't make and often weren't told about.

Rotation is a welfare measure and also a quality measure: judgement degrades fast under sustained hostility.

Putting a community manager in front of a decision they didn't make is both a welfare failure and a strategic one, because the audience knows they lack authority and reads the substitution as evasion.

Your duty of care to the individual at the centre does not lapse either. A serious harassment outcome becomes its own crisis on top of the one you already have.

## 4. Templates

Copy, edit, rewrite in your own voice. Credit belongs in whatever internal document you paste them into, not in the message you publish.

### 4.1 First acknowledgement (0 to 3 hours)

> **[Plain description of the issue. No marketing language.]**
>
> **What you should do right now:** [Specific action, or: "No action is needed on your side. If that changes we will say so here first."]
>
> [One or two sentences acknowledging the effect on people. Effect, not intent.]
>
> **What we know:** [Two to four verified facts. Nothing unverified.]
>
> **What we don't know yet:** [Two or three specific open questions. Specificity here builds more credibility than reassurance does.]
>
> **What happens next:** [Name, role] is coordinating our response. The next update will be posted here by **[exact date, time, timezone]**, whether or not we have new information by then.
>
> Updates are posted in this thread first and linked everywhere else.

### 4.2 Holding update

> **Update ([date, time])**
>
> No substantive change since the last update. [One sentence on what is actively being worked on.]
>
> Next update by **[exact date and time]**.

### 4.3 Technical findings (Class B)

> **Technical findings ([date])**
>
> **Affected:** [Exact artefact names and version ranges]
> **Available between:** [dates]
> **Observed behaviour:** [What it did, under what conditions]
> **Scope of impact:** [State explicitly whether anything beyond the observed behaviour occurred: file access, network activity, credentials, persistence. If nothing, say so plainly. If unknown, say so and give a date.]
> **How this was found:** [Detection path; credit the finder if they consent]
> **Timeline:** [Introduced / first observable / reported / confirmed by us / contained]
>
> **What we have done:** [Removal, revocation, patching, access changes]
> **What you should do:** [Specific user action, or explicit "none required"]
>
> **Audit:** [Scope: what is being reviewed and by whom.] Findings will be published by **[date]** regardless of what they contain.

### 4.4 Constrained silence (Class D)

> We know people want to know what's happening with the individual involved, and we understand why.
>
> We can't discuss any individual's employment or any process relating to it. That restriction applies to us whatever the outcome turns out to be, and it exists to make sure the process is fair. That isn't a satisfying answer, but we'd rather tell you the constraint than go quiet.
>
> Here's what we can commit to, and none of it depends on the outcome:
>
> - [Access control change, specific]
> - [Review requirement, specific]
> - [Audit scope and publication date]
> - [Policy or process change]
>
> The point of these is that they don't require you to trust any individual, including us.
>
> Next update by **[date and time]**.

### 4.5 Moderation policy statement

> **How we're moderating this discussion**
>
> This thread stays open. For the duration of this incident we are removing only:
>
> - Personal information about any individual
> - Threats, incitement, or calls to contact people privately
> - Content targeting family members or uninvolved third parties
>
> We are not removing criticism of us, however harsh, and we are not removing posts for tone.
>
> Every removal is logged with the rule it was removed under. If you think we've got one wrong: [contact route].
>
> [Name] is responsible for moderation decisions during this incident.

### 4.6 Moderator brief (internal, send before the public statement)

> **For our moderators ([date])**
>
> **What's happening:** [Two or three sentences, plainly.]
> **What's being published and when:** [Link and time.]
> **What you can say:** [Three or four approved lines.]
> **What not to discuss:** [Specific constrained topics.] If asked, use: *"I don't have that information and I'm not the right person to ask. [link] is where updates go."* Using that line is the correct answer, not a failure.
> **Escalate to [name] immediately for:** threats, personal information posted, press contact, anything involving a minor.
> **You can step back at any point, for any reason.** Tell [name] and we'll cover it.
> **Private channel:** [link]. [Name] is monitoring it.

### 4.7 Refund routing notice

> **On refunds**
>
> If you bought through [Platform A / B / C], those purchases are handled under that platform's process: [links]. We don't control those and can't process them for you.
>
> If you bought directly from us: [process, contact route, turnaround].
>
> We're not going to argue with anyone about this.

### 4.8 Decision log entry

```
TIMESTAMP    : [ISO 8601 with timezone]
DECISION     : [One sentence]
DECIDED BY   : [Name, role]
PRESENT      : [Names]
BASIS        : [Information this rested on, and its source]
ALTERNATIVES : [Briefly]
ACTION OWNER : [Name], due [date/time]
PUBLISHED?   : [Yes/No, where and when]
```

## 5. Why this works

Not needed to act. Useful when you're deciding whether to trust it, adapting it, or arguing for it internally.

### The communication principles underneath

The gold-standard framework in emergency communication is the CDC's Crisis and Emergency Risk Communication model, developed for public health emergencies and widely adopted well beyond them. It sets out six principles: **be first, be right, be credible, express empathy, promote action, show respect.**

The specific guidance behind three of those directly shapes section 2 and module 3.2:

- **Be first.** If the information is yours to give, give it as soon as possible; if you can't, explain how you're working to get it. First sources become the standard everything else is measured against.
- **Be right.** Give facts in increments. Say what you know when you know it, say what you don't know, and say when you expect to know more.
- **Be credible.** Tell the truth, don't withhold to avoid embarrassment, and understand that uncertainty is worse than bad news because rumour does more damage than hard truth.

**Promote action** is why instructing information sits above the apology: giving people something specific to do restores a sense of control in circumstances that feel out of control.

CERC also defines five lifecycle stages: pre-crisis, initial, maintenance, resolution, evaluation. Section 2 covers initial, section 3 covers maintenance, section 8 covers evaluation, and the last instruction in section 8 is to build your own pre-crisis stage.

### Why the class matters more than the severity

Coombs' Situational Crisis Communication Theory is the most heavily replicated framework in crisis communications. Its core claim is that stakeholders assign *responsibility* before they assign anger, and that response strategy must be matched to the level of attributed responsibility. It groups crises into victim, accidental and intentional clusters, and responses into deny, diminish and rebuild families, with crisis type, crisis history and prior reputation together predicting how audiences will attribute blame.

Two findings are load-bearing for this playbook:

- **Preventable crises damage reputation more than any other type, and rebuild strategies (apology and compensation) produce the strongest recovery for them.** Almost everything in classes C, D and E is a preventable crisis. Deny and diminish are the wrong tools and will read as contempt.
- **The ethical base response comes first regardless of type.** Skipping instructing and adjusting information in favour of reputational strategy is one of the most common misapplications of the framework.

### Same outcome, different route

Several classes end in the same visible outcome: a statement, an audit, a policy change, sometimes a departure. They cannot be run the same way, and pretending otherwise is how teams make promises in week one they have to break in week three.

**Speech constraints differ.** Class B: publish facts as fast as you can verify them. Class D: you are legally constrained and will remain so for the whole process. Applying Class B instincts to Class D prejudices the process and creates liability. Applying Class D caution to Class B looks like a cover-up.

**Timelines differ and conflict.** Security remediation runs in hours. Employment process runs in weeks and cannot be compressed without exposure. Community patience runs to about forty-eight hours. Split them publicly and explain that you're splitting them, or the slow track poisons the fast one.

**Reversibility differs.** Class C decisions can be reversed and often should be. Class B and D facts can only be remediated. Teams frequently try to reverse their way out of a Class B by shipping a fix and saying nothing, which fails because the trust question was never about the code.

**The evidentiary bar differs.** An unverified technical claim costs you a correction. An unverified claim about a named individual costs you a defamation exposure.

**Who can credibly speak differs.** Class C and E require the principal. No community manager can carry a governance failure, and asking them to is unfair and ineffective in equal measure.

### Why this document is shaped the way it is

The structure is not arbitrary. It follows what the human factors literature established about procedural documents used under stress. Most of it was developed for aviation checklists, and explicitly intended by its authors to transfer to other high-risk domains.

**Short-term memory is the binding constraint.** Degani and Wiener's foundational work on flight-deck checklists identifies limited working memory as one of the greatest constraints on human performance, and notes that many procedural documents place unrealistic demands on it. The mitigation they describe is chunking: grouping items into defined units around a common factor, so a long procedure becomes a small number of retrievable groups rather than one undifferentiated list. That is why section 2 is four short checklists rather than one list of thirty items, and why the modules in section 3 are separate rather than continuous.

Their other design recommendations that this document tries to honour: restricted vocabulary, frequently used words, sequential ordering that matches the order of actual operation, and clear allocation of duties between people rather than to "the team."

**Findability beats completeness.** The prevailing view in incident response practice is that a runbook nobody can find during an incident may as well not exist, and that conflicting documents breed hesitation. Each procedure needs one definitive source so responders know which document to trust under pressure. Hence: one file, action at the front, no cross-referencing you have to chase, and a single source-of-truth rule applied to your own channels as well.

**Start simple and add granularity later.** Mature incident response guidance recommends not worrying about severity tiers at the beginning. Just establish whether something is an incident, get the roles and the trigger working, and add sophistication once the basic process runs. This playbook deliberately has no severity matrix for the same reason. If you get to the point of needing one, you've outgrown this document, which is the correct outcome.

## 6. Failure modes

| Failure mode | Why it fails |
|---|---|
| Silence in the first 24 hours | Vacuum fills with the least charitable theory, which frames everything after |
| "We take X seriously" with no facts | Reads as a template; signals you have nothing or are hiding something |
| Locking or purging channels | Confirms concealment; relocates the conversation beyond your reach |
| Mass-banning critics | Converts a product story into a censorship story, which travels further |
| Leading with intent | The act has already been judged; intent reads as excuse-making |
| Missing a self-set deadline | Destroys the one thing you were building |
| Different messages on different channels | The discrepancy becomes the story within hours |
| Junior staff carrying senior decisions | Audience knows they lack authority; reads as evasion; harms the staff member |
| Euphemism for a deliberate act | Treated as a second deception, because it is one |
| Promising transparency you can't legally deliver | Guarantees a visible broken promise in week three |
| Reversing in week four what you could have reversed in week one | Full price, no credit |
| Treating the loudest voices as the whole community | Distorts severity in both directions; use refunds and churn |
| No decision log | No review is possible and no defensible account exists |

## 7. Case files

Short, sourced, each isolating one transferable mechanism.

**Helldivers 2 / PSN account linking (2024), Class C.** A publisher-mandated account-linking requirement triggered one of the largest review-bombing events in the platform's history, peaking above 369,000 negative reviews, with community staff publicly directing players toward reviews and refunds, and the title pulled from sale in a large number of territories where the required accounts weren't available. The publisher reversed within days, the studio CEO publicly accepted the criticism as warranted and apologised, and players reversed their reviews at scale: over 200,000 positive reviews in a single day. **Mechanism:** reversal works, and works fast, when the decision is reversible. Absence of comms discipline turns internal disagreement into public escalation.

**node-ipc / peacenotwar (2022), Class B.** A maintainer of a widely-depended-upon package shipped code causing file damage on machines in particular locations, framed by its author as protest. Security analysis described it as destructive corruption of files by a maintainer with attempts to conceal and restate the sabotage in different forms, treating the protest motivation as irrelevant to classification. It followed the colors and faker sabotage weeks earlier and prompted direct questions about whether the maintainer should retain publishing privileges. **Mechanism:** ecosystems judge the act, not the stated target or motive, and the trust consequence attaches to the person's future access rather than to the artefact.

**Package registry incidents generally, Class B.** The pattern is consistent: a maintainer account or artefact is compromised or sabotaged, a version ships, and the damage is done before flagging because automated systems pull dependencies continuously. Dormant or lightly maintained packages retain broad ecosystem reach long after active development stops, so a recovered or hijacked maintainer identity can reach a large dependency graph without ever touching source control. **Mechanism:** in a modding or plugin ecosystem your exposure is not your own code. It is every widely-installed community artefact and every account that can publish one. Ecosystem-level controls are the durable fix; individual accountability is not.

## 8. After

Run this within two weeks of the incident closing, while people still remember.

- [ ] When could we first have known, and when did we actually know? The gap is your detection problem.
- [ ] What did we say that we later had to correct? Why did we say it?
- [ ] Which commitments did we hit, and which did we miss? Missed ones are the durable damage.
- [ ] Where did approval bottleneck?
- [ ] Who absorbed the worst of it, and what did we do for them?
- [ ] What structural control would have prevented this, and is it now in place, with a named owner and a date?

**Then write your own two-page version of this.** Your product, your channels, your team, names filled in. Store it somewhere findable at 2am. Review it, on your own schedule, while this stays current. It takes an afternoon and it is the highest-return preparation available to a small team.

The current NIST guidance makes this point structurally: improvement is continuous through the incident lifecycle, not reserved for a retrospective at the end. If there's something you can fix now, fix it now.

## 9. Sources and changelog

### Communication frameworks

- CDC, [*Crisis and Emergency Risk Communication (CERC)*](https://emergency.cdc.gov/cerc/index.asp) manual and tools
- Coombs, W.T. (2007), [*Protecting Organization Reputations During a Crisis: The Development and Application of Situational Crisis Communication Theory*](https://link.springer.com/article/10.1057/palgrave.crr.1550049), Corporate Reputation Review
- Coombs, W.T., [*Situational Crisis Communication Theory (SCCT)*](https://onlinelibrary.wiley.com/doi/10.1002/9781119678953.ch14), in The Handbook of Crisis Communication
- Claeys, Cauberghe & Vyncke (2010), *Restoring reputations in times of crisis*, Public Relations Review

### Incident response and disclosure

- [NIST SP 800-61 Revision 3](https://csrc.nist.gov/projects/incident-response), *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* (April 2025)
- [ISO/IEC 29147:2018](https://www.iso.org/standard/72311.html), *Vulnerability disclosure*
- ISO/IEC 30111, *Vulnerability handling processes*
- [CERT/CC, *The CERT Guide to Coordinated Vulnerability Disclosure*](https://certcc.github.io/CERT-Guide-to-CVD/)
- [PagerDuty, *Incident Response Documentation*](https://response.pagerduty.com/)

### Document design under stress

- Degani, A. & Wiener, E.L. (1993), [*Cockpit Checklists: Concepts, Design, and Use*](https://journals.sagepub.com/doi/10.1177/001872089303500209), Human Factors 35(2)
- Degani, A. & Wiener, E.L. (1990), *Human Factors of Flight-Deck Checklists: The Normal Checklist*, NASA Contractor Report 177549
- [Flight Safety Foundation, *Making a List*](https://flightsafety.org/asw-article/making-a-list/)

### Case material

- [Snyk (2022), *Alert: peacenotwar module sabotages npm developers in the node-ipc package*](https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/)
- [CSO Online (2022), *Developer sabotages own npm module*](https://www.csoonline.com/article/572327/)
- [Kotaku (2024), Helldivers 2 review-bombing response and platform refunds](https://kotaku.com/helldivers-2-steam-reviews-apology-psn-login-1851455150)
- [Game World Observer (2024), PSN linking reversal](https://gameworldobserver.com/2024/05/06/helldivers-2-psn-linking-removed-review-bombing-positive)
- [VideoGamer (2024), review reversal volumes](https://www.videogamer.com/news/helldivers-2-is-no-longer-the-most-negatively-reviewed-game-as-players-undo-the-mass-review-bombing/)

### Licence

Take it, adapt it, rewrite it in your own voice, build your own version on top of it. That's the point of publishing it. The only ask is attribution, and it's deliberately easy:

- **Internal credit is fine.** A line in your process doc, a note on the wiki page, a comment at the top of the file. It does not have to be public.
- **Never in a crisis post.** If you're using a template in a live statement, credit belongs in the document it came from, not the message going to users.
- **It can wait.** Nobody handles attribution at hour three.
- **Cost is never the blocker.** This is free and stays free. Small team, volunteer project, solo developer, community with no budget: use it and don't think about it again.
- **If you adapt it, keep a link in the adapted version** so the next person can find the original.

Commercial use is permitted, including paid work built on it. Scope: communications, coordination and moderation only. This is not legal advice; employment and consumer law questions raised here are jurisdictional and need a qualified local practitioner.

### Changelog

- **v1.0 (12 November 2026).** First release under this title and in this format. Content carried over from the original standalone build, published under the title "The Small Studio Crisis Playbook" since September 2026, restructured to markdown-as-source-of-truth with the rest of the Playbooks series and renamed to foreground that this covers more than small studios.
