# People Practice Playbook, Vol. 3: Building HR Tools with AI

Version 0.1.1 · 12 November 2026 · By Specious Coda-Bishop · Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## 1. Who this is for, and what it isn't

*Section last reviewed 12 November 2026.*

AI can help build software well, but only when someone who understands the system is steering and checking the work. Handing an AI a wish list and shipping whatever comes back is a different thing, and it isn't free.

This volume is for people who are new to AI and are being asked to approve, fund or build an internal tool with it: People and HR teams, founders, operations leads, and anyone sitting in the meeting where someone says "we could just build it ourselves". It uses an HR system (an HRIS) as the running example, because that's where the stakes are clearest.

**The short version:**

- **Vibe coding** (describe it, accept what comes back, never read the code) is fine for throwaway experiments. It isn't fine for a system that holds employee data and that other people rely on.
- **AI-assisted engineering** (a person plans, checks and owns every change, with AI doing much of the typing) is how AI builds real software well.
- **"We already pay for AI, so building is free" doesn't hold up.** A seat price is the minimum spend, not the real bill.
- **If your organisation builds anyway,** section 10 lists the steps that make it much less risky.

**What it isn't.** It isn't legal advice: laws on employee data and on AI vary by country and state, so check what applies to you locally. It isn't a coding tutorial. And it isn't anti-AI. I use AI heavily, including to research and draft this volume.

**About the numbers.** Every cost here is an example, there to show the kinds of things you'd need to estimate for your own project. None of it is a quote. Pricing examples use Claude, the tool this volume was researched with; other providers also bill by usage, with their own rates. Prices change often, so check the live pages linked in section 4.

### This will change

- **Versions.** A big version bump means a recommendation has changed. A small one means new sections or examples. The smallest means fixes.
- **Changelog.** Every change is listed in section 13, newest first.
- **Review dates.** Each section shows when it was last reviewed.
- **Changing my mind.** Where a call is genuinely arguable, there's a short note on what would change it.
- **Licence.** CC BY-SA 4.0. Share and adapt it, with credit to Specious Coda-Bishop, under the same licence.
- **Corrections.** By pull request on the [GitHub repository](https://github.com/iamspecious/portfolio) or by email to <work.specious@gmail.com>. Corrections that change a recommendation are credited in the changelog.

## 2. Four ways people use AI

*Section last reviewed 12 November 2026.*

These often get called the same thing, but they carry very different levels of risk. The difference is who decides, who checks, and who fixes it when it breaks.

| Approach | What it looks like | Who checks the result | When it breaks |
| --- | --- | --- | --- |
| AI as an assistant | Asking questions, drafting emails, summarising documents | You, by reading it | You redo one answer |
| Automation with AI | AI as one step in a fixed workflow, such as reading expense receipts and filing them by category | Whoever set up the workflow | One step can fail quietly, but the rest of the process is known and can be checked |
| Vibe coding | Describing an app and accepting the code the AI writes, without reading or testing it | Nobody, really. If it seems to work, it ships | Nobody knows why, so the AI is asked to guess at a fix |
| AI-assisted engineering | A person who understands software plans the work, has AI write parts of it, then reviews and tests every change | A skilled person, before anything goes live | Someone can trace the cause, fix it and explain it |

Programmer Andrej Karpathy coined "vibe coding" in February 2025 for a way of building where you ["forget that the code even exists"](https://martinfowler.com/bliki/VibeCoding.html). Software writer Martin Fowler draws the same line this volume does: ignoring the code is vibe coding, while using AI and still reviewing the code is a different practice, which he calls agentic engineering. He notes the two get mixed up because "vibe coding" caught on as a catch-all.

Programmer and writer Simon Willison defends vibe coding for personal tools, where a bug only hurts the person who built it. For software other people rely on, he calls it ["grossly irresponsible"](https://simonwillison.net/2026/may/6/vibe-coding-and-agentic-engineering), because it's other people's information, and other people get hurt by the bugs. He also points out that the AI has no professional reputation. A person is accountable for what gets shipped.

## 3. The sandcastle

*Section last reviewed 12 November 2026.*

Ask an AI to "build me a sandcastle" and it will. It scoops up whatever is on the beach, packs it into the bucket and flips it over. For a moment it looks like a castle.

But the bucket held dry sand, shells and bits of plastic. Nobody checked the mix. The castle slumps the moment the bucket lifts, or it stands until the first wave, or until someone leans on a wall.

Build it the other way and you decide the sand-to-water ratio first. You lay a solid base. You build one tower, check it holds, then build the next. It takes more thought up front, and it stands.

| On the beach | In software |
| --- | --- |
| "Build me a sandcastle" | A vague request with no requirements |
| The full bucket | The AI's first draft, which looks finished |
| Shells and plastic in the mix | Hidden junk: unused code, unsafe shortcuts, outside components nobody chose |
| Sand-to-water ratio | The plan: requirements, rules and limits written down before building |
| Checking each tower before the next | Testing each change before adding more |
| The first wave | Real staff, real data, an attacker, or a change in the rules |

The catch for non-engineers: with a sandcastle, you can see it fall. With software, many failures are invisible. A security hole or a wrong calculation can look fine for months until someone finds it.

## 4. Tokens: what you're actually paying for

*Section last reviewed 12 November 2026.*

Every AI model reads and writes in tokens, and usage is measured in them. That's true for Claude, ChatGPT, Gemini and the rest, even though each counts tokens slightly differently.

> **Check current prices:** [Claude pricing](https://claude.com/pricing) · [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing). The figures below were correct in November 2026 and are here as examples.

- **A token** is a small chunk of text: a short word, or part of a longer one. The same text can produce different counts on different models. Anthropic notes its newer models produce [about 30% more tokens for the same text](https://platform.claude.com/docs/en/about-claude/pricing) than older ones.
- **Input tokens** are everything the AI reads: your request, the instructions, the conversation so far, and any files or code it looks at.
- **Output tokens** are everything it writes back. On Claude's current models, output costs five times as much as input.
- **The context window** is how much the AI can hold in view at once. Bigger projects fill more of it, on every request.

### Two ways organisations pay

**Pay per token (the API).** Prices in November 2026, in US dollars per million tokens ([source](https://platform.claude.com/docs/en/about-claude/pricing)):

| Model | Input | Output |
| --- | --- | --- |
| Claude Opus 5.5 | $4 | $20 |
| Claude Sonnet 5.5 | $2 | $10 |
| Claude Haiku 5.5 (requests up to 100,000 tokens; higher above that) | $0.10 | $0.50 |

**Pay per seat (subscriptions).** On Claude's Team plan, a Standard seat is $20 a month billed annually ($25 monthly) and a Premium seat, meant for heavier use, is $100 ($125 monthly) ([source](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)). Each seat has its own usage limits per session and per week. Limits are per person and can't be pooled. When someone hits theirs, they wait for the reset or the organisation pays for extra usage.

### A worked example (illustrative)

Coding tools don't just read your request. They re-read large parts of the project each time, to understand what they're changing. Say a mid-sized internal app means each request reads 150,000 tokens and writes 5,000, on Opus 5.5 at API prices:

- Input: 150,000 × $4 ÷ 1,000,000 = $0.60
- Output: 5,000 × $20 ÷ 1,000,000 = $0.10
- **About $0.70 per request.** A hundred requests in a working day is about $70, or roughly $1,400 over 20 working days.

Caching (reusing text the AI has already read) cuts this a lot. If 140,000 of those input tokens are cached, a request drops to about $0.17, or roughly $340 over the same month. The project size is made up and the sums leave out caching set-up costs, but the shape holds: **the bigger the project, the more every request costs.**

## 5. Why "we already pay for AI" doesn't make it free

*Section last reviewed 12 November 2026.*

The AI bill is the visible part of the cost, and usually not the biggest part. Building with AI swaps one known subscription for many smaller costs, most of which nobody has added up.

### Why vibe coding burns through usage

- **Each change costs more than the last.** As the app grows, the AI reads more of it on each request.
- **Bug loops.** When nobody understands the code, the fix for a bug is to ask the AI again, and again. Each attempt is paid for, and a fix can break something else.
- **Vague requests mean rework.** "Make it better" produces a guess. Wrong guesses get thrown away, but the usage is still spent.
- **Seat limits run out.** Our take: a full HR system that other people log into is very unlikely to get built within the normal limits of a few seats. When limits are hit, the organisation pays for extra usage or bigger seats, or the work stalls until the reset. A stalled build costs staff time.
- **AI features inside the app cost per use.** If the finished system uses AI itself, for example to screen CVs or answer staff questions, that usage is usually billed by the token, on top of any seats.

### The all-in comparison (illustrative)

This is the comparison to put in front of decision-makers. The example subscription is $300 a month, or $3,600 a year.

| Cost | Buying an HRIS | Building one with AI |
| --- | --- | --- |
| Software | Subscription, e.g. $3,600 a year | AI seats, plus extra usage when limits run out |
| Hosting, logins, backups | Usually included | Paid separately, and someone has to set them up |
| E-signatures | Usually included or integrated | Usually another paid service, so signatures hold up |
| Security testing and audits | Usually done by the vendor (check their security page) | Your cost, if it happens at all |
| Rule changes | Usually handled in vendor updates | Someone has to notice, then rebuild |
| Fixing bugs | Vendor support | Your staff time, plus usage |
| When the builder leaves | The product carries on | Nobody may understand the system |
| A data breach | The vendor handles the technical response; your own duties to staff and regulators stay with you | All yours: investigation, fixing it, your duties to staff and regulators, legal costs, higher insurance premiums |
| HR's own time | Routine tasks are a click | Time spent testing, reporting bugs and working around gaps |

For a sense of scale on the breach line: IBM's 2026 Cost of a Data Breach report puts the global average cost of a breach at $4.99 million, and breaches took 247 days on average to find and contain ([IBM report](https://www.ibm.com/reports/data-breach), via [eSecurity Planet's summary](https://www.esecurityplanet.com/cybersecurity/ibm-2026-cost-of-a-data-breach-report-key-findings/)). These are averages across the organisations IBM studied, not a prediction for yours. Even a breach costing a small fraction of that would outweigh years of subscription fees.

The question to ask whoever is proposing the build: **what is the full yearly cost, including people's time, and who owns each line?** If nobody can answer, the "free" option hasn't been costed.

*What would change my mind:* real cost records from a comparable organisation that built and ran its own HR system, including staff time, for less than a subscription over two or more years.

### Feeling faster isn't the same as being faster

In a 2025 randomised trial by the research group METR, 16 experienced developers worked on 246 real tasks. With AI tools they [took about 19% longer](https://arxiv.org/abs/2507.09089), yet afterwards believed AI had made them about 20% faster. METR's [2026 follow-up](https://metr.org/blog/2026-02-24-uplift-update/) with newer tools found signs that AI now speeds people up, but called its own data "only very weak evidence", partly because some developers declined to take part, or held back tasks, rather than work without AI. The lesson isn't that AI is slow. It's that how fast AI *feels* is a poor guide to how fast it *is*. Measure the time actually spent, including fixing and checking.

## 6. Why an HR system is a risky place to start

*Section last reviewed 12 November 2026.*

An HRIS is a system of record. It holds some of the most sensitive data an organisation has, and people's pay, leave and rights depend on it being right.

- **Sensitive data:** home addresses, bank details, ID documents, salaries, absence and health notes, disciplinary records, right-to-work checks.
- **Rules on data:** most places have rules on how employee data is stored, who can see it, how long it's kept and what happens after a breach. They vary by location and they change.
- **Many users:** employees, managers and HR each need different access. Getting permissions wrong means someone sees a colleague's salary or medical note.
- **Audit trails:** you may need to show who changed what and when, for example in a dispute.
- **Links to other systems:** payroll, benefits, e-signatures, rota tools. Each link is another thing that can break or leak.

### AI-written code is often insecure by default

Security firm Veracode has tested code from more than 100 AI models since it began this research. In its July 2026 report, the code was almost always valid, but it [failed about 44% of security tests](https://sdtimes.com/agentic-security/veracode-finds-ai-generated-code-security-has-barely-improved-since-last-year/) when nobody asked for security specifically. Models built for coding did no better than general ones. Veracode sells security tools, so weigh that. Fowler makes a similar point: vibe-coded apps [can expose sensitive data or credentials](https://martinfowler.com/bliki/VibeCoding.html), and a change in one place can quietly break another.

### A real example

Thoughtworks [published a case](https://martinfowler.com/articles/vibesec-reckoning.html) from its own marketing team in May 2026. A non-technical colleague built a prototype video tool with AI. When the team's engineers then worked with AI to scale it up, the AI recommended storing files so that anyone with a link could open them, and when challenged, said every company does this. A service account was also given far more access than the task needed, which the team caught before running the code. Both problems were caught because a person asked a question, and the tool then went out to 150 users. The team's lesson: telling an AI to be secure doesn't make it secure. Note that the AI pushed these defaults on professional engineers, not just a beginner.

### Describing a standard isn't the same as meeting it

Our take: a common suggestion is to give the AI a vendor's security and compliance pages and ask it to match them. It won't do what people hope. Those pages describe results: outside audits passed, encryption in place, penetration tests done, a breach response team on call. Each one stands for months of work, staff to run it and an independent firm checking it.

An AI that reads those pages can produce code that looks secure: a login screen, a setting labelled "encryption". Whether it protects anything is something only a skilled reviewer can tell. If nobody in the room could check the result, the AI hasn't replaced the expertise. It has hidden that the expertise is missing.

## 7. Fairness, privacy and access

*Section last reviewed 12 November 2026.*

Whatever you build, plan for these three things from day one. This section sticks to practice. Where the law comes into it, the rules vary by country and state and are changing quickly, so check what applies to you locally with an adviser.

### Fairness

- **Unfair outcomes are your problem, whoever wrote the code.** If the system screens, ranks, scores or flags people, someone in your organisation needs to own checking its results for bias. Using a vendor's tool doesn't hand that job away.
- **Rules on AI in hiring and employment are still being written and rewritten.** Check what applies to you before the system touches any decision about people.
- **A vibe-coded system can bake in bias without anyone choosing it,** for example through default categories, required fields or filtering rules nobody reviewed. Ask who might be treated differently, and test for it.

### Privacy by design

Build data protection in from the start rather than adding it later. In my view that means at least: collecting only what you need, making the most private setting the default, limiting access by role, and assessing the risks before going live. AI tools tend to default to convenience instead, as the example in section 6 shows.

### Accessibility

Everyone on staff has to be able to use the system, including people who use screen readers, keyboard-only navigation or magnification. The W3C's [WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the current version of its accessibility guidelines. You can ask the AI to build to it, but checking that it did means testing with real assistive technology, and with disabled colleagues who are willing to try it.

## 8. Try it: plan one module before building anything

*Section last reviewed 12 November 2026.*

The best way to see what building an HRIS involves is to plan one small part of it properly. It takes an afternoon, costs only time, and is useful whatever you decide. If you build, it's your spec. If you buy, it's your checklist for comparing vendors.

Take leave requests. On the surface it's one sentence: *staff request leave and their manager approves it.* Underneath, these are the questions someone has to answer before the code can be right.

| Area | Questions you'll need to answer | Who usually answers |
| --- | --- | --- |
| Policy rules | Is leave given yearly or built up monthly? How is it worked out for part-timers and people who join or leave mid-year? Can it carry over, and does it expire? Half days or hours? Can a balance go negative? | HR |
| Leave types | Holiday, sick, parental, bereavement, unpaid, time off in lieu. Does each have its own rules and balance? | HR, with legal advice |
| Public holidays | Do they differ by location? Who updates them each year? | HR |
| Approvals | Who approves when the manager is off? Can HR override? What happens if approved leave is cancelled? | HR and an engineer |
| Who sees what | Can staff see colleagues' leave? Who can see the reason for sick leave? | HR, legal adviser, engineer |
| Records | Where is the data stored? How long is it kept? Is every change logged? What's deleted when someone leaves? | Legal adviser and engineer |
| Links to other systems | Does unpaid leave or holiday pay on leaving go to payroll? Do approvals send emails or appear in calendars? | Engineer |
| Awkward cases | Overlapping requests, policy changes mid-year, fixing a past mistake, time zones for remote staff | HR and engineer, then tests |
| Running it | Logins and password resets, backups, what happens if it's down on payroll day, who fixes bugs | Engineer or IT |

### How to use the exercise

1. **Answer everything you can.** Most of the policy questions are yours, and writing them down is valuable on its own.
2. **Mark what you can't answer.** Be honest. Those gaps are where the risk is.
3. **Look at the "engineer" column.** If nobody in your organisation can answer those, an AI can't answer them for you either. It will guess, and the guesses will look finished.
4. **Multiply.** Leave is one module. A basic HRIS also covers employee records, onboarding and leaving, documents and e-signatures, reporting, and often recruitment. Each has a table like this one.

This isn't meant to put anyone off trying. Trying is often the fastest way to learn. Planning one module properly usually shows what a vendor has already done for you, and where AI-assisted engineering, with people who know how to build software, has to come in.

## 9. Asking like an engineer, not making a wish

*Section last reviewed 12 November 2026.*

What an AI builds depends heavily on what you tell it. A good request is a small plan: what it's for, who uses it, what data it touches, what must never happen, and how you'll know it works.

### The same feature, asked two ways

**The wish:**

```
Build a time-off request system for our staff.
```

The AI has to guess who can approve, what happens to balances, who can see what, and how data is stored. It will guess, and it will look finished.

**The plan:**

```
I want to build ONE small piece: a form where an employee requests annual leave.
Don't write any code yet. First, reply with a plan and a list of risks.

Users:
- Employees can request leave and see only their own requests.
- Their direct manager can approve or reject. Nobody else can.

Rules:
- A request can't be longer than the employee's remaining balance.
- Approved requests reduce the balance. Rejected ones don't.
- Every approval or rejection is logged with who did it and when.

Must never happen:
- One employee seeing another employee's requests or balance.
- Real employee data being used while we test. Use made-up test people.

Done means:
- Write tests that check each rule above, and show me them passing.
- Explain in plain English what you built, and anything you're unsure about.
```

### Habits that make the biggest difference

1. **Plan before code.** Ask for a plan and a risk list first, and read it.
2. **One small piece at a time.** One form, one rule, one screen. Check it works before moving on.
3. **Say what must never happen.** AI often leaves security out unless asked (section 6).
4. **Ask for tests.** Tests are small checks that a rule works, and they keep checking it after later changes.
5. **Ask it to explain.** If the explanation doesn't make sense to you, nobody on the team understands the system yet.
6. **Ask what could go wrong.** Ask "what are the risks in what you just built?" and take the answer seriously.

### Not sure what you want yet? Let the AI interview you

Anthropic's own guidance suggests asking the AI to [interview you until it could write the spec](https://code.claude.com/docs/en/best-practices), then building from that written spec in a fresh session. This suits non-engineers, because the AI asks about the parts you hadn't thought of:

```
I want to build a leave request form for a 30-person company. I haven't
thought it through yet. Interview me, one question at a time, until you
could write a full spec. Include questions about who can see what, what
must never happen, and how we'll test it. Then write the spec. No code.
```

### What the AI companies themselves say

The companies selling these tools give much the same advice:

- **Plan before code.** [OpenAI's Codex guide](https://learn.chatgpt.com/guides/best-practices) says to plan first when a task is complex or unclear, and suggests having the AI interview you. Anthropic's guide suggests the same interview step.
- **Give it a way to check its work.** [Anthropic notes](https://code.claude.com/docs/en/best-practices) that without a pass-or-fail check, the AI stops when the work *looks* done, and you become the test.
- **Ask for evidence.** Not "all tests pass", but the command it ran and the result.
- **A prompt is a request, not a guarantee.** Anthropic is explicit that a model usually follows an instruction but isn't guaranteed to. Anything that must *never* happen needs enforcing through settings or automated checks, which someone technical has to set up.
- **Start fresh rather than arguing.** If two corrections haven't fixed it, start a new session with a better request.

Google's Cloud developer team [reached similar conclusions](https://cloud.google.com/blog/topics/developers-practitioners/five-best-practices-for-using-ai-coding-assistants) after using its Gemini tools on complex projects: save a step-by-step plan and approve it before anything is built, give the AI the details you'd give a new teammate, and keep a running notes file so each session picks up where the last one left off. GitHub has turned the plan-first approach into a free toolkit, [Spec Kit](https://github.github.com/spec-kit/), where a written spec feeds a plan, the plan feeds a task list, and only then does the AI write code.

A better request makes vibe coding safer, but it doesn't turn it into engineering. Someone still has to be able to check the answer.

## 10. If you're building it anyway: the guardrails

*Section last reviewed 12 November 2026.*

Nobody can stop every organisation from vibe coding. These steps don't make it safe, but they make it far less risky. Each one is something a non-engineer can do or insist on.

### Before you start

- [ ] Write down the one problem it solves, in a sentence. If you can't, stop here.
- [ ] Name an owner who is responsible for it after launch, and a backup person.
- [ ] Set a budget and turn on spending caps and usage alerts in the AI tool.
- [ ] Agree what data it will hold, and leave out anything you don't strictly need.
- [ ] Check which data rules apply to you, with a qualified adviser.

### While building

- [ ] Don't use real employee data. Test with made-up people.
- [ ] Use version control from day one. It keeps every past version, so a bad change can be undone. Ask the AI to set it up.
- [ ] Build one small piece at a time, from a written plan (section 9).
- [ ] Ask for tests for every rule, and run them after every change.
- [ ] Keep a short decision log: what was built, why, and what's still unsure.
- [ ] Don't paste passwords, keys or real records into the AI chat.
- [ ] Question every permission the AI suggests. Be wary of anything public, "anyone with the link", or broad access to company systems.
- [ ] Don't accept "everyone does it this way" from an AI. Ask for the most secure option and the trade-off.

### Before anyone else uses it

- [ ] Have a qualified engineer review the code and the security. This is the one step not to skip.
- [ ] Check every role's access: can an employee see anything they shouldn't?
- [ ] Run an attacker review: ask the AI, in a fresh session, to act as someone trying to break in or see data they shouldn't, and list what it finds. Treat it as a first pass, not a substitute for the engineer review.
- [ ] Confirm backups exist, and test restoring one.
- [ ] Write down what happens if it breaks: who gets called, and how people keep working in the meantime.
- [ ] Plan your exit: how you'd move the data into a bought system if this doesn't work out.

The permission and attacker-review steps are adapted from [Thoughtworks' VibeSec Reckoning](https://martinfowler.com/articles/vibesec-reckoning.html).

## 11. Which approach fits?

*Section last reviewed 12 November 2026.*

Match the approach to what's at stake. The more people who rely on it, and the more sensitive the data, the further down this table you are.

| What you're making | Example | Approach | Who needs to be involved |
| --- | --- | --- | --- |
| A throwaway experiment | A mock-up to show what a leave form could look like | Vibe coding is fine | Just you |
| A personal helper | A spreadsheet formula, a script that renames your files | Vibe coding, with care and no sensitive data | You, checking the results |
| A team workflow | Filing expense receipts, drafting standard letters from a template | Automation or AI-assisted engineering | Someone who can check it, and an owner |
| A system of record | HRIS, payroll, applicant tracking, anything with employee data | Buy a proven product; build only with real engineering | Engineers, security review, legal advice, a named owner |

Our take: for most small and mid-sized organisations, the honest answer for an HRIS is to buy one, and use AI around it for the tedious parts that don't involve sensitive data.

*What would change my mind:* an organisation with its own engineers and security staff, or a need no product on the market meets. Both shift the answer towards building, with AI-assisted engineering.

## 12. Glossary

*Section last reviewed 12 November 2026.*

| Term | Plain meaning |
| --- | --- |
| Agent | An AI tool that takes several steps on its own, such as reading files, writing code and running it |
| Context window | How much text the AI can hold in view at once |
| Hallucination | When an AI states something false with confidence, or writes code that seems right but isn't |
| Model | The AI itself, such as Claude Sonnet or GPT. Different models cost different amounts |
| Production | The live version real people use, as opposed to a test version |
| Prompt | The instructions you give the AI |
| Spec | A written plan of what to build and the rules it must follow |
| System of record | The official source of truth for something, such as who works here and what they're paid |
| Technical debt | Shortcuts that make a system harder and costlier to change later |
| Test | A small automated check that a rule works |
| Token | A small chunk of text. AI usage is measured and billed in tokens |
| Version control | A record of every change to the code, so mistakes can be undone |

## 13. Sources and changelog

*Section last reviewed 12 November 2026.*

### Sources

Free to read, as far as we could check. IBM's full report may ask you to sign up.

- [Anthropic: Claude pricing](https://claude.com/pricing) and [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing). Vendor documentation. Model prices, tokenizer note.
- [Claude Help Center: What is the Team plan?](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) Vendor documentation. Seat prices, usage limits.
- [Anthropic: Best practices for Claude Code](https://code.claude.com/docs/en/best-practices). Vendor documentation. Checks, evidence, enforcement, interviews.
- [OpenAI: Codex best practices](https://learn.chatgpt.com/guides/best-practices). Vendor documentation. Plan first, tests and review.
- [Loftesness and Davenport: Five best practices for using AI coding assistants](https://cloud.google.com/blog/topics/developers-practitioners/five-best-practices-for-using-ai-coding-assistants) (Google Cloud, October 2025). Vendor blog. Plans, context, prompting.
- [GitHub Spec Kit](https://github.github.com/spec-kit/). Open-source project site. Spec, plan, tasks, implement.
- [Martin Fowler: Vibe Coding](https://martinfowler.com/bliki/VibeCoding.html) (May 2026). Practitioner essay. Definition, origin of the term, limitations.
- [Simon Willison: Vibe coding and agentic engineering are getting closer than I'd like](https://simonwillison.net/2026/may/6/vibe-coding-and-agentic-engineering) (May 2026). Practitioner blog. Accountability, software for others.
- [Koul, Moss, Drew-Lopez and Edeokoh: The VibeSec Reckoning](https://martinfowler.com/articles/vibesec-reckoning.html) (Thoughtworks, May 2026). Practitioner case study. Real-world case, guardrails.
- [Becker, Rush, Barnes and Rein: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/abs/2507.09089) (METR, 2025). Randomised controlled trial, preprint. And [METR's February 2026 update](https://metr.org/blog/2026-02-24-uplift-update/).
- [SD Times on Veracode's 2026 GenAI Code Security Report](https://sdtimes.com/agentic-security/veracode-finds-ai-generated-code-security-has-barely-improved-since-last-year/) (July 2026). Veracode press release, published via SD Times. Veracode sells security tools.
- [IBM: Cost of a Data Breach Report 2026](https://www.ibm.com/reports/data-breach), figures taken from [eSecurity Planet's summary](https://www.esecurityplanet.com/cybersecurity/ibm-2026-cost-of-a-data-breach-report-key-findings/). Vendor research, reported by trade press.
- [W3C: Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/). Standards body.

Prices, research and rules in this area change quickly. If you spot something wrong or out of date, corrections are welcome.

### Changelog

| Version | Date | What changed |
| --- | --- | --- |
| 0.1.1 | 12 November 2026 | Fixes from the first integrity audit. Section 7 reworded to practice only, with legal detail left to local advice. Thoughtworks example corrected to match the source. Expense receipts replace CV sorting as the low-stakes automation example. Buy-vs-build table softened where it overstated what vendors do, and breach row corrected. Smaller wording fixes (Willison paraphrase, METR follow-up, Veracode scope, Haiku pricing tier, "tests check" not "prove"). Corrections links added. |
| 0.1 | 12 November 2026 | First version. |

---

People Practice Playbook, Vol. 3 · Specious Coda-Bishop · [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
