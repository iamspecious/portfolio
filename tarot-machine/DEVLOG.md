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

*Entries are written at the time of the decision, not after.*
