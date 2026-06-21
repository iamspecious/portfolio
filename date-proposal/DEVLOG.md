# DEVLOG — Date Proposal Website

> Written as decisions happen, not reconstructed after the fact.

---

## Entry 009 — Local Listings Research and Transport Step Design

**Date:** June 2026
**Status:** Research / Planning

**The local listings problem.**

The request was simple: if someone says they want to see a play in London, or a specific film in Berlin, what can we actually surface? The answer exposed a structural problem across both cinema and theatre: the venues that hold the data have deliberately not made it available to outside developers. Their entire model depends on you booking through their site.

**Cinema.**

No major cinema chain — Vue, Odeon, Cineworld, AMC, Cineplex, UCI Kinowelt — has a public developer API. TMDB, which the current cinema path uses for film discovery, is a film *metadata* database. It knows what's now playing globally. It doesn't know which cinema in Berlin is showing Project Hail Mary at 7pm on Saturday, and it never will — that's not what it is.

Google aggregates real-time showtime data directly from chains worldwide and presents it as a rich widget at the top of search results. This data is not available via any Google API. The practical conclusion: a structured Google search deep-link is the most honest and universally effective handoff that exists right now.

```
https://www.google.com/search?q=Project+Hail+Mary+showtimes+Berlin
```

That query returns a showtime widget with cinema names, times, and booking buttons sourced directly from chains — localised, current, and functional in every market. The user sees what they want to see; they just see it on Google rather than in this UI. Scraping is the alternative, but it's ToS-violating, fragile, and breaks with every site redesign.

**Theatre and events.**

Eventbrite — currently used for the activity path — skews toward community and self-organised events: workshops, meetups, food tours. It doesn't cover West End shows, the National Theatre, or professional music venues.

**Ticketmaster Discovery API** is the right tool for professional entertainment. Free tier: 5,000 calls/day. Requires only an API key, no OAuth. Supports keyword search, city or lat/long location filtering, classification filtering (Arts & Theatre / Music / Sports), and date range. Returns event name, venue, date, time, and a direct ticket link. Coverage includes Europe — a Ticketmaster search for "theatre London" returns West End productions and major venue listings.

The right split going forward:
- **Ticketmaster** → professional entertainment (theatre, concerts, sports, shows)
- **Eventbrite** → community events, workshops, meetups

Both APIs are free at the usage levels this project requires. The activity path should support both or switch to Ticketmaster as the primary source.

**Transport step design.**

Before the confirm card, a new step: *"How would you like to get there?"* Three options:

*I'll pick you up* — reveals a text input for their address. The confirm step generates two separate `.ics` downloads: the main event (venue, start time, address) and a second "collection reminder" event with a title like "Collect [Name] from [address]" timed 40 minutes before the main event. Two files, two separate invites in their calendar — cleaner than trying to encode both things in one event's description.

*I'll book a taxi* — no extra inputs. The confirm card notes that transport is arranged. Could also construct an Uber deep-link (`https://m.uber.com/ul/?drop[0][formatted_address]=...`) pre-filled with the venue address where the API has returned one. The `.ics` description notes the taxi booking.

*You'll make your own way* — nothing changes. Single `.ics` for the event only.

The two-file approach for the pickup option is the simpler implementation: the `.ics` format supports it natively, and two distinct calendar entries are clearer for the recipient than a single event with a complex description trying to encode both pieces of information.

---

## Entry 008 — Activity Type Selector: Four Paths, One Flow

**Date:** June 2026
**Status:** Built

The roadmap called for asking *what kind* of date it is before asking where. This entry documents what was built, why the step architecture had to change, and what each path looks like.

**The step ID problem.**

The original flow used numeric step IDs (`step-1`, `step-2`, etc.) with a linear `currentStep` counter and `showStep(n)` calls. That's fine for a single path, but four branching paths need something more flexible. A step number is meaningless when "step 4" could be cuisine selection on the food path or coffee style on the coffee path.

Replaced numeric IDs with semantic string IDs: `s-what`, `s-cuisine`, `s-vibe`, `s-food-venues`, `s-coffee-style`, `s-coffee-venues`, `s-activity-cat`, `s-activity-events`, `s-cinema-genre`, `s-cinema-films`, `s-datetime`, `s-confirm`. Navigation is now `goToStep(id)` — find the div with that ID, activate it. No counters, no arithmetic, no off-by-one bugs.

Each path is defined as an ordered array of step IDs in a `FLOWS` object:

```javascript
const FLOWS = {
    food:     ['s-what','s-cuisine','s-vibe','s-food-venues','s-datetime','s-confirm'],
    coffee:   ['s-what','s-coffee-style','s-coffee-venues','s-datetime','s-confirm'],
    activity: ['s-what','s-activity-cat','s-activity-events','s-confirm'],
    cinema:   ['s-what','s-cinema-genre','s-cinema-films','s-confirm'],
};
```

Progress dots render from the current flow array. Completed steps are computed by finding the current step's index in the array.

**The four paths.**

*Food* — unchanged from the original restaurant flow. Foursquare Places API, cuisine + vibe filters, four venue cards, date/time picker, OpenTable deep-link booking, .ics download.

*Coffee* — same Foursquare query, category switched to café. No vibe filter (coffee shops don't have price tiers that map to vibe in a meaningful way). No booking step — you don't book a coffee. Time slots shifted to Morning (08:30–10:30) and Afternoon (13:00–16:00) since the old Lunch/Dinner slots were wrong for a coffee date.

*Activity* — Eventbrite API (`/events/search/` with `?token=` auth, no OAuth). Category selector: Arts & Culture, Sports, Music, Classes & Workshops. Results show event name, date, venue, short description. No separate date/time step — events have their own date baked in. Goes straight to confirm.

*Cinema* — TMDB API (`/movie/now_playing`, client-side genre filtering). Genre selector: Action, Comedy, Romance, Horror, Drama. Results show film poster, title, tagline, rating, runtime. No showtimes API exists that works universally; the "Find Showtimes" button deep-links to a Google search for the film + location + "cinema showtimes". The calendar invite uses an all-day ICS event since the actual showtime isn't known.

**Time slots vary by path.**

`buildTimePickers()` checks `state.activityType` and renders appropriate slots:
- Food: Lunch 11:30–13:00, Dinner 18:30–20:30
- Coffee: Morning 08:30–10:30, Afternoon 13:00–16:00
- Activity and Cinema skip the time step entirely.

**The confirm card is fully path-aware.**

`buildConfirmCard()` checks `state.activityType` and renders different content for each path: restaurant name + booking button + .ics download for food; café name + .ics for coffee; event name + date + "Get Tickets" for activity; film poster + "Find Showtimes" for cinema. The ICS generator also branches by path — cinema generates an all-day event, everything else generates a timed event.

**API keys, demo fallbacks.**

The config panel grew from two fields (name, Foursquare key) to five: name, custom message, Foursquare key, Eventbrite key, TMDB key. Each stores to `localStorage`. Each has its own demo fallback that activates when no key is present:

- Foursquare missing → `demoByCuisine` (restaurants) or `demoCafes` (coffee)
- Eventbrite missing → `demoEventsByCat` keyed by category
- TMDB missing → `demoFilmsByGenre` keyed by genre

Demo data is contextually appropriate — demo events for Arts look different from demo events for Sports. All demos show an info banner explaining the situation.

---

## Entry 007 — Demo Mode Bug, Location Label, and Roadmap Expansion

**Date:** June 2026
**Status:** Fixed / Planning

**Bug: demo mode returned the same restaurants for every location and cuisine.**

The original fallback data was a single hardcoded array of four restaurants — La Petite Fleur, Sakura Garden, Il Cielo, The Garden Room — returned unconditionally whenever no Foursquare API key was configured. Trying London then Ghent produced identical results. Selecting Italian then Mexican produced identical results. The data wasn't wrong, it just wasn't aware of anything the user had told it.

Fixed by replacing the single array with a `demoRestaurantsByCuisine` object keyed by cuisine ID. Each of the six cuisines now maps to four contextually appropriate restaurant names. The addresses remain generic (the demo genuinely doesn't know the location) but the names at least match what was asked for. An info-styled banner now appears in demo mode explaining the situation and pointing to the config panel — honesty over pretending the results are real.

**Label change: "And where are you?" → "Where would you like to go?"**

The original wording implied the person's current location. The field is actually asking where they want to go for the date — a destination question, not a presence question. Small change, more accurate.

**Roadmap expansion: activity type selection.**

The next logical evolution of the experience is asking *what kind* of date it is before asking where. Four options, four different discovery paths:

- **Food** — existing restaurant flow, unchanged.
- **Coffee** — same Foursquare query, category switched to `café`. No booking step needed. Flow is shorter.
- **Activity** — Eventbrite has a free REST API (no OAuth) for location-based event search by category and date. Meetup.com uses GraphQL with OAuth but has broader recurring-meetup coverage. Either is a realistic implementation path.
- **Cinema** — the hardest. No universal showtimes API. Realistic approach: TMDB (free, API-key-only) for film discovery and posters, then a search deep-link to the local cinema's booking page. Same handoff model as restaurants — looks like discovery, ends at the venue's own booking flow.

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
