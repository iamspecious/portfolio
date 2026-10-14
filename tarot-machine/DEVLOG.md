# DEVLOG — Tarot Machine

> Written as decisions happen, not reconstructed after the fact.

---

## Entry 001 — Choosing the hardware and setting up the build

**Date:** 2026-10-06  
**Status:** Setup

Hardware ordered, development environment set up. No code on the device yet. These are the decisions made so far.

### Decision 1: StickS3 over the StickC Plus2

The older StickC Plus2 was the other option. I picked the StickS3 because it has a real audio codec and speaker instead of a buzzer. Voice is on the roadmap, and a buzzer can't do it. The StickS3 also has more memory, which matters once card images go on the device.

### Decision 2: Buying from a German retailer

Bought from OpenELAB, which ships from a warehouse in Munich. That avoids customs and long shipping. The kit ships with no cable, so I sourced a USB-C data cable separately.

### Decision 3: Parts list kept to the stick and a cable

No soldering, no sensors, no add-on kits. The StickS3 already has a screen, speaker, buttons and a motion sensor.

### Decision 4: Short sessions, each with a visible result

The build is split into short sessions. Each one ends with something I can see on the device. Feature ideas go into an ideas file so they don't derail the current step.

### Decision 5: Writing the card meanings myself, in a format code can read

I wrote all 78 card meanings myself, upright and reversed. They're in a pipe-delimited `cards.txt`, so they can be converted into code automatically rather than by hand.

### Decision 6: One sketch folder per version

The Arduino sketchbook has one project folder, with a separate sketch folder for each version: `tarot_v1`, `tarot_v2`, and so on. If something breaks, there's always a working version to fall back to.

---

## Entry 002 — Converting the card list into code

**Date:** 2026-10-07  
**Status:** Building

**Goal:** turn my 78 hand-written card meanings into a file the Arduino sketch can use, and learn how the conversion works instead of having it done for me.

### What I built

- `convert.py`, a Python script that reads `cards.txt`, splits each line at the `|`, trims the spaces, and writes every card as a line of C++.
- `cards.h`, the generated output: a `Card` struct, an array of all 78 cards, and a `CARD_COUNT` that works out the total itself.

### How I approached it

- Converted three cards by hand first, to understand the target format before automating it. A missing comma between two cards was the first bug, and the clearest argument for writing a script.
- Built the script in small pieces and ran it after every change: print a line, count the lines, read one card, split it, trim it, format it, loop it, write it.
- Ran a proofreading pass on `cards.txt` before converting. Standardised on Irish/British spelling and consistent hyphenation.

### Decisions

- `cards.txt` is the single source of truth. I only ever edit that file and rerun the script.
- `cards.h` is generated, never edited by hand. Any hand edits would be overwritten on the next run.
- Built the C++ frame (header and footer) as separate lists and joined them at write time, so the card count printed by the script stays accurate.

### What tripped me up

- Python counts from 0. `lines[70]` returned the 71st card. Rule: position = line number − 1.
- An `IndentationError` after adding the loop. Read the error, found the line, fixed it.
- The terminal opened in my home folder instead of the project folder. Fixed with `cd`.
- f-strings use `{ }` to insert values, so printing a real brace needs `{{ }}`.

### Known limitations

- The script assumes every line in `cards.txt` is well formed. A blank line, a missing `|`, or a `"` inside a meaning would break it. Fine for now because the file is clean. Hardening it is on the ideas list.

**Next:** add `cards.h` to the sketch and draw a random card with a button press. Needs the device, which is still in the post.

---

## Entry 003 — Outside review of the converter

**Date:** 2026-10-07 (addendum)  
**Status:** Review

**What came up:** an outside review questioned the approach. Why convert the text on my computer instead of having the device read `cards.txt` directly? And isn't generating code from a text file a security risk?

### Why I kept the approach

- Reading and parsing text in C++ on a microcontroller is harder than doing it in Python on a laptop, and it means uploading the text file to the device's storage separately.
- Converting first means the device code stays simple and a typo can't crash it at runtime. Any problem shows up on my computer instead.
- The trade-off: changing a meaning means rerunning the script and re-uploading the sketch.

### What I'm changing

The injection point is valid. A stray `"` in a meaning could close the text early and let code slip into `cards.h`. The risk is low here (my own file, my own machine, output I read before uploading), but the habit matters. I'm adding escaping to `convert.py` so quotes inside meanings are neutralised.

---

## Entry 004 — Researching card art

**Date:** 2026-10-11 to 2026-10-13  
**Status:** Research

**Goal:** find card images that are legal to use, look good on a 1.14" screen, and can appear in portfolio photos.

### What I looked at

- **1909 Pamela Colman Smith deck (Wikimedia Commons scans).** Public domain, and the deck my meanings were written for. Avoid the 1971 recoloured edition, which is still under copyright. "Rider-Waite" is a trademark, so it stays out of the project name.
- **Sola Busca (1491).** The earliest fully illustrated 78-card deck, and the one that inspired Waite to illustrate the minor arcana. Public domain, but its majors don't map to standard meanings. A candidate for a hidden "archive mode".
- **Tarot de Marseille.** Bold, flat colours that would read well on a tiny screen, but no illustrated minors.
- **Pixel-art packs on itch.io.** Several full 78-card decks at around 48×80 to 57×79 pixels, licensed for use with credit. Pixel art scales up 2× cleanly, which leaves room for text under the card.
- **Drawing my own.** Possible in pixel art. Only the 22 majors and court cards would need unique art. Number cards could use suit symbols, either drawn by hand or drawn by the code.

### What I learned

The screen shows full-colour JPEG/PNG images. The limit is resolution (135×240), not the type of image. Bold art survives the shrink, fine linework doesn't.

### Decision

Not made yet. The code works the same whichever art I choose, so this doesn't hold up the build. Next step is a test: shrink a few candidate cards to 135×240 and check them at real size.

---

## Entry 005 — First code on the device

**Date:** 2026-10-14  
**Status:** Built

**Goal:** get my own code running on the stick.

### What happened

- The stick arrived running UiFlow2 (M5Stack's factory block-coding software). My first upload replaced it, and it can be restored with M5Burner if I ever want it back.
- Entered download mode by holding the side button until the green LED blinked.
- Found the right port by unplugging the device and seeing which entry disappeared. The port number changes depending on which USB socket is used (1401 through an adapter, 101 direct).
- The first compile failed with `bad CPU type in executable`. Arduino's `ctags` tool is Intel-only, and my Mac has Apple Silicon. Fixed by installing Rosetta: `softwareupdate --install-rosetta --agree-to-license`.
- Compiled at 16% of program storage and 7% of dynamic memory, so there's plenty of room for the card data.
- Uploaded a minimal M5Unified sketch: start the hardware, rotate to landscape, print text.

**Result:** "hello Spec" on the device screen. Session 1 complete.

**Next:** Session 2 Part B. Add `cards.h` to the sketch and draw a random card with button A.

---

*Entries are written at the time of the decision, not after.*
