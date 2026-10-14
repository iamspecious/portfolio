# Tarot Machine

A pocket tarot-draw gadget built on an M5StickS3. Press a button and it draws a random Rider-Waite-Smith card, shows the card and its meaning, and eventually speaks. "Tarot Machine" is a working title.

**Status: in progress.** First sketch running on the device ("hello Spec" on screen). Card meanings converted into C++. No card draws yet.

---

## Introduction

This is my first hardware build. I learn by doing, and I wanted a project interesting enough to actually finish.

The inspiration is Finbarre Snarey's TAROTRON 2000. That build and its design are his. This page covers my own version on an M5StickS3.

The device is an M5Stack StickS3: an ESP32-S3 board with a 1.14" screen, a speaker, buttons and a motion sensor, all in one small case. It needs no soldering and no extra parts.

What's done so far:

- Chose the hardware and ordered it.
- Set up Arduino IDE 2 with the M5Stack board package and the M5Unified and M5GFX libraries.
- Wrote all 78 card meanings myself, upright and reversed, in a pipe-delimited `cards.txt`.
- Set up the sketchbook so each version of the build gets its own sketch folder.
- Wrote `convert.py`, a Python script that turns `cards.txt` into `cards.h`, a C++ file the sketch can use. `cards.txt` is the only file I edit. `cards.h` is generated and never edited by hand.
- Researched card art: public-domain decks, pixel-art packs and drawing my own. No choice made yet.
- Got my first sketch running on the stick: "hello Spec" on the screen. Session 1 complete.

The decisions behind each of these are in [DEVLOG.md](./DEVLOG.md).

---

## Constraints

**No card draws yet.**  
The device runs a minimal "hello" sketch. The card data is ready in `cards.h`. Drawing a card is the next session. This page will only describe features once they work.

**The converter trusts its input.**  
`convert.py` assumes every line in `cards.txt` is well formed. A blank line, a missing `|`, or a `"` inside a meaning would break it. The file is clean for now. After an outside review, I'm adding escaping so a quote inside a meaning can't close the text early. Wider hardening is on the ideas list.

**First hardware build.**  
I'm learning the board, the libraries and the Arduino workflow as I go. The build is split into short sessions so each step is small enough to finish.

**Parts kept to the stick and a cable.**  
No soldering, no extra sensors, no add-on kits. Everything planned has to work with what the StickS3 already has.

**No images yet.**  
Card art is researched but not chosen. The screen is 135×240, so the next step is testing a few candidates at real size.

---

## Roadmap

1. **Get the device talking to the computer** — "hello" on screen. Done 2026-10-14.
2. **First draw** — button press gives a random card name, with reversals.
3. **Meanings on screen.**
4. **Sound effects.**
5. **Card images.**
6. **Voice, shake-to-draw, modes, case.**

Feature ideas that come up along the way go into an ideas file, not into the current session.

---

## Stack

- **Hardware:** M5Stack StickS3 (SKU K150), USB-C data cable
- **Development:** Arduino IDE 2, M5Stack board package, M5Unified and M5GFX libraries
- **Python:** `convert.py` generates `cards.h` from `cards.txt`
- **Planned:** LittleFS for card images, the ESP32 hardware random number generator for draws, Python for batch image resizing
