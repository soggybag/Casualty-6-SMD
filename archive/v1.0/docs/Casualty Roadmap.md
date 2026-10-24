# Casualty 6 SMD: roadmap, notes and to-do

Current design: Rick Holt's Causality 6 phaser rebuilt for JLC (see the KiCad schematic). Fixes vs the original are in the project memory and the schematic notes. Not built yet.

## Planned: LoveTone-style extras

Quirky features to add once the base phaser is proven. The Trem's SHAPE (ramp ↔ triangle) and square/triangle ideas apply here too. The first concrete one is below.

## Random / sample-and-hold LFO (2026-10-14)

**Inspiration:** the Maestro FSH-1 / madbean Sharkfin. Its S/H section steps a resonant filter to random levels at the LFO rate. It's rare in guitar effects and sounds great. The Sharkfin's analog S/H is finicky: avalanche-noise transistor, JFET sampler and JFET hold buffer, all needing ±9 V and part selection.

**For Casualty:** add an **LFO SHAPE switch: triangle / S&H (stepped) / smooth random**.
- The random generator's output becomes a CV that drives the same point as today's LFO: CV → 10k per Iabc pin.
- WIDTH and RANGE then work on it unchanged.
- Stepping a phaser's notches sounds gentler than stepping a resonant filter, so even the stepped mode stays musical.
- **U5B (spare)** can be the hold buffer or the GLIDE stage.

### Random generator options (all single 9 V)

1. **Shift-register pseudo-random (preferred).**
   - CD4015 (dual 4-bit shift register, cascaded to 8 bits) + CD4070 XOR feedback = a linear-feedback shift register (LFSR).
   - Clock it from the existing LFO's square, so the RATE knob sets the step rate.
   - Take 3–4 outputs through a weighted resistor ladder (R / 2R / 4R / 8R, or an R-2R ladder) = a 3–4 bit DAC. Each clock gives a new step.
   - No noise source, no sampling, no hold cap to leak; all CMOS; nothing to audition.
   - The sequence repeats only after up to 255 steps (8 bits).
   - **Optional "true-ish" randomness:** XOR a free-running oscillator into the feedback (see option 3), so the pattern never repeats exactly.
2. **Microcontroller (ATtiny85).**
   - Stepped random, smooth random, triangle, square and envelope modes from one chip, with RATE and GLIDE pots read by the ADC.
   - The output is filtered PWM (2-pole RC; filter well, as on GlitchStorm / Mutant).
   - Most flexible, but digital in an analog pedal.
3. **Hex Schmitt (CD40106) oscillators, summed.**
   - Five gates as free-running square oscillators at **unrelated** rates (not integer ratios, e.g. 0.7 / 1.3 / 2.9 / 5.3 / 11 Hz), summed through weighted resistors. That gives a complex stepped waveform that changes whenever any oscillator flips: random timing **and** random levels.
   - **For clocked steps** (classic S&H: one step per beat), use the sixth gate as the RATE clock and **sample** the sum: CD4066 / CD4053 switch → film cap → TL072 buffer.
   - Or (simpler) feed the oscillators into the **shift register's data / XOR input**. The shift register then does the clocking, and no S&H is needed.
   - Cautions: CMOS RC oscillators drift with supply and temperature (fine here). Decouple the chip well, or the oscillators **lock to each other** through the supply.
   - The pattern only repeats at the lowest common multiple of the periods.

### GLIDE

A slew control between the steps and the CV.
- Simplest: a pot + resistor into a cap, buffered (a 1-pole RC).
- Better (even in both directions): an op-amp slew limiter.
- Low settings give the stepped "computer" sound; high settings give smooth wandering sweeps.

### Spin-off: a standalone "S&H filter" pedal

The same random generator + GLIDE, driving a **resonant OTA filter** (LM13700, 2-pole state-variable or the Sharkfin-style two-OTA low-pass).
- Envelope filter dropped; single 9 V supply.
- Controls: RATE, GLIDE, RANGE/DEPTH, REZ, (MIX/LEVEL); optional tap or an "LED = clock" indicator.
- The random LFO block becomes a **reusable building block**:
  - Casualty (above);
  - a random tremolo (Trem's VCA);
  - Penfold's VCA;
  - Frobnicator;
  - a Eurorack random/S&H module (Euro-LFO / Mutant family).
- The Sharkfin build (madbean PCB, didn't work; suspected the F/SH 3PDT fitted rotated 90°) is the reference for the filter sound.

## JLC order notes (2026-10-19)

- **IC rotation in JLC's placement preview was inconsistent** with the same `positions.csv` (U1 270°, U2–U6 90°):
  - JLCONE desktop app: U1–U6 rotated;
  - first web order: correct;
  - second web order: rotated again (legs across the pads).
- **Fix on the order:** rotated U1–U6 90° clockwise in the web viewer, so pin 1 (pink dot) matches the small arrow on the silkscreen.
- **Third web order:** rotated again, so 2 of 3 web uploads agree. **Fixed in KiCad:** hidden `FT Rotation Offset` 270 on U1–U6 (schematic, every unit, and board). `positions.csv` now has U1 180°, U2–U6 0°.
- **Next order:** check every IC in the web viewer anyway. Legs must sit along the pads, and pin 1 must match the silkscreen arrow. If they ever come out rotated the other way, remove the offset.
