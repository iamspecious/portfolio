# DEVLOG: Surviving Cancellation: A Crisis Playbook

> Written as decisions happen, not reconstructed after the fact.

---

## Entry 010: v1.0, moved onto the Playbooks series format

**Date:** 12 November 2026
**Status:** Done

Published as v1.0 under the title "Surviving Cancellation: A Crisis Playbook", replacing the standalone build that had been live since September 2026 as "The Small Studio Crisis Playbook". Two things prompted the change.

First, the title. "Small Studio" undersold the scope: the six incident classes cover a plain outage and a security incident as directly as a public pile-on, and the phrase made people think it was only for small studios when the audience is anyone running a product or community with no crisis procedure. Dropped it from the title and kept the "studios, open-source projects and community teams" framing in the opening section instead, where it describes the audience without gatekeeping who reads it.

Second, format. The People Practice Playbook series (now three volumes) established a house convention for this site's playbooks: markdown as the single source of truth, a build script that generates the page with stable section anchors and scrollable tables, a licence box with a download link, and a full dev log kept in this file rather than fabricated into daily entries on the portfolio card. The standalone HTML build predated that convention and had drifted from it in two ways worth naming. It was hand-maintained HTML with no markdown source, so the Parts 3 to 6 prose and the templates could only be edited by hand, inconsistently with every other playbook on the site. And it used a lot of em dashes and "not X, but Y" antithesis, the exact pattern this site's own prose audit (`AI-PROSE-AUDIT.md`) flags as an AI-writing tell, and which the newer build scripts now hard-fail on if an em dash reaches the built page. Neither was present in my own original markdown drafts; both were introduced when the content was first turned into a standalone page. Rebuilding from the original wording, restructured into the house's numbered-section convention and run through the same build.py pattern as the People Practice volumes, fixed both at once.

Kept two deliberate departures from the People Practice template rather than forcing a false match: the module headings in sections 2 to 4 keep their numeric prefixes (2.1, 3.5, 4.3) because the classification table in section 2.2 routes readers to a specific module by number, which none of the People Practice volumes need to do; and the one-page companion stays a hand-written HTML file rather than a second markdown-to-build.py pipeline, because its print layout and its deliberately different editorial rules (Entry 007) don't map onto the main template.

Reused the same roundup of tags as before (`technical-writing`, `community`, `support-ops`); no new taxonomy terms needed.

<details>
<summary>Show 9 older entries</summary>

## Entry 009: Deliberate exclusions

**Date:** September 2026
**Status:** Scoping

No severity matrix, for the reason in Entry 005. No jurisdiction-specific legal detail: consumer and employment law questions are flagged, not answered, because getting this wrong in a document aimed at multiple jurisdictions is worse than not addressing it. No naming of individuals in any case file beyond what's already public and organisational. No advice on the employment decision itself, only on how to communicate around one.

---

## Entry 008: Licensing

**Date:** September 2026
**Status:** Decision

Three iterations. First: CC BY 4.0 for the document, CC0 for the templates, so people could paste templates without an attribution obligation mid-crisis. Second: moved to uniform CC BY 4.0, since a split licence creates exactly the kind of small inconsistency that gets a cautious lawyer to tell a team not to use the document at all, and a credit or link-back is a reasonable minimum ask. Third: expanded into a full "using this" section, then trimmed it back off the one-pager.

Made four things explicit in the final terms, because CC BY alone doesn't answer them and the ambiguity is what causes hesitation: internal credit is fine and doesn't have to be public; never put a licence notice in a live crisis post, credit belongs in the internal document the template was pasted into; attribution can wait until things calm down; cost is never the blocker, so small teams, volunteers and unfunded communities should use it and not think about it again. Plus a stated norm, not a requirement: if you adapt it, keep a link to the original.

Known trade-off, accepted deliberately: CC BY permits commercial use, so a consultancy can build paid work on this and satisfy the licence with a back-matter credit. The version people encounter later may not be mine. The alternative, CC BY-NC, blocks any use a lawyer might call commercial, which in practice means some studios won't touch it at all. Reach was judged more valuable than control.

---

## Entry 007: The one-page companion

**Date:** September 2026
**Status:** Design

Built the one-page card as a separate, short artefact rather than trusting people to find section 2 inside the full document. Section 2 was already designed to be self-sufficient, so extracting it cost nothing and produces the thing people actually reach for: something printable, pinnable, and survivable when Discord itself is unusable. Contents: first 60 minutes, classification table, statement order, do-not list, hours 1 to 24, roles card. Nothing requiring the full playbook first.

Pulled the URL out of the card's footer. It originally linked back to the full playbook; changed to "see the accompanying playbook" because a team that rewrites the playbook into their own internal doc and keeps the card would otherwise have a hard link pointing at something that's no longer their source of truth. The softer phrasing stays true whatever they do with it.

Dropped the licence blurb from the card entirely. The "cost is never a blocker" framing belongs where someone is deciding whether to adopt the thing, not on the card they're reading while their community is on fire. Attribution stays in the byline; space on a one-pager is the scarcest resource in the whole project.

Standing rule for maintenance: every future addition to the card costs it the property that makes it work. New material goes in the playbook, not the card.

---

## Entry 006: Structural revision, v1 to v2 (standalone build)

**Date:** September 2026
**Status:** Pivot

v1 to v2 of the original standalone build was a full restructure, not an edit. v1 ordered triage, then modules, then failure modes, then cases, then templates, then after: reasoning-first with action distributed throughout. Correct as an argument, wrong as a tool, because a reader in crisis had to understand the framework before they could act on it.

v2 reordered to pure action first, then modules (checklist, then why), then templates, then the evidence, failure modes, cases and review, with the last group explicitly labelled as not needed to act. Every module opens with a tickable Do block and puts the Why underneath. This is the single change that most improves usability, and the one most likely to get undone by a well-meaning editor who thinks the reasoning should come first.

Cut from v2: a "handing this to a team mid-crisis" note and its accompanying covering-note template. Both were artefacts of an earlier framing where the document was something you'd hand over personally. Once it became a published open resource, they were dead weight on the most valuable real estate in the file.

---

## Entry 005: Research pass two, structure

**Date:** September 2026
**Status:** Research

This is the pass that changed the document most, prompted by a specific question: what does best-in-class crisis documentation actually look like, structurally?

CDC Crisis and Emergency Risk Communication (CERC): the gold standard framework for emergency communication, developed for public health and widely adopted beyond it. Six principles: be first, be right, be credible, express empathy, promote action, show respect. Two pieces ended up load-bearing: "be right" (give facts in increments; say what you know when you know it, what you don't know, and when you expect to know more) validated the "what we know / what we don't know" structure already in the first-statement template. "Be credible" (uncertainty is worse than not knowing, because rumour does more damage than hard truth) is the sharpest available argument against the instinct to stay quiet until you have a complete picture. "Promote action" provided the evidential basis for something the first draft asserted without support: that instructing information outranks the apology, because giving people something specific to do restores a sense of control.

Degani & Wiener, *Cockpit Checklists: Concepts, Design, and Use* (Human Factors, 1993), and the earlier NASA normal-checklist report: the foundational human-factors research on procedural documents used under stress, and the authors state explicitly that the principles transfer to other high-risk domains. The finding that changed the document: limited working memory is the binding constraint on human performance, and the mitigation is chunking, grouping items into defined units around a common factor, so a long procedure becomes a small number of retrievable groups rather than one undifferentiated list. This directly caused the restructure into what is now sections 2 and 3: a short action section plus discrete modules rather than one continuous document. A section states this openly, so anyone adapting the playbook understands why not to flatten it back into prose.

PagerDuty incident response documentation and adjacent runbook practice: a runbook nobody can find during an incident may as well not exist, and conflicting documents breed hesitation; each procedure needs one definitive source. Applied both to the playbook itself (one file, no chasing cross-references) and to the guidance it gives (single source-of-truth channel). And: start without severity tiers, just establish whether something is an incident, get roles and triggers working, add sophistication later. This is why the playbook deliberately has no severity matrix, and says so.

---

## Entry 004: Same outcome, different route

**Date:** September 2026
**Status:** Design

Direct requirement: be honest that different incidents need different handling even when the visible outcome looks identical. Built around five axes on which the classes genuinely diverge: speech constraints, timelines, reversibility, evidentiary bar, and who can credibly speak.

The sharpest version of the point, worth keeping if the section ever gets cut for length: applying security-incident transparency instincts to a conduct incident prejudices the process and creates liability; applying conduct-incident caution to a security incident looks like a cover-up. Same instinct, opposite outcomes, depending only on the class.

---

## Entry 003: The incident class taxonomy

**Date:** September 2026
**Status:** Design

Classified by class, not severity. Most incident response frameworks sort by severity (SEV1/SEV2, P0/P1). Correct for operational incidents, wrong for this domain, because severity tells you how hard to run but not what you're allowed to say, and speech constraints are the thing that actually differs.

Six classes: Product failure, Security, Commercial, Conduct, Governance, Community conflict. They map loosely onto SCCT's clusters but are cut for this domain specifically, because "accidental vs intentional" doesn't distinguish a pricing backlash from a code sabotage even though the required responses are almost opposite.

Each class carries: the real question underneath, which module to open, and who must speak. That last column does more work than it looks like it does: it's the thing that stops a community manager being handed a governance failure.

Three rules attached to the taxonomy, all of which came out of thinking about how these actually unfold: classes compound (silence turns a security incident into a governance one in about seventy-two hours); if leadership knew, it's already a governance incident regardless of origin; when two classes run at once, split them publicly and say you're splitting them.

---

## Entry 002: Research pass one, substance

**Date:** September 2026
**Status:** Research

Goal: ground the content in something other than opinion.

Coombs' Situational Crisis Communication Theory (2007, and the later Handbook chapter) is the most replicated framework in crisis communications. Used for two things: the finding that preventable crises damage reputation more than any other type, with rebuild strategies (apology, compensation) producing the strongest recovery for them, is why the playbook pushes hard against deny and diminish responses. And Coombs' own note that a common misapplication of SCCT is skipping the "ethical base response" (instructing and adjusting information) in favour of reputational strategy became the load-bearing justification for the ordering of the first statement.

NIST SP 800-61 Revision 3 (April 2025): checked and confirmed it supersedes r2 entirely and reorganises around the Cybersecurity Framework 2.0 functions. Used lightly: the playbook doesn't ask anyone to implement a NIST profile mid-crisis, but it gives the security module defensible structure and a citation that isn't invented on the spot. Its shift to treating improvement as continuous rather than post-incident got reused in the post-incident review.

ISO/IEC 29147:2018's seven-day acknowledgement standard, left unqualified, would give a panicking team permission to sit on a live incident for a week. It's the floor for an inbound private vulnerability report, not a benchmark for a public incident already in progress. Flagged the distinction explicitly rather than just citing the number.

Chose node-ipc/peacenotwar (2022) as the primary supply-chain case because it isolates exactly the mechanism that matters: the ecosystem judged the act, not the stated motive, and the trust consequence attached to the maintainer's future access rather than to the specific package. That's the transferable lesson for any modding or plugin ecosystem, and it directly undercuts the "it only targeted bad actors" defence that surfaces in nearly every incident of this type.

Chose Helldivers 2 / PSN account linking (2024) because it does three jobs at once: it demonstrates what happens with no comms discipline (community staff publicly directing players to review-bomb), it quantifies the commercial damage (369,000+ negative reviews at peak), and it demonstrates recovery (reversal within days, 200,000+ positive reviews in one day, the CEO accepting the criticism as warranted after a formal redirect had failed). The last part is the most useful and least obvious: the formal acknowledgement failed and the named person accepting blame worked. That's a clean, evidenced argument for why the principal has to speak.

---

## Entry 001: What it is and why

**Date:** September 2026
**Status:** Scoping

Started from a practitioner discussion about a community crisis in a games modding ecosystem: the kind of situation where a technical incident, an employment question and a community trust collapse all arrive at once and land on whoever happens to run the Discord.

Decided to generalise completely. Nothing in the playbook references any live or identifiable situation. Two reasons, one practical and one ethical. Practical: a document that reads as a diagnosis of a specific team's failure gets defensive-read and binned. A document that reads as generic guidance which happens to arrive on a useful day gets used. Ethical: writing about a live incident involving identifiable individuals turns a resource into a commentary. That's a different artefact with different obligations, and it isn't this one.

Scoped the whole document to communications, coordination and moderation only, stated on the first page and repeated in the footer. No legal strategy, no technical remediation, no employment decisions; only how to talk about those things and who should own them. This was the single most important structural choice. A scoped document can be accepted by a nervous team without them feeling they're accepting a verdict on their legal position or their staffing.

Target audience: teams of roughly five to twenty-five with no prepared crisis procedure. Studios, open-source maintainers, community teams, volunteer moderator groups.

</details>
