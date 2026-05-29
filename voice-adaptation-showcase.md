---
layout: default
title: "Voice Adaptation Showcase"
---

# Voice Adaptation Showcase

## About This Document

This document demonstrates voice adaptation as a technical writing skill. The same content — a short how-to guide for setting up two-factor authentication on a fictional app called Forma — is written three times, each version calibrated to a different company's documented voice principles.

The purpose is to show that writing in a company's voice is a research discipline, not intuition: it requires reading the source guide, identifying the principles that apply to the content type, and making deliberate choices at the sentence level.

**Sources used:**

- **Apple Style Guide** — [support.apple.com/guide/applestyleguide/welcome/web](https://support.apple.com/guide/applestyleguide/welcome/web)
- **Mailchimp Content Style Guide — Voice and Tone** — [styleguide.mailchimp.com/voice-and-tone/](https://styleguide.mailchimp.com/voice-and-tone/)
- **PostHog Handbook — Writing for PostHog** — [posthog.com/handbook/content-and-docs/writing-for-posthog](https://posthog.com/handbook/content-and-docs/writing-for-posthog)

Spec's natural writing register is Apple-influenced: second person, active voice, imperative steps, precision over warmth. Section 1 represents native range. Sections 2 and 3 show deliberate departure from it.

---

## Section 1 — Apple

**Precise, user-empathetic, no assumed knowledge, every state accounted for, calm and clear, never condescending.**

- **Source:** [Apple Style Guide](https://support.apple.com/guide/applestyleguide/welcome/web)
- **Key voice principles applied:**
  - Imperative mood for all steps — instructions begin with the action, not the context
  - Second person ("you", "your") throughout; no passive constructions
  - Every UI element named exactly as it appears onscreen, with its position stated when helpful
  - Security warnings delivered as plain information, not alarm — calm, proportionate, actionable

---

### Set up two-factor authentication in Forma

Two-factor authentication adds a second layer of security to your Forma account. After you set it up, signing in requires both your password and a verification code from your phone.

**Before you begin:** Make sure you have your phone nearby. You'll need it to complete setup and to confirm that everything is working.

**To set up two-factor authentication:**

1. Open Forma and sign in to your account.

2. Click your profile picture in the top-right corner, then click **Account Settings**.

3. Click **Security**.

4. Under Two-Factor Authentication, click **Set Up**.

5. Choose how you want to receive verification codes:
   - **Authenticator app** — An app on your phone generates a six-digit code each time you sign in. This method works without a cellular connection.
   - **Text message** — Forma sends a code to your mobile number each time you sign in.

6. Follow the onscreen instructions for the method you chose:
   - **Authenticator app:** Open your authenticator app and scan the QR code displayed in Forma.
   - **Text message:** Enter your mobile number, then click **Send Code**.

7. Enter the six-digit verification code in the field provided, then click **Verify**.

8. Forma displays a set of recovery codes.

   **Important:** Store your recovery codes in a safe place before you click **Done**. If you lose access to your phone, these codes are the only way to regain access to your account. Each code can be used only once.

9. Click **Done**.

Two-factor authentication is now active on your account. The next time you sign in, Forma will ask for your password and a verification code from your phone.

**If you don't receive a code:** Check that your phone has a signal if you're using text messages, or that your authenticator app is showing the correct time. If the problem persists, click **Resend Code**, or contact Forma Support.

---

*Apple documentation accounts for failure states without dramatising them. The "If you don't receive a code" note isn't a warning block — it's the next piece of information the reader might need, placed at the natural point where they'd need it. The hardest discipline was naming every UI element precisely ("click your profile picture in the top-right corner") rather than assuming the user will find things. Apple's voice trusts readers to succeed while quietly preparing them for the case where they don't — and it does that without a single sentence that reads as anxious.*

---

## Section 2 — Mailchimp

**Warm, human, dry humour where appropriate, plainspoken, genuine, clarity over entertainment.**

- **Source:** [Mailchimp Content Style Guide — Voice and Tone](https://styleguide.mailchimp.com/voice-and-tone/)
- **Key voice principles applied:**
  - Plainspoken — no jargon, no hyperbole, sentences that say exactly what they mean
  - Genuine — relatable framing that acknowledges the reader's situation without being preachy
  - Dry humour applied once, where it fits naturally, not engineered (the backup codes step)
  - Tone shifts at the security moment: straight-faced rather than light, because clarity matters more than entertainment

---

### How to set up two-factor authentication on Forma

Two-factor authentication means that even if someone gets hold of your password, they still can't get into your account without your phone. It takes about two minutes to turn on.

**What you'll need:** your phone, and a few minutes.

**Steps:**

1. Sign in to Forma and open the account menu in the top-right corner.

2. Go to **Account Settings**, then click **Security**.

3. Under Two-Factor Authentication, click **Set Up**.

4. Pick how you want to receive verification codes:
   - **Authenticator app** — an app on your phone generates a code whenever you need one. Works offline.
   - **Text message** — Forma sends a code to your phone number each time you sign in.

5. Complete setup for the method you chose:
   - **Authenticator app:** open your app and scan the QR code Forma shows you.
   - **Text message:** enter your phone number and click **Send Code**.

6. Enter the six-digit code and click **Verify**.

7. Forma will show you a list of recovery codes. These are how you get back into your account if you lose your phone or can't access your codes.

   Write them down. Somewhere real — not a sticky note on your monitor. A password manager works well.

8. Click **Done**.

That's it. Two-factor authentication is now turned on. The next time you sign in, Forma will ask for your password and a code from your phone.

**Didn't receive a code?** Check your signal, or try the resend option. If neither works, Forma's support team can help.

---

*The trickiest moment was the recovery code warning. Mailchimp's guide is explicit that tone should match the reader's emotional state — and at the "write your codes down" step, the reader is mildly impatient, not anxious. A full caution block would lose them. "Write them down. Somewhere real." carries the seriousness without slowing things down. The other deliberate choice was closing with "That's it" rather than a formal confirmation sentence — Mailchimp's warmth lives in exactly those small concessions to how people actually talk.*

---

## Section 3 — PostHog

**Direct, developer-first, opinionated, no filler, assumes technical competence, gets to the point fast.**

- **Source:** [PostHog Handbook — Writing for PostHog](https://posthog.com/handbook/content-and-docs/writing-for-posthog)
- **Key voice principles applied:**
  - No preamble — open with the task path, not an explanation of what 2FA is
  - Opinionated where it matters: a clear recommendation between the two methods, with a reason
  - No hand-holding on concepts developers own (passwords, QR codes, authenticator apps)
  - Flat, dense structure — no nested callouts, no reassurance padding

---

### Enable 2FA on Forma

Go to **Account Settings → Security → Two-Factor Authentication** and click **Set Up**.

**Choose your verification method:**

**Authenticator app** (recommended) — open Duo, Authy, or Google Authenticator, scan the QR code Forma shows you, then enter the six-digit code. Works offline, more reliable than SMS.

**Text message** — enter your phone number, receive a code, enter it. Fine if you don't want to install an app.

**Save your recovery codes.** Forma generates a set of single-use codes after you verify. Store them in your password manager. If you lose your phone without these, account recovery goes through support and takes time.

Click **Done**. 2FA is now active on the account. You'll see a code prompt on every subsequent login.

---

*PostHog's voice required the sharpest edit — the work is almost entirely subtraction. The first draft included an opening sentence explaining what 2FA is; it was cut because PostHog's audience already knows. The recommendation to prefer authenticator apps over SMS is deliberately opinionated: PostHog's handbook states explicitly that "it's better to be slightly wrong, or controversial, than say nothing." The `→` path notation replaces numbered navigation steps — a PostHog docs convention that signals developer familiarity without explaining itself.*
