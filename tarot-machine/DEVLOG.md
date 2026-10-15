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

## Entry 006 — Drawing cards on the device

**Date:** 2026-10-14 (afternoon)  
**Status:** Built

**Goal:** get the device drawing random cards from my own meanings.

### What I built

- Added `cards.h` to the sketch and confirmed all 78 cards loaded by printing `CARD_COUNT` on screen before anything else.
- Button A draws a random card with `esp_random() % CARD_COUNT`.
- A 50/50 reversal with `esp_random() % 2`, which picks the upright or reversed meaning to display.
- `printWrapped()`, my first C++ function: it measures each word with `textWidth()` and starts a new line before a word would run off the screen, so words aren't split in half.

### Changes I made myself

- Replaced the "hello" text with a proper start screen showing the machine name and how many cards are ready.
- Noticed the start screen had the same wrapping problem and fixed it by reusing `printWrapped()` instead of writing new code.

### What tripped me up

- Save As produced a blank sketch instead of copying my code. I now check the new version has my code in it before moving on.
- I questioned whether the draws were truly random after a run of three reversals and then three uprights. In six coin flips, about 59% of sequences contain a streak of three, so a streak is normal. I also learned that `esp_random()` is only true hardware randomness while the radio is on. Without it, the numbers are generated by a formula. Still fair for a tarot draw, just not hardware-random.

---

## Entry 007 — Card art, flip animation, and quality-of-life features

**Date:** 2026-10-14 (evening)  
**Status:** Built, one open bug

**Goal:** add the card art and make the device feel like a finished gadget.

### Card art

- Got a 1-bit card set: 78 PNGs at 135×240, white on black, with a README specifying the colour per suit and that reversed cards reuse the same art rotated 180°.
- Converted all 78 to C arrays myself in image2cpp (horizontal, 1 bit per pixel). Each card is 4,080 bytes. The whole deck took program storage from 16% to 26%.
- Each card is drawn with `drawBitmap()` and tinted at draw time by suit: Majors teal, Wands orange, Cups blue, Swords silver, Pentacles gold. A `cardColour()` function picks the colour from the card's position in the deck.
- The art's README said its order matched my `cards.txt`. It didn't: my Wands were in a different order. Reordered `cards.txt` to match the art rather than renaming 14 images.

### Screens and controls

- A framed opening screen and a "Drawing…" screen with animated dots, drawn entirely in code with rounded rectangles and centred text (`setTextDatum(middle_center)`).
- A flip animation: the card outline narrows to a sliver and widens again, like a card turning edge-on, revealing the back with the card name, a divider, and the meaning in the suit colour.
- Tap/hold controls on the one safe button: tap flips between the art and the meaning, hold (800 ms) draws a new card from any screen. This replaced an earlier version where every press drew a new card, with no way back to the art.
- A `screen` variable tracks three states (opener, card, meaning). `pick` and `isReversed` became global variables, because the meaning is shown on a later press than the draw and the card has to be remembered between them.

### Battery

- The screen sleeps after 60 seconds without a press and wakes on the next press, back where it was. The waking press only wakes the screen; it doesn't flip or draw.
- M5Stack's docs only show sleep with timer wake-up, not button wake-up, so true deep sleep is parked until I can test it properly.

### Auto-sized meanings

- `wrapText()` gained a measuring mode, so it can work out how tall a meaning would be without drawing it.
- `printFitted()` tries font sizes from largest to smallest and uses the first one that fits the space.
- First version: any single word wider than the frame forced a drop to a much smaller, different font, so some cards looked random. Long words like *misinterpretation* and *self-awareness* were the trigger. Fixed by scaling the same font to 90% and then 80% instead of switching font.

### What tripped me up

- `#include "cards_art.h"` when the file was `card_art.h`: a one-letter typo the compiler pinpointed by line and column.
- New functions pasted in twice, which gave "redefinition" errors. Replaced the file with one clean copy, and now search for each function name after pasting.
- The upload port disappeared because the stick wasn't in download mode.

### Open bug

Wands cards show the wrong meaning (the 4 of Wands shows the Page of Wands). The art is in the new order, but the sketch's `cards.h` is still in the old order. `convert.py` reported "78 cards converted" either way, because it only checks the count, not the order. Next session: trace which step didn't apply (the download, the conversion, or the copy into the sketch).

### Ideas logged

- Have `convert.py` write `cards.h` straight into the current sketch folder, removing the manual copy.
- Have `convert.py` print the first card of each suit after converting, so a wrong order shows up straight away.
- Add the quote escaping back into `convert.py`.

**Next:** fix the Wands order, then sound.

---

## Entry 008 — Fixes, safer tooling, and version 4

**Date:** 2026-10-15  
**Status:** Fixed / Built

### Wands bug: fixed

- **Cause:** `convert.py` never ran on the reordered `cards.txt`. The old `cards.h` stayed in the project folder and was copied into every later sketch.
- **How I found it:** checked each stage in turn (the source file, the generated file, then the sketch's copy), using `sed -n 23p` to print one line and `grep -m1 Wands` to find the first Wands card. The source was right and the generated file wasn't, which pointed to the conversion step.
- **Fix:** reran the conversion, confirmed it with `grep`, copied it in, and reopened the sketch so the IDE couldn't save its old copy back over the new file.
- **Lesson:** "78 cards converted" only counted lines and never checked the order. A message only proves what it checks.

### `convert.py` hardened

- Made a backup (`convert_backup.py`) before changing working code.
- **Escaping:** a `clean()` function puts a `\` in front of any quote or backslash in a meaning, so it can't end a C++ string early. This closes the injection risk raised in the outside review on Day 2.
- **Order check:** the script confirms there are 78 cards, card 0 is The Fool, and each suit starts with its Ace at positions 22, 36, 50 and 64. If anything is wrong, it stops before writing `cards.h`, so a bad list can't overwrite a good file.
- **Auto-copy:** the script finds the newest `tarot_vN` folder by comparing version numbers (not names, so v10 sorts after v9) and writes `cards.h` straight into it. This removed the manual Finder copy that caused two bugs. Older versions keep their own copy, which is what a backup should do.
- **Version number:** the script writes `SKETCH_VERSION` into `cards.h`. If the device ever shows an older version than the sketch, `cards.h` is out of date.
- New routine: edit `cards.txt` → `python3 convert.py` → reopen the sketch → upload.

### Version 4 features

- **Battery indicator** on the opening screen: an icon drawn from three shapes, a percentage, a "+" while charging, and red below 20%. It uses `M5.Power.getBatteryLevel()` and `isCharging()` from M5Stack's StickS3 example.
- **Home button:** the side button (B) returns to the opening screen from anywhere, which also refreshes the battery reading. Final controls: front tap flips, front hold draws, side button goes home.
- **Version display:** the opening screen shows the version from `cards.h`, so I never type it by hand.

### What tripped me up

- `unexpected indent` in Python from code copied with leading spaces. Lines must start at the left edge unless they're inside a block or a list.
- The first plan for home was a double-tap, which would have made every single tap wait slightly. I pointed out the stick has a second programmable button, which was the better solution.

---

## Entry 009 — Where the card art came from

**Date:** 2026-10-15  
**Status:** Note

I think AI-generated art is bad. I'm less sure whether this counts as it.

Each card is a border coded around the display, some text, and a common symbol: five cups for the 5 of Cups, the astrological sign for Leo on Strength. Symbols like these are freely available UI icons. I put the set together with Claude, but nothing here is an illustration, and I'm not making art. I'm placing an icon.

I'm honestly unsure where that sits, so I'm writing down exactly how it was made and letting people judge for themselves.

The full deck is in [contact-sheet.webp](./contact-sheet.webp).

---

*Entries are written at the time of the decision, not after.*
