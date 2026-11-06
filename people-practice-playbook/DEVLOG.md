# DEVLOG: People Practice Playbook, Vol. 1

> Written as decisions happen, not reconstructed after the fact.

---

## Entry 001: What it is and why

**Date:** November 2026
**Status:** Scoping

An open, free, living playbook on job architecture and levelling, published under CC BY-SA 4.0. It sits next to the Small Studio Crisis Playbook on this site and works the same way: open licence, cited sources, and built to be taken and adapted.

The gap it fills: most published material on levelling gives you a finished ladder with the working removed. You get the engineering framework from a big tech company, but not how they worked out what was wrong, what they did first, or how they got managers to use it. This playbook publishes the process instead. It starts from one idea, that you should diagnose which problem you've got before you design anything, because the most common failure I see is an adoption problem being treated as a writing problem.

---

## Entry 002: Key decisions

**Date:** November 2026
**Status:** Design

### Decision 1: Scoped to companies of 50 to 500 people

Big enough to need levels, too small to have a dedicated reward team or a consultant on retainer. A lot of what's published comes from companies with conditions this group doesn't have, so the playbook says when a source comes from a much bigger or different setting.

### Decision 2: EU law and pay left out on purpose

Pay bands, benchmarking and anything specific to one country's law are out of Vol. 1. The aim is that a manager, an HR generalist or someone in L&D can pick this up as a starting point without it needing legal review first. Where levelling bumps into pay or law, the text says so and stops there.

### Decision 3: Examples throughout, not scripts

Every section has an illustrative example, clearly marked as made up, and the conversation section shows the difference between a verdict and a conversation about the work. None of it is a script. Scripts get read out word for word, and a levelling conversation read from a script is exactly the kind that goes wrong.

### Decision 4: Written for anyone with a stake in levelling, not just HR

The reader might be in HR or L&D, a function leader, a manager who's ended up holding it, or someone about to be levelled. Section 5 sets out what each of those people is best placed to do, rather than assuming HR does it alone.

---

## Entry 003: The evidence standard

**Date:** November 2026
**Status:** Research

Every claim in the playbook is one of three things, and the text makes it clear which:

- **Research**, cited.
- **Published practice**, cited.
- **My view**, said in plain words ("I'd", "as I see it", "my read is").

"Practitioner consensus" is only used where there are published sources behind it. It doesn't get to mean "what people say at conferences".

Citations were checked back to the original sources, not to the summaries that quote them. Where a secondhand summary had overstated what a study found, the claim was corrected to match the original. Where only a summary or an abstract was available, the playbook links to that and says so.

---

## Entry 004: Where the evidence turned out different from the original brief

**Date:** November 2026
**Status:** Research

Three places where the research didn't say what the brief expected.

### Adoption is better researched than expected

The brief assumed adoption would be mostly practitioner opinion. It isn't. It just isn't studied under the name "career ladders". Researchers call it HR implementation: the gap between the policy as designed and what line managers actually do with it. That literature (Purcell and Hutchinson, Bos-Nehles and colleagues, Trullen and colleagues) turned section 6 from the thinnest section into one of the better-supported ones.

### Locke and Latham were the wrong citation for checklist distortion

The brief cited Locke and Latham for the idea that a ladder used as a checklist distorts behaviour. That's backwards: Locke and Latham built much of goal-setting theory and defend it. The argument that specific goals bring side effects, like narrowed focus, comes from Ordóñez and colleagues ("Goals Gone Wild", 2009). The playbook now cites Ordóñez and colleagues for the claim, cites Locke and Latham's reply, and says plainly that the debate is contested.

### Rating-scale evidence is mixed, not simply weak

The brief said the evidence on competency formats was weak. It's more accurate to say it's mixed. One 1975 study found behaviourally anchored scales somewhat better on most measures, another found they cut halo error but not leniency, and a third found them no better than simple global ratings. Section 3 reports all three rather than collapsing them into "weak".

---

## Entry 005: Publishing it on the portfolio

**Date:** 2026-11-06
**Status:** Publishing

The markdown file is the single source of truth. `build.py` converts it to `index.html` with pandoc, with smart punctuation switched off so the text isn't altered, and the same file is offered as a download so people can adapt it under the licence.

- **Stable anchors.** Sections are `#section-1` to `#section-10`. Subheadings are `#section-N-<heading>`, so the "An example" heading in section 6 is `#section-6-an-example` and stays put even if other sections gain subheadings.
- **Tables scroll on a phone.** All 15 tables sit in a scrolling wrapper. On narrow screens the columns keep a readable width and the table scrolls sideways instead of squashing.
- **Links untouched.** Every source URL in the markdown is checked against the built page.
- **Corrections route.** The placeholder sentence in section 1 now links to the repo for pull requests and to my email.
- **Version and changelog.** The page header shows the version and date and links to the changelog in section 10, which stays the single record of versions.
- **No em dashes.** The build fails if one appears anywhere on the page.

---

## Entry 006: Open items for v0.2

**Date:** 2026-11-06
**Status:** Planning

From the "Open items" list in section 10:

1. Look properly for research on levelling and LGBTQ+ people, neurodivergent people, and people working across countries and cultures.
2. Read the original 1986 Allen and Katz paper on dual ladders, rather than relying on course notes and a later working paper.
3. Check whether the UK government framework has moved to a new address.
4. Collect more accounts from the people being levelled, not just the people building ladders.

---

## Entry 007: People Practice Playbook v0.1.1, link fixes

**Date:** 6 November 2026
**Status:** Patch

### What and why

Readers would hit dead ends checking sources: links that went nowhere, came back forbidden, timed out, or only showed an abstract. A playbook that asks people to check its evidence has to let them actually reach it.

### What changed

- Eleven sources now link by DOI. A DOI is a permanent address that always finds the paper, even when sites move.
- Two sources also link a legal free copy: the authors' NBER working paper for Guiso, Sapienza and Zingales, and the accepted manuscript in the Universidad Carlos III repository for Trullen et al.
- The technician rating scales study is now named properly (Gomez-Mejia, 1988) instead of being linked as "abstract".
- The HR system strength line was reworded. The old version cited a conference summary that no longer exists and said the idea was "under-tested". It now cites the original paper and the authors' 2016 follow-up, and says what that follow-up actually says.
- Version moved to 0.1.1: fixes only, no recommendations changed.

### Key decisions

- Free where it's legal. Where a paper is behind a paywall and no legal free copy exists, it links by DOI only. Free copies on random third-party sites were left out. They're often unofficial and tend to disappear.
- DOI first, free copy second. The DOI always identifies the exact published paper. The free copy can be an earlier or pre-publication version.

### Evidence standard

Every new DOI was checked against the publisher's record or an indexing service that lists it. No citation was swapped for a different paper.

### Open items

- These stay paywalled with no legal free copy found: Kluger and DeNisi 1996, Gomez-Mejia 1988, Roch et al. 2012, Bowen and Ostroff 2004, Ostroff and Bowen 2016, Howell et al. 2012. Check again at the six-month review.
- The other non-DOI links (university repositories, practitioner sites, frameworks) weren't flagged this pass. Do a full link check at the next review.
