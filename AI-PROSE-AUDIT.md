# AI-Prose Audit

**Date:** 2026-06-21
**Scope:** Visitor-facing copy in `index.html` and `front-door-config.json`, prioritising the newest additions (denim case study, Digital Spec entry + dev log, front-door lane blurbs).
**Reference:** `voice-and-tone-guide.md` — the human's real voice: *precise not pedantic, direct not terse, confident not absolute, names the behaviour not the category, cuts the setup and the filler.*
**Status:** READ-ONLY. Nothing below was edited. These are recommendations only.

The voice guide's most relevant rule for this audit is **Principle 7 — "Name the behaviour, not the category."** Almost every flag below is a variant of the same failure: reaching for a balanced epigram ("X, not Y" / "the constraint is the feature") or a rhythmic flourish where a plain statement of what the thing *does* would be more honest and more in-voice.

Flags are ordered by visibility: About copy and front-door blurbs first (seen before anything else), case-study and project openers next, dev-log entries and bullets last.

---

## 1. About Me  *(default landing tab — highest visibility)*

| Location | Passage (quoted) | Tell | How the voice guide differs |
|---|---|---|---|
| About card "Orientation" | "…isn't a winding path — **it's** a consistent pattern of being useful…" | "not X, it's Y" antithesis + dramatic em-dash | Guide names the behaviour directly; drop the setup-and-reveal framing. |
| About card "Orientation" | "Generalist **by design**" | "by design" epigram (recurs 4× across the site — see §3, §4) | A label, not a behaviour. State what the generalism *does*. |
| Para 3 | "I'm also **genuinely** technically curious." | Filler intensifier ("genuinely") | Guide: confident not absolute — cut the intensifier, the claim stands alone. |
| About card "Approach" | "…logged — **not polished after the fact, but documented as it happened**." | "not X, but Y" antithesis + em-dash | Say it plainly: "logged as it happened." |
| About card "Principle" | "…because **that's what honest work looks like**." | Generic uplift closer | Guide: cut the closer ("Don't close with 'As you can see…'"). The constraints section already makes the point. |
| Cards "Strength" / para 2 | "The interesting problems are almost always at that boundary." / "that's where the interesting problems tend to live." | Repeated motif across cards (tidy parallelism) | Guide: consistency is about terminology, not reused rhetorical beats. Vary or cut the duplicate. |

**Read as human voice (leave alone):** Para 1 ("drawn to the places where things aren't quite working, and I find the structural reason why") and para 4 (LoreBySpec → KH Lore Checker). Specific, plain, in-voice.

---

## 2. Front-door lane blurbs & node text  *(`front-door-config.json` — first interactive surface)*

| Location | Passage (quoted) | Tell | How the voice guide differs |
|---|---|---|---|
| `laneIntros.cs-support` | "it runs deep — **not just answering tickets well, but building the systems that stop the tickets**…" | "not just X, but Y" antithesis + em-dash | State the stronger claim directly: "…building the systems that stop the tickets happening at all." |
| `laneIntros.creator-lore` | "**it's not a hobby bolted on, it's** the same pattern-tracing brain pointed at narrative." | "not X, it's Y" antithesis + em-dash | Guide: drop the contrast scaffold; "the same pattern-tracing brain, pointed at narrative" carries it. |
| `laneIntros.ops-strategy` | "systems thinking, alignment without authority, **and the discipline to know what not to build**." | Rule-of-three / tricolon, colon-led parallel list | Guide: one idea per sentence; the tidy triad reads as rhythm-for-its-own-sake. |
| `laneIntros.builder-technical` | "Spec builds small, sharp tools and **— the part most people skip —** documents the decisions…" | Em-dash interjection for a dramatic pause | Guide: lead with the action. "…builds small tools and documents the decisions as he goes." |
| `nodes.whoisspec` | "a generalist **by design**" | "by design" epigram (also in §1, §3, §4) | Same as §1 — name the behaviour. |
| `nodes.kh-lore` | "For an ultra-niche audience, that's **genuinely** impressive." | Filler intensifier | The sub count already makes the point; cut "genuinely." |

**Read as human voice (leave alone):** `implementation` blurb ("getting a product live in someone else's messy real-world setup"), and the `nodes.opening` / `whoareyou` text — conversational, specific, no tells.

---

## 3. Denim case study  *(case-study opener — flagged in front door as "the thing Spec's proudest of building")*

| Location | Passage (quoted) | Tell | How the voice guide differs |
|---|---|---|---|
| Diagnosis para (l.503) | "…what we wanted the customer experience to *be* — **not just 'fewer angry emails,' but** the standard of care…" | "not just X, but Y" antithesis + em-dash + italic emphasis pile-up | Guide: precise not pedantic; one clean statement of the standard, no contrast scaffold. |
| Diagnosis para (l.503) | "That reframing — **inbound as a visibility problem, not a staffing problem** — shaped everything after it." | "X, not Y" antithesis inside an em-dash interjection | The reframing is genuinely good; state it without the balanced-contrast packaging. |
| Bullet s7 (l.513) | "**Navigated** cross-border duty-of-care obligations." | LLM-favourite verb ("navigate") | Guide: lead with a concrete action verb — "Worked through…" / "Untangled…". |
| Constraint 2 (l.529) | "…questions you've already anticipated and documented; **genuinely** novel issues still need a person, **by design**." | Filler intensifier + "by design" epigram | Cut "genuinely"; replace "by design" with the actual reason. |
| Opening (l.499) | "orders not landing, customers in the dark, a small founding team underwater, and a reputation taking on water with it." | Four-item piling + extended water metaphor | Borderline. The "underwater / taking on water" pun reads as a deliberate human flourish — lower priority; flag, don't rush to cut. |

**Read as human voice (leave alone):** Bullet s2 ("This is the piece I'm proudest of: a support fix that reached into the physical production process, because that's where the actual problem lived") and the s5 EOR bullet's honest framing ("an evaluation-and-selection story carried through to contract, not a multi-year operation — and I frame it that way"). Specific, self-aware, in-voice.

---

## 4. Digital Spec — project entry  *(project opener + layer cards + bullets)*

| Location | Passage (quoted) | Tell | How the voice guide differs |
|---|---|---|---|
| Layer card "No AI" | "The **constraint is the feature**: every word is accountable." | Aphoristic inversion / tidy epigram | Guide: name the behaviour. "Pre-programmed means nothing it says is unaccountable." |
| Win bullet | "**Additive and robust** — Built as an overlay…" | "robust" (flagged LLM word) + abstract category label | Guide Principle 7: say what it does — "the full portfolio works untouched beneath it." |
| Constraint bullet | "…it has no live brain — **it guides, it doesn't converse**." | Parallel antithesis ("it X, it doesn't Y") + em-dash | State the limit plainly: "it guides rather than answers free-typed questions." |
| Win / description motif | "Sorts visitors **by intent, not topic**" / "curates **by tags, not lists**" | Repeated "X, not Y" structural motif across the entry | Guide: consistency is terminology, not a reused rhetorical template. Vary the construction. |
| Win / constraint labels | "Transparent **by construction**" / "Tappable-only **by design**" / "No AI, **by design**" | "[adj] by design/construction" epigram repeated 3× in one entry | Overly symmetrical labelling; each should describe the actual mechanism. |
| Description (l.562) | "**Crucially**, it has no AI behind it…" | Filler intensifier opener | Guide: cut the setup adverb; the sentence is strong without it. |

**Read as human voice (leave alone):** The "Curates by tags, not lists" *mechanism* explanation (the query-over-tagged-index detail is concrete and specific) — it's only the repeated *label* form that's the tell, not the underlying content.

---

## 5. Digital Spec — dev log  *(running build notes — lowest visibility, audit last)*

| Location | Passage (quoted) | Tell | How the voice guide differs |
|---|---|---|---|
| "Origin" note | "**The honest inversion became the point**: a constructed guide that's loud about being constructed… more transparent than most 'handcrafted' portfolios." | Tidy epigram + constructed/handcrafted antithesis | Guide: confident not absolute; the observation is good but over-polished. |
| "Never trap a busy visitor" | "**Charm for those who lean in, zero cost for those who don't.**" | Balanced parallel antithesis closer | A rhythmic sign-off, not a decision. State the behaviour. |
| "Posture-first" decision | "**Posture-first, not content-first.** The opening sorts by mindset… **not by topic**." | "X, not Y" antithesis (same motif as §4) used twice in one entry | Guide: one idea, plainly. The repetition across entries makes it conspicuous. |
| "Instant responses" | "Personality goes in **the words, not artificial latency**." | "X, not Y" antithesis | Plain: "no fake typing delays — the personality is in the wording." |
| "Tappable replies only" | "An open input promises a brain that isn't there." | Borderline — reads as voice, but adjacent to the antithesis cluster | Low priority; likely leave. |

**Read as human voice (leave alone — most of the log):** The `Issue/Fixed` entries are concrete and specific — the Ctrl+R / sessionStorage caching fix, the deeplink-anchor fix, the "Spec Lite" naming scrub, the v1-live note. These read as a real engineer's notes and should not be touched.

---

## Summary

**Worst sections (highest AI-prose density):**
1. **Front-door lane blurbs** — 6 flags; every blurb leans on an antithesis or a tricolon. Highest visibility, worst density. Prioritise.
2. **Digital Spec project entry** — 6 flags; dominated by the repeated "X, not Y" and "[adj] by design" templates and the "constraint is the feature" epigram.
3. **About Me** — 6 flags; default landing tab, so these are seen first. Mostly the "by design" / "not X but Y" / uplift-closer family.

**Already in the human's voice (leave alone):**
- About paras 1 & 4; the `implementation` and `opening`/`whoareyou` front-door text.
- Denim bullets s2 and s5 (proudest-of and the self-aware EOR framing).
- The dev log's `Issue/Fixed` entries — concrete, technical, unpolished, exactly what the About card "Build to understand" promises.

**The single recurring tell:** the balanced antithesis — "X, not Y" / "not just X, but Y" / "[adjective] by design" — used as a rhythmic default. It appears in all five sections. The voice guide's Principle 7 ("name the behaviour, not the category") and "Cut the setup" rule are the direct antidote. Fixing that one pattern would clear roughly two-thirds of the flags.

**Flag count by section (ordered by visibility):**

| # | Section | Visibility | Flags |
|---|---|---|---|
| 1 | About Me | Default landing tab | 6 |
| 2 | Front-door lane blurbs & node text | First interactive surface | 6 |
| 3 | Denim case study | Case-study opener ("proudest of") | 5 |
| 4 | Digital Spec project entry | Project opener + bullets | 6 |
| 5 | Digital Spec dev log | Build notes (last) | 5 |
| | **Total** | | **28** |

*Recommendations only — no prose was changed in this pass.*
