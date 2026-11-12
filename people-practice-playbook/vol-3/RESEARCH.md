# People Practice Playbook, Vol. 3: Research notes

Working notes from the research behind Vol. 3, gathered 11 to 12 November 2026. Not reader-facing. The published text uses only the sources in vol3-SOURCES.md.

## What the AI companies recommend

- **Anthropic (Claude Code best practices):** most failures come from missing information, no way for the AI to check its work, or rules a prompt can't guarantee. Give it a pass/fail check, ask for evidence, enforce zero-exception rules through settings, let it interview you until it can write a spec, and start fresh after two failed corrections. Note: the current page doesn't say "explore, plan, code" in those words, so plan-first is credited to OpenAI in the playbook.
- **OpenAI (Codex best practices, now at learn.chatgpt.com):** plan first when a task is complex or unclear; have the agent interview you; ask it to write tests, run checks and review the result.
- **Google Cloud (Oct 2025):** pick the right tool, document early, make and approve a plan, brief the AI like a new teammate, keep a context file between sessions.
- **GitHub Spec Kit:** spec, then plan, then tasks, then implement. GitHub's own site calls it an "extensible, intent-driven harness". A secondary write-up called it an "experiment"; that isn't confirmed, so it isn't used.

## Main voices

- **Martin Fowler:** vibe coding means not looking at the code; reviewing it is a different practice. Vibe coding suits disposable software.
- **Simon Willison:** fine for personal tools, "grossly irresponsible" for software other people use. Humans stay accountable. Admits the line is blurring in his own work.
- **Thoughtworks, The VibeSec Reckoning:** the AI pushed insecure defaults (public link storage, over-broad service account access) on the engineers scaling a citizen builder's prototype; a human question caught both. Rolled out to 150 users. The article cites many third-party statistics; none are reused without checking.
- **Birgitta Böckeler (Thoughtworks, QCon London 2026, via DevClass):** AI is useful enough to pull people out of the loop; judge risk by probability, impact and detectability. Not used in the published text; candidate for a later version.

## Evidence

- **METR 2025 RCT (arXiv 2507.09089):** 16 experienced developers, 246 tasks, ~19% longer with AI, believed ~20% faster. Small, expert, early-2025 tools.
- **METR Feb 2026 update:** 57 developers, 800+ tasks. Returning developers about 18% faster, new about 4% faster, both with wide uncertainty. Selection effects (some declined, 30 to 50% held back tasks). METR calls it "only very weak evidence".
- **Veracode 2026:** security pass rate about 56%, coding models no better than general ones. Vendor press release.
- **IBM 2026:** global average breach $4.99M, 247 days to find and contain. Sample reported elsewhere as 600+ organisations; not checked directly.

## Researched but left out (legal detail is out of scope for the series)

- US employer liability for vendor AI tools; NYC Local Law 144 bias audits; California automated-decision rules from 1 January 2027 (National Law Review, Sept 2026).
- EU AI Act: employment AI is high-risk; Digital Omnibus moved those duties to 2 December 2027 (Gibson Dunn). The audit noted the Omnibus came into force on 27 July 2026.
- Colorado replaced its 2024 AI Act in 2026 (flagged by the audit).
- GDPR Article 25, data protection by design and by default (EDPB Guidelines 4/2019). GDPR Article 33: the employer, not the vendor, notifies the regulator after a breach.
- The US EEOC's current position on AI hiring tools: not found.

## Framing decision

Using AI to write an HR system isn't the same as the system using AI. The heavier rules bite when the finished system screens, ranks or decides about people. The playbook keeps to practice and tells readers to check locally.
