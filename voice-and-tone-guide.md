# Voice & Tone Guide for Technical Documentation Teams

Internal contributor guide defining voice, tone, and writing standards for technical documentation teams.

---

## Introduction

This guide defines the voice and tone standards for contributors writing technical documentation. It covers the characteristics of our voice, how tone shifts depending on context, and the writing principles that keep documentation consistent and useful.

**Who this is for:** anyone writing, reviewing, or editing documentation — whether you're contributing for the first time or you've been writing docs for years and have strong existing habits.

**Why consistent voice matters in technical documentation:** Documentation is used in moments of friction. A reader arrives because something isn't working, because they're learning something unfamiliar, or because they need to make a decision quickly. Inconsistent voice makes readers decode *how* something is written at the exact moment they're trying to understand *what* it says. That overhead is avoidable.

Consistent voice doesn't mean every page sounds identical. It means every page comes from the same team with the same standards. A reader moving from a tutorial to an API reference should feel they're in the same documentation system — not switching between two different writers with two different ideas of what documentation should be.

This guide gives you a shared set of defaults. Use it to make decisions without needing to ask for guidance every time.

---

## Voice vs Tone

**Voice** is consistent. It's the underlying character of the documentation — who we are as a team. Voice doesn't change based on what you're writing.

**Tone** is contextual. It's how we modulate that character depending on what the reader is trying to do and what they're likely feeling while they're doing it.

**A technical documentation example:**

Consider the same event — a breaking API change — appearing in three different places:

- In a **migration guide**, tone is methodical and reassuring. Walk through the change step by step. Acknowledge that it requires effort.
- In an **API reference entry**, tone is flat and neutral. State the new behaviour, the old behaviour, and the version it changed in. No warmth, no softening.
- In a **release note**, tone is brief and factual. One sentence stating what changed, a link to the migration guide.

The voice — precise, direct, empathetic — stays constant across all three. The tone changes because the reader's situation is different in each.

---

## Our Voice

### We are precise, not pedantic.

We get the details right. We don't omit things that matter. But we don't list every qualifier and edge case inline when most readers don't need them. Detail that serves the reader stays in. Detail that serves completeness for its own sake comes out.

**Before:**

> The `limit` parameter, which accepts integer values within the inclusive range of 1 to 25, controls the total quantity of result objects returned within the JSON array response payload.

**After:**

> The `limit` parameter controls how many results are returned. Accepts integers from 1 to 25.

---

### We are empathetic, not patronising.

We acknowledge that some things are difficult, unfamiliar, or frustrating — without being condescending about it. We don't add "simply" or "just" to steps that aren't simple. We don't praise readers for completing routine tasks.

**Before:**

> Simply navigate to the settings panel and just click the toggle to enable the feature. Easy!

**After:**

> Go to **Settings** and enable the feature toggle.

---

### We are direct, not terse.

We get to the point without skipping the context that makes the point usable. A three-word instruction that leaves the reader stranded is not better than a sentence that orients them.

**Before:**

> Call `/v1/refresh`. Requires token. Returns 200.

**After:**

> Call `/v1/refresh` with a valid access token to start a new session. Returns `200 OK` on success.

---

### We are confident, not absolute.

We state things clearly and without excessive hedging. We don't qualify every sentence with "should", "might", or "in most cases" when the behaviour is deterministic. When there are genuine exceptions, we name them specifically instead of hedging vaguely.

**Before:**

> This should work in most cases, though results may vary depending on your environment.

**After:**

> This works for standard PostgreSQL setups. If you're using a managed database service, check your provider's documentation for the correct connection string format.

---

### We are consistent, not rigid.

We use the same term for the same thing every time — across a page, a doc set, a product. We don't vary terminology for stylistic variety. But consistency applies to terminology and structure, not sentence rhythm. Two sentences don't need to be built the same way to feel consistent.

**Before:**

> Click the **Run** button to execute the build. Hit **Deploy** to push your changes. Press the **Rollback** control to revert.

**After:**

> Click **Run** to start the build. Click **Deploy** to push your changes. Click **Rollback** to revert.

---

## Tone by Context

### Instructional content

Task-focused, imperative, present tense. The reader is trying to do something. Walk them through it without editorialising. Each step is one action. Confirm what success looks like at the end.

> 1. Open the project in your IDE.
> 2. Navigate to **File > Settings > Plugins**.
> 3. Search for the plugin by name and click **Install**.
> 4. Restart the IDE when prompted. The plugin appears in the left sidebar after restart.

---

### Error messages

State what happened, why it happened, and what to do next — in that order. Don't blame the user. Don't be vague. Don't pad with apologies.

**Before:**

> An unexpected error has occurred. Please try again later.

**After:**

> `401 Unauthorized` — The API key is missing or invalid. Check that the `x-api-key` header is included in your request and that the value matches your dashboard key exactly.

---

### API reference documentation

Flat and neutral. No personality, no softening, no encouragement. State the input, the behaviour, the output, and the constraints. Use tables for structured data. The reader is using this as a lookup, not reading end-to-end.

> **`order`** `string` — Optional. Sort order for results. Accepted values: `RANDOM`, `ASC`, `DESC`. Default: `RANDOM`. When set to `RANDOM`, pagination is disabled and the `page` parameter is ignored.

---

### Onboarding content

Warmer than reference documentation, but still direct. Anticipate the questions a new user is likely to have and answer them before they need to ask. Explain *why* as well as *how*. Acknowledge when something won't make full sense until later.

> Before you can make API requests, you'll need an API key. Keys identify your account and track usage against your monthly limit. You can generate one from the dashboard — it takes under a minute, and you'll only need to do it once.

---

### Warnings and cautions

Lead with the consequence, not the action. The reader needs to understand what they're risking before they decide whether to proceed. Keep it short. Don't bury the warning in a long paragraph.

**Before:**

> Note: Please be aware that running this command in a production environment without first taking a backup of your database could potentially result in permanent data loss.

**After:**

> **Warning:** This command permanently deletes data. Back up your database before running it in a production environment.

---

## Writing Principles

### 1. Lead with the action

Put the verb at the start of instructions. Readers scan for what to do next — don't make them hunt for it inside a noun-heavy phrase.

**Before:** `Selection of the correct environment variable is necessary before deployment.`

**After:** `Set the correct environment variable before deploying.`

---

### 2. Write for the user's current state

Ask: what does this reader already know, and what are they trying to accomplish right now? Don't assume they've read everything that came before, but don't re-explain basics they must already have in order to be at this step.

**Before:** `As mentioned in the introduction, authentication is required. Authenticated users can access all endpoints.`

**After:** `Authenticated requests unlock all endpoints. See [Authentication](#authentication) if you haven't set up a key yet.`

---

### 3. Prefer active voice

Active sentences are shorter, clearer, and easier to act on. Passive voice hides who does what — and in technical documentation, that ambiguity costs the reader time.

**Before:** `The configuration file is generated automatically when the project is initialised.`

**After:** `The IDE generates a configuration file when you initialise the project.`

---

### 4. One idea per sentence

If a sentence needs a semicolon or a second clause joined by "and", consider splitting it. Readers of technical documentation are often scanning under pressure — shorter sentences parse faster.

**Before:** `The webhook fires on every push event, and you can configure it to filter by branch, though this requires setting up a filter rule in the payload settings, which is covered in the next section.`

**After:** `The webhook fires on every push event. You can filter by branch using a payload filter rule — see [Filtering webhooks](#filtering-webhooks).`

---

### 5. Use second person

"You" keeps focus on the reader and what they need to do. Avoid "the user", "one", or "developers should" — these create distance and make instructions feel like they're describing someone else.

**Before:** `Developers should ensure the dependency is installed before running the build script.`

**After:** `Install the dependency before running the build script.`

---

### 6. Cut the setup

Don't explain what you're about to explain. Don't open with "In this section, we will cover...". Don't close with "As you can see...". Start the explanation. The reader is already here.

**Before:** `In this section, we will walk through the process of configuring your environment. This is an important step that many new users find confusing.`

**After:** `Configure your environment before running the project for the first time.`

---

### 7. Name the behaviour, not the category

Describe what a thing does in this specific context, not what kind of thing it is. Readers need to know what happens — not what label applies.

**Before:** `The \`retry\` parameter is a configuration option that affects request behaviour.`

**After:** `The \`retry\` parameter sets the number of times the client retries a failed request before returning an error.`

---

### 8. End steps with an outcome

When writing instructions, tell the reader what success looks like after each significant step. Don't leave them wondering whether they did it right.

**Before:** `Run \`npm install\`.`

**After:** `Run \`npm install\`. Once it completes, a \`node_modules\` directory appears in the project root.`

---

## Common Mistakes

### "Simply" and "just"

These words don't add warmth — they minimise difficulty. When the step turns out not to be simple, they make the reader feel inadequate. Cut them entirely.

**What not to do:** `Simply restart the server to apply the changes.`

**Corrected:** `Restart the server to apply the changes.`

---

### Nominalised verbs

Turning verbs into nouns adds length without adding meaning. Common offenders: "make a selection" (select), "perform a restart" (restart), "provide configuration" (configure), "give consideration to" (consider).

**What not to do:** `Make a selection from the available options and perform a confirmation of your choice.`

**Corrected:** `Select an option and confirm.`

---

### Hedging deterministic behaviour

When something always happens, say so. Reserve "should", "may", and "might" for genuinely uncertain outcomes — when the result depends on the user's environment or a condition you can't predict.

**What not to do:** `Setting this flag should cause the build to skip tests.`

**Corrected:** `Setting this flag skips the test suite.`

---

### Stacked noun phrases

A chain of nouns used as modifiers becomes ambiguous and slow to parse. Break the chain or restructure the phrase.

**What not to do:** `Check the authentication token validation error handling configuration.`

**Corrected:** `Check how error handling is configured for authentication token validation.`

---

### Passive voice hiding the actor

The passive is occasionally appropriate, but it becomes a problem when it obscures who is responsible for an action — especially in instructions, where the reader needs to know who does what.

**What not to do:** `The flag should be set before the build is run.`

**Corrected:** `Set the flag before running the build.`

---

### Undefined jargon

Terms obvious to you after months in the codebase may not be obvious to a reader encountering them for the first time. Define or link technical terms on their first use — even when it feels unnecessary.

**What not to do:** `Enable the EAP channel before installing the nightly build.`

**Corrected:** `Enable the [Early Access Program (EAP)](https://www.jetbrains.com/resources/eap/) channel before installing the nightly build.`

---

## Contributor Checklist

Use this before submitting documentation for review.

- [ ] Does every instruction step start with an imperative verb?
- [ ] Have you used "you" consistently instead of "the user" or "developers"?
- [ ] Have you used the same term for the same thing throughout the document?
- [ ] Is each sentence one idea? Check for sentences with multiple clauses joined by "and" or separated by semicolons.
- [ ] Have you removed setup sentences that don't add information? ("In this section, we will...")
- [ ] Does each warning lead with the consequence, not the action?
- [ ] Have you defined or linked technical terms on their first use?
- [ ] Does each significant instruction step end with what success looks like?
- [ ] Have you removed "simply", "just", "easy", and "obvious" from all instructions?
- [ ] Have you replaced passive constructions with active ones wherever the actor is relevant?
- [ ] Does the tone match the content type? (Reference: flat and neutral. Onboarding: warmer. Error messages: specific and actionable.)
- [ ] Have you read the document as someone encountering this feature for the first time?
