# DEVLOG — Date Proposal Website

> Written as decisions happen, not reconstructed after the fact.

---

## Entry 006 — UX Fixes: Name Collection and Sticky Button

**Date:** June 2026
**Status:** Fixed

Two issues surfaced on mobile testing.

**Name collection.** The original Step 2 had two plain text inputs — name and location — which read as a form rather than an experience. Replaced with a fill-in-the-blank embedded in the headline: "I'm so glad, ______." The input is styled at the same scale as the headline text, rose-coloured when active, with just a bottom border. It reads as a sentence the user completes, not a field they fill. Location stays as a standard input below it since "Where are you?" is innocuous enough to not need disguising.

Added a recipient name field to the sender config panel (⚙). If the sender pre-fills it before sharing the link, Step 2 is replaced with a fully personalised "I'm so glad, [Name]." headline — the question never appears at all. This is the cleaner path when the sender already knows the name, which is presumably always.

**Restaurant step button.** On portrait mobile the four restaurant cards fill the viewport height, pushing the proceed button off-screen below the fold. Fixed by switching to a `position: fixed` sticky button anchored to the bottom of the viewport (`bottom: 28px + env(safe-area-inset-bottom)`). It starts invisible and slides up from below as soon as a card is selected. No scrolling required.

Secondary issue exposed by the fix: `body { overflow: hidden }` was preventing scroll on the restaurant step, so the bottom card was also partially clipped. Re-enabled `overflow-y: auto` on the body when step 5 is active, and added an 88px spacer below the restaurant grid so the last card clears the sticky button. The sticky button is the fast path; scrolling is available as a fallback.

---

## Entry 001 — The Research Question

**Date:** June 2026
**Status:** Research

The question that started this was simple: *how much of what she experienced was real?*

The original post showed someone charmed by what looked like a completely automated experience — pick a restaurant, get a booking, receive a calendar invite. The aesthetic made it feel frictionless. But several things about the description didn't add up technically.

Spent several hours mapping the full API landscape:

**Restaurant discovery** — three real options. Yelp Fusion (now Yelp Places API) was the obvious first choice, but they killed their free tier in 2025 with minimal warning and now charge ~$7.99–$14.99 per 1,000 calls. Unusable for a personal project. Google Places API has excellent data but costs real money at scale and the free credit runs out fast. **Foursquare Places API v3** has a 10,000 call/month free tier on basic endpoints, supports cuisine filtering via query parameter, and returns price tiers, ratings, photos, and addresses. The right call.

**Table booking** — this is where the illusion falls apart. OpenTable has an affiliate API but requires a 3–4 week formal approval process, and even then it's a deep-link handoff, not a true programmatic booking. Resy has no public API at all — their partner API is enterprise-only, and the third-party Apify wrapper ($3.99/booking) is ToS-violating and fragile. SevenRooms starts at $499/month. The booking industry has deliberately locked down API access to protect platform revenue. No legitimate path exists to programmatically complete a restaurant reservation without partnership agreements.

**Calendar invites** — completely trivial. RFC 5545 (iCalendar format) is plain text, universally supported, and generating an `.ics` file is 30 lines of JavaScript. Email it or download it — either works on any device.

**Conclusion:** The original site was almost certainly using Yelp or Google for discovery filtered to OpenTable-bookable restaurants, then constructing a pre-filled OpenTable deep-link. When she "confirmed", she was booking through OpenTable's UI herself. The calendar invite was probably emailed via EmailJS or similar — her email address was likely collected early in the flow under a neutral label. What looked like magic was an elegant steering mechanism.

This is worth building. Not to copy it, but to document what's real and what isn't — and build the best honest version of it.

---

## Entry 002 — Design Choices

**Date:** June 2026
**Status:** Design

The aesthetic brief from the source was clear: white background, clean bubbly font, fluid transitions. This is intentional contrast — every other tool in this portfolio is dark. The date proposal site should look completely unlike a developer tool. It should feel like something made for a person, not for a screen.

**Font: Nunito.** Rounded letterforms, strong weight range from 300 to 800, clean on white. Poppins was the other contender but Nunito's extra roundness suits the tone better.

**Colour: rose (#E8739A).** Not red (too alarming), not pink (too juvenile). A considered rose that reads as romantic without being saccharine. One accent colour across the whole experience.

**Transitions: CSS only.** A `@keyframes fadeUp` animation triggered when a step gets the `.active` class. No JavaScript animation library, no GSAP. Each step fades in from 28px below its resting position over 480ms with a cubic-bezier that decelerates fast — it feels snappy, not sluggish.

**The No button mechanic:** The standard implementation tracks mouse proximity via `mousemove` events on the document, uses `getBoundingClientRect()` to find the button's current position, and trigonometry to calculate the escape direction (angle away from cursor). The button jumps 170–280px in that direction each time. After five near-misses it fades out. On mobile, there's no `mousemove`, so the button degrades through three click states ("Are you sure?", "Really...?") before disabling itself.

**Decision: fixed positioning on first escape.** The button starts as a normal inline element. Switching to `position: fixed` immediately on the first escape attempt (recording the button's rect first, then setting fixed with matching coordinates) avoids a visible jump. The transition looks seamless because it is.

**Step progress dots.** Shown from step 2 onwards. Six dots for steps 2–7. The current step dot is rose-coloured and slightly larger. Completed steps are a muted rose-border colour. This gives the experience a sense of forward motion without adding navigation that would let someone skip the questions — which would defeat the point.

---

## Entry 003 — The Booking Gap

**Date:** June 2026
**Status:** Building

Spent time thinking about how to handle the booking step honestly. The options:

1. **Pretend it's booking.** Make the button say "Booking..." with a spinner, then show a fake "Booked!" confirmation. Intentionally deceptive, not useful as a portfolio piece.

2. **Link to the restaurant website.** If Foursquare returns a `website` field, go there. Clean and direct, but restaurant websites often don't have easy online booking.

3. **OpenTable search deep-link.** Construct `https://www.opentable.com/s/?term={name}&dateTime={date}T{time}&covers=2`. Pre-fills the search with the selected restaurant, date, time, and party size. OpenTable's search usually surfaces the right restaurant immediately. The user clicks "Reserve" on OpenTable. This is functionally what the original site was doing.

**Decision: restaurant website if available, OpenTable search as fallback.** This is the honest version of the original's approach. The README documents exactly what happens. The button says "Book the table →" which is accurate — it takes you somewhere to book, pre-filled.

The calendar invite is cleaner. Download an `.ics` file: on iOS it shows "Add to Calendar", on Android it opens the default calendar app, in Gmail/Outlook on desktop it shows Accept/Decline. Universal support, no OAuth, no permissions. The event has the restaurant name, address, and a two-hour end time calculated from the selected start time.

---

## Entry 004 — Foursquare Integration

**Date:** June 2026
**Status:** Building

The Foursquare Places API v3 request is straightforward:

```
GET https://api.foursquare.com/v3/places/search
  ?query=Italian+restaurant
  &near=London
  &limit=8
  &min_price=2
  &max_price=3
  &fields=fsq_id,name,location,rating,price,photos,categories,website
Authorization: fsq3XXXXXXXXX
```

CORS is supported natively — Foursquare explicitly allows browser-side requests to their v3 API. No proxy needed, unlike some other APIs.

Price tiers (1–4) map onto the vibe selection: Casual → 1–2, Date Night → 2–3, Fine Dining → 3–4. This filters before returning results, so the restaurant cards shown actually match the vibe the person selected. Whether Foursquare's `min_price`/`max_price` parameters are respected precisely varies by venue data quality, but the filtering is real.

Photos come back as `{ prefix, suffix }` pairs. The full URL is `{prefix}{width}x{height}{suffix}` — I'm requesting 400x240 for the card image. If the photo fails to load (network issue, bad URL), the onerror handler replaces it with the cuisine emoji. Graceful.

**Demo mode.** When no API key is configured, the tool waits 1.4 seconds (simulating a real API call) then shows four sample restaurants with generic addresses. The experience is identical — the user doesn't see an error state. This matters for the portfolio demo: someone exploring the portfolio shouldn't hit a broken state because they don't have a Foursquare key.

The config panel (⚙ gear icon, 0.22 opacity, top-right corner) is how the "sender" configures their key without it being visible to the recipient. The key saves to `localStorage`. Closing the overlay by clicking outside it or the Cancel button leaves everything in place.

---

## Entry 005 — What the original site was actually doing

**Date:** June 2026
**Status:** Research (retrospective)

Now that the build is done, it's worth writing down the conclusion more clearly.

The viral site showed her: a "No" button that ran away, preference questions, four restaurants, a booking, and a calendar invite. Each component maps to something:

| What she saw | What was actually happening |
|---|---|
| Restaurant discovery | Yelp or Google filtered to OpenTable-listed venues |
| "Only bookable restaurants shown" | Yelp `transactions` field includes `"restaurant_reservation"` if a venue is on OpenTable |
| Clicking a restaurant and "booking" | A pre-constructed OpenTable deep-link with date/time/covers pre-filled — she completed it herself |
| Calendar invite on her phone | An `.ics` file emailed to her email address, collected earlier as "where should we send details?" |

The "sinister" read isn't that he did something technically coercive. He didn't. She completed every real action herself (the booking, accepting the calendar invite). What he did was design an experience that made every decision feel inevitable — her cuisine preference surfaced exactly the restaurants he'd already vetted, the date and time were probably pre-selected to limit real choice, and the "confirmation" step was structured to feel like the app did it rather than her.

It's less about technical capability and more about information asymmetry. He knew the restaurant. She thought she chose it.

That's the part that's worth documenting: not that it's technically impossible to replicate (it mostly isn't), but that the interesting engineering was in the design of the illusion, not the code that ran underneath it.
