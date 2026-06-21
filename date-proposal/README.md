# Date Proposal Website

A recreation and technical deconstruction of a viral moment: a developer who built a website to ask someone out on a date — complete with a "No" button that flees the cursor, a preference wizard, live discovery across four date types, optional booking, and a calendar invite. The project started as a research question — *how much of this is technically possible, and how much is a well-designed illusion?* — and became a working tool.

---

## Introduction

The original post showed her being charmed by what looked like magic: a clean, white webpage asked if she'd go on a date, her preferences guided the experience, and somehow a restaurant was booked and a calendar invite landed on her phone without her really doing anything.

The interesting part isn't the UI — the running No button is about 20 lines of JavaScript. The interesting part is the booking. There is no public API that lets a third party programmatically book a restaurant table. Not OpenTable, not Resy, not Tock. All of them are either gated behind formal partnership agreements or don't exist at all for outside developers.

What the original site almost certainly did was construct a deep-link to OpenTable with the restaurant, date, time, and party size pre-filled — so when she clicked "confirm", she was booking it herself on OpenTable's UI, not through his code. The site made her feel like she was choosing while actually steering every outcome.

This project builds the full experience, documents the API landscape honestly, and calls out the gap between what it looks like and what it actually does.

---

## What it does

- **The question** — "Will you go on a date with me?" with a Yes button and a No button that runs away from the cursor. After five near-misses the No button disappears.
- **Activity type** — four paths: Get some food, Go for a coffee, Do an activity, Go to the cinema.
- **Preference collection** — name, location, then path-specific preferences (cuisine + vibe / coffee style / event category / film genre).
- **Discovery** — four APIs, one per path:
  - *Food* — Foursquare Places API (free tier, 10,000 calls/month), filtered by cuisine and price tier.
  - *Coffee* — same Foursquare query, category switched to café. No price tier filter.
  - *Activity* — Eventbrite API (free, no OAuth), filtered by category (Arts, Sports, Music, Classes) and location.
  - *Cinema* — TMDB API (free, API key only), now-playing films filtered client-side by genre.
- **Venue/event selection** — four cards with name, rating, address, and photo where available.
- **Date and time** — date picker (minimum: tomorrow) and time slots appropriate to the date type. Food: Lunch / Dinner. Coffee: Morning / Afternoon. Activity and Cinema skip this step — events have their own date, cinema showtimes are on the cinema's site.
- **Booking / handoff**:
  - *Food* — opens the restaurant's website if available, otherwise an OpenTable search pre-filled with name, date, time, and party size.
  - *Coffee* — no booking. Calendar invite only.
  - *Activity* — links to the event's Eventbrite page.
  - *Cinema* — Google search deep-link for the film + location + "cinema showtimes".
- **Calendar invite** — generates and downloads an `.ics` file (iCalendar format) that opens natively in Google Calendar, Apple Calendar, and Outlook on any device. Cinema generates an all-day event; all other paths generate timed events with a two-hour end time.

---

## Wins

**The No button** is the mechanic everyone notices. Mouse proximity detection via `mousemove` events, `getBoundingClientRect()` for position, basic trigonometry for the escape direction. Mobile fallback degrades the button through three taps before it disables itself.

**Four paths, one architecture.** Each activity type follows an ordered list of step IDs defined in a `FLOWS` object. Navigation is `goToStep(id)` — no numeric counters, no arithmetic, no off-by-one bugs. Progress dots compute dynamically from the current path.

**The transitions** are pure CSS — a `@keyframes fadeUp` animation on each step's `.active` class. No library, no framework. Clean enough that it actually feels like a product.

**The booking gap is documented, not hidden.** The project explains exactly why true programmatic booking doesn't exist publicly, and every handoff button is honest about what it does.

**Calendar generation is 30 lines of JavaScript.** RFC 5545 (iCalendar) is a plain-text format. Universal support across iOS, Android, Outlook, and Google Calendar.

**Three APIs, three demo fallbacks.** All demo data is contextually appropriate — demo cafés for coffee, demo events keyed by category, demo films keyed by genre. No broken states for visitors without API keys.

---

## Constraints

**Programmatic table booking doesn't exist via a public API.** Every path to real booking requires either a formal partnership agreement (OpenTable: 3–4 week approval; Resy: enterprise-only), ToS-violating third-party scrapers ($3.99/booking via Apify's Resy wrapper, fragile and undocumented), or paying $499/month for SevenRooms. The "booking" step is a deep-link handoff — not a technical failure, but an honest limitation.

**No cinema showtimes API.** TMDB covers film metadata and posters. Vue, Odeon, Cineworld, and Picturehouse don't have public developer APIs. The "Find Showtimes" button deep-links to a Google search. It works. It's not elegant.

**Three API keys required for full live data.** Foursquare (restaurants and cafés), Eventbrite (events), TMDB (films). All free tiers. The config panel (⚙ gear icon) handles all three — each saves to `localStorage`. Demo mode covers all paths when no keys are present.

**No email sending.** The calendar invite downloads as an `.ics` file rather than being emailed directly. Adding EmailJS would close this gap.

**Desktop-first mechanic.** The running No button works via `mousemove` events, which don't fire on touch devices. Mobile gets a degrading-text fallback instead.

---

## Roadmap

1. **EmailJS integration** — collect an email address during the flow and send the `.ics` as an attachment automatically on confirmation. Closes the gap between downloading and receiving. Free tier: 200 emails/month.
2. **Sender personalisation mode** — a `?setup` URL parameter opens an extended config: custom opening message, a pre-selected restaurant to steer the choice, a locked-in date. Documents the "sinister" version explicitly as a design option.
3. **OpenTable affiliate integration** — currently a search deep-link. With OpenTable's affiliate approval (3–4 week process), becomes a cleaner availability-surfacing integration with direct booking links per restaurant.

---

## Running it

Static HTML — open `index.html` in any browser. No build step, no dependencies, no backend.

To enable live data, click the ⚙ gear icon on the page and enter the relevant API keys — each saves to `localStorage` and never leaves the browser:

- **Foursquare** (food and coffee paths) — free account at [foursquare.com/developers](https://foursquare.com/developers)
- **Eventbrite** (activity path) — free account at [eventbrite.com/platform](https://www.eventbrite.com/platform/api)
- **TMDB** (cinema path) — free account at [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

All requests are made directly from the browser. No proxy, no backend.
