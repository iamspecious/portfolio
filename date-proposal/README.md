# Date Proposal Website

A recreation and technical deconstruction of a viral moment: a developer who built a website to ask someone out on a date — complete with a "No" button that flees the cursor, a preference wizard, live restaurant discovery, table booking, and a calendar invite sent to her phone. The project started as a research question — *how much of this is technically possible, and how much is a well-designed illusion?* — and became a working tool.

---

## Introduction

The original post showed her being charmed by what looked like magic: a clean, white webpage asked if she'd go on a date, her preferences guided the experience, and somehow a restaurant was booked and a calendar invite landed on her phone without her really doing anything.

The interesting part isn't the UI — the running No button is about 20 lines of JavaScript. The interesting part is the booking. There is no public API that lets a third party programmatically book a restaurant table. Not OpenTable, not Resy, not Tock. All of them are either gated behind formal partnership agreements or don't exist at all for outside developers.

What the original site almost certainly did was construct a deep-link to OpenTable with the restaurant, date, time, and party size pre-filled — so when she clicked "confirm", she was booking it herself on OpenTable's UI, not through his code. The site made her feel like she was choosing while actually steering every outcome.

This project builds the full experience, documents the API landscape honestly, and calls out the gap between what it looks like and what it actually does.

---

## What it does

- **The question** — "Will you go on a date with me?" with a Yes button and a No button that runs away from the cursor. After five near-misses the No button disappears.
- **Preference collection** — name, location, cuisine type (Italian / Japanese / French / Mexican / Indian / American), and vibe (Casual / Date Night / Fine Dining).
- **Restaurant discovery** — Foursquare Places API (free tier, 10,000 calls/month), filtered by cuisine and price tier. Falls back to sample restaurants if no API key is configured.
- **Restaurant selection** — four cards with name, rating, price level, address, and photo where available.
- **Date and time** — date picker (minimum: tomorrow) and pre-set time slots for lunch and dinner.
- **Booking** — opens the restaurant's website if available, otherwise falls back to an OpenTable search pre-filled with the restaurant name, date, time, and party size of two.
- **Calendar invite** — generates and downloads an `.ics` file (iCalendar format) that opens natively in Google Calendar, Apple Calendar, and Outlook on any device.

---

## Wins

**The No button** is the mechanic everyone notices. Mouse proximity detection via `mousemove` events, `getBoundingClientRect()` for position, basic trigonometry for the escape direction. Mobile fallback degrades the button through three clicks before it disables itself.

**The transitions** are pure CSS — a `@keyframes fadeUp` animation on each step's `.active` class. No library, no framework. Clean enough that it actually feels like a product.

**The booking gap is documented, not hidden.** The project explains exactly why true programmatic booking doesn't exist publicly, and the "Book the table" button is honest about what it does: it pre-fills OpenTable's search with the selected restaurant, date, and time, then hands off to OpenTable. It looks like booking. It's a very good handoff.

**Calendar generation is 30 lines of JavaScript.** RFC 5545 (iCalendar) is a plain-text format. Universal support across iOS, Android, Outlook, and Google Calendar. Accepted on the device, it triggers reminders like any other event.

**Foursquare over Yelp.** Yelp eliminated their free tier in 2025 with minimal notice. Foursquare's basic tier gives 10,000 calls/month for free, which is more than adequate for a personal project.

---

## Constraints

**Programmatic table booking doesn't exist via a public API.** Every path to real booking requires either a formal partnership agreement (OpenTable: 3–4 week approval; Resy: enterprise-only), ToS-violating third-party scrapers ($3.99/booking via Apify's Resy wrapper, fragile and undocumented), or paying $499/month for SevenRooms. The "booking" step in this project is a deep-link handoff — not a technical failure, but an honest limitation of what's publicly available to developers.

**Foursquare API key required for live data.** The tool ships with demo restaurants when no key is present. Real discovery requires a (free) Foursquare developer account. The config panel (⚙ gear icon) handles this without breaking the experience for the intended recipient.

**No email sending.** The calendar invite downloads as an `.ics` file rather than being emailed directly. The original site likely used the person's email address (collected early in the flow) to send the `.ics` as an attachment. Adding EmailJS would close this gap.

**Desktop-first mechanic.** The running No button works via `mousemove` events, which don't fire on touch devices. Mobile gets a degrading-text fallback instead.

---

## Roadmap

1. **EmailJS integration** — collect an email address during the flow and send the `.ics` as an attachment automatically on confirmation. Closes the gap between downloading and receiving. Free tier: 200 emails/month.
2. **Sender personalisation mode** — a `?setup` URL parameter opens an extended config: custom opening message, a pre-selected restaurant to steer the choice, a locked-in date. Documents the "sinister" version explicitly as a design option.
3. **OpenTable affiliate integration** — currently a search deep-link. With OpenTable's affiliate approval (3–4 week process), becomes a cleaner availability-surfacing integration with direct booking links per restaurant.

---

## Running it

Static HTML — open `index.html` in any browser. No build step, no dependencies, no backend.

To enable live restaurant data:
1. Create a free account at [foursquare.com/developers](https://foursquare.com/developers)
2. Generate an API key
3. Click the ⚙ gear icon on the page and enter the key — it saves to `localStorage`

The key never leaves the browser. All Foursquare requests are made directly from the client.
