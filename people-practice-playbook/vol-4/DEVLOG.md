# People Practice Playbook, Vol. 4: Dev log

### 13 Nov 2026: Placing the v0.2 handoff and publishing v0.2.1

- Spec's v0.2 handoff placed as given: the v0.2 markdown, CHANGELOG, SOURCES, RESEARCH, DEVLOG and build.py. README.md and portfolio-index.json were changed by applying the supplied diff, not by overwriting the whole files, so nothing else in them moved.
- Added beyond the handoff, which didn't cover them: the Playbooks card (version, summary, "what it demonstrates", scope, roadmap, download link, dev log) and the search lexicon ("suicide prevention", "small business"). Index tags left as people-hr and research, so the lane decision above still holds.
- Network: about 30 more hosts allowed, with Spec's approval, for the international helplines, Acas, the ILO, Workplaces Respond, Find A Helpline and the v0.2 research sources, so the audit could open each one.
- Decision: v0.2 was audited before publishing, as the handoff asked. Fixes went in as v0.2.1 and the v0.2 file was renamed rather than kept, the same pattern as v0.1 and v0.1.1.
- Decision: two gaps the audit raised were left as open items rather than filled with unchecked details: Germany's ambulance number, and whether the UK abuse helpline covers Scotland, Wales and Northern Ireland.
- Card dev log toggle moved so two entries show before "show older", matching the other cards.
- Checks: tools/audit.py 0 FAIL; page rebuilt with no em dashes and no sideways scroll at phone width.

<details>
<summary>Show 6 older entries</summary>

### 12 Nov 2026: Integrity audit of v0.2 and v0.2.1

- Independent audit by a separate agent that saw only the document: PASS WITH FIXES. 143 claims; none fabricated; no wrong phone numbers among those it could check; 2 major and 12 minor findings. The audit was interrupted by a usage limit and resumed after it reset.
- Major fixes: Samaritans in Ireland no longer connects withheld numbers (changed 9 November 2026), so the Ireland row now says to show your number, and adds 999 or 112. The Germany men's line details are dated to their 2022 source, with a link to the service.
- Minor fixes: "unlikely to cause harm" rather than "safe"; check-in wording; Rivas "looked at" rather than "pooled"; Albaum "half were pilot trials"; section 5's police note; Acas's remit; UK chat hours; TelefonSeelsorge "free" removed; Find A Helpline and Befrienders counts; Men's Aid sourced to its own site.
- v0.2 was never published, so only v0.2.1 goes live. The changelog records both.

### 12 Nov 2026: v0.2, accuracy pass and wider reach

- Brief from Spec: re-check accuracy, add evidence and best practice, make it useful at any company size, and don't keep it Canada-only.
- Re-checked the core claims against their sources (Nuij, Wathen, CCOHS). One wording fix: CCOHS's police example.
- Evidence added to section 3: young people (Albaum 2025, no significant effect of safety planning alone), abuse and violence (Rivas 2016 Campbell review; Ford-Gilboe 2020 iCAN trial), and asking about suicide (Dazzi 2014, plus 9-8-8's advice). This closes the "haven't checked the abuse research" open item.
- Decision: size guidance is framed by HR capacity (no HR, one person, a function, multi-country), not headcount bands, because capacity is what changes what's realistic. Only Workplaces Respond's "about 20 or fewer" definition is used, and it's attributed.
- Decision: warning signs are framed as reasons to check in, not evidence, with a bias caveat. CCOHS's list includes cameras off in video meetings, which would land on disabled, neurodivergent and caregiving staff if used as a red flag.
- Decision: international list kept to five countries plus Find A Helpline, one crisis line and the main abuse lines each, with a men's route where the main line is for women. More countries means more numbers to keep right; the directory covers the rest.
- Resolved a tension between Acas (keep records) and the "don't write details into files" line: keep a minimal, access-limited record of requests and actions, not the details of the abuse.
- Not yet independently audited when handed over.

### 12 Nov 2026: Publishing v0.1.1

- Decision: index tags are people-hr and research, with technical-writing left off. With it, Vol. 4 took the last document slot in Digital Spec's Documentation lane and pushed cat-api-documentation out of every lane, leaving that lane four playbooks out of seven items. Vol. 4 is reached from the Playbooks tab and search instead. A one-line change if that call should flip.
- Rebased onto main after the crisis playbook rebuild (#59), which renamed crisis-management-playbook to crisis-playbook. Kept both sets of _config.yml excludes and re-applied Vol. 4's index entry, search keywords and card on top of main's versions.
- Checks: tools/audit.py 0 FAIL. tools/smoke-test.js showed 4 failures, all scroll-position checks on older Projects-tab items (optimising-cs-operations, leadership-coaching-project, niche-market-web-dev-strategy); the same failures appear on the commit before Vol. 4, so they predate it. Vol. 4 is found by search and its page loads.
- Network: about 30 Canadian crisis, government, charity and research hosts added to the environment's allowlist, with Spec's approval, so sources could be opened rather than taken from search summaries.
- Published as PR #60 and merged; the page was live about 50 seconds later.

### 12 Nov 2026: Integrity audit and v0.1.1

- Independent audit by a separate agent that saw only the playbook: PASS WITH FIXES. 86 claims; none fabricated; no wrong crisis numbers; 3 major and 11 minor findings.
- Major fixes: 9-1-1 caveat for Nunavut everywhere 9-1-1 appears; abuse resources now say who they serve, with routes for men and anyone a women's shelter doesn't fit; an unsourced coming-out claim recast as opinion.
- Minor fixes: Deaf and hard-of-hearing access to 9-8-8; 9-8-8 and Trans Lifeline police wording; pflag's FAQ still giving the old number; HR disclosure percentage; private browsing doesn't beat spyware; paper copy at work; log link.
- v0.1 was never published, so only v0.1.1 goes live. The changelog records both.

### 12 Nov 2026: Research and first draft

- Network allowlist extended twice (Canadian crisis, government, charity and research hosts) so sources could be opened rather than cited from search summaries. PubMed and PMC served a captcha and ScienceDirect a 403; neither was worked around, and free copies were used instead.
- Corrections from the original post: Crisis Services Canada's number replaced by 9-8-8; LGBT YouthLine no longer takes calls; Egale and pflag aren't general crisis lines. CCGSD and canada.ca couldn't be reached and were left out.
- Pivot: Tech Safety Canada warns that changing passwords or location settings can alert an abuser and escalate things. The digital safety checklist now starts with "Before you change anything".
- Evidence kept to what was opened: the Nuij 2021 meta-analysis for suicide prevention, with its limits, and the 2014 Wathen survey on who people tell at work. Domestic violence trial evidence is an open item, not a claim.

### 12 Nov 2026: Groundwork

- Started from a break-room conversation about supports for 2SLGBTQI+ staff, where few people knew what a safety plan was. The source is Spec's earlier community post: definition, who plans are for, a checklist, HR guidance and Canadian resources.
- Scope: shorter than Vols. 1 to 3. Written for anyone making a plan and for HR people who may be told. Coming out gets its own section because that's where the question came from.
- Decision: re-check every resource on the service's own website rather than trusting the post or third-party lists. Phone numbers are the claims most likely to hurt someone if wrong.

</details>
