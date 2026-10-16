# Casualty 6: simulation notes (2026-10-15)

ngspice (KiCad's libngspice, `ng.py`).
- **LFO:** behavioural TL072s with 1.2–7.8 V outputs, real 1N4148 diodes.
- **Audio path:** small-signal AC, with the LM13700 as gm = Iabc / 52 mV and ideal followers for the Darlington buffers.

Scripts: `lfo.py`, `phaser_ac.py`, `regen_fix.py`.

## LFO (U6): works

Range, with SHAPE at noon:

| Timing caps | RATE min (0 Ω) | 25k | 100k | 500k (max) |
|---|---|---|---|---|
| 2 × 22µ X5R, nominal (44µ) | 11.1 Hz | 0.63 Hz | 0.19 Hz | 0.06 Hz |
| 2 × 22µ, derated to ~64% (28µ) | 15.6 Hz | 0.98 Hz | 0.29 Hz | 0.10 Hz |
| 47µ electrolytic (original) | 10.5 Hz | 0.59 Hz | 0.18 Hz | 0.06 Hz |

- The timing cap swings 3.4–5.6 V (Schmitt thresholds from the three 220k resistors). C9 10n softens the edges, so it's a Miller cap as on the Crash Sync / Bandwrecker.
- **Ceramic derating only makes it ~40–50% faster.** Not critical: keep the 1206 ceramics, or hand-fit a 47µ electrolytic if the slow end matters.
- **Control-current range** (CV → 10k per Iabc pin + 470k minimum):
  - RANGE max / WIDTH max: Iabc ≈ 17 µA → 0.68 mA (the full sweep).
  - RANGE min: tops out at ~0.28 mA.
  - WIDTH min: a narrow sweep around the RANGE setting.

## Notch positions (6-stage; 4-stage in brackets): good

The OTA all-pass corner is f ≈ 6.0 MHz × Iabc (33n caps, 27k / 27k / 2k divider).

| Iabc | Notch 1 | Notch 2 | Notch 3 |
|---|---|---|---|
| 17 µA | 39 Hz (79) | 176 Hz (1.4 k) | 1.6 kHz |
| 60 µA | 112 Hz (195) | 463 Hz (2.0 k) | 2.7 kHz |
| 200 µA | 258 Hz (381) | 1.16 kHz (3.4 k) | 5.1 kHz |
| 700 µA | 485 Hz (640) | 3.1 kHz (7.0 k) | 12.6 kHz |

So the main notches sweep the usual phaser range (~100 Hz – 3 kHz).

## Problem: REGEN loads AP1 → shallow upper notches

- R30 (15k, the REGEN feed) goes into AP1's − input, so even with REGEN at minimum it loads that node. AP1's high-frequency gain becomes 1 + 10k / (10k ∥ 15k) − 1 = **1.67 (+4.3 dB)** instead of 1.
- The wet path is louder than the dry above ~3 kHz, so they can't cancel there:

| (6-stage, REGEN min) | Notch 1 | Notch 2 | Notch 3 |
|---|---|---|---|
| As built, Iabc 200 µA | −50 dB | −29 dB | −14 dB |
| AP1 unloaded, Iabc 200 µA | −48 dB | −43 dB | −42 dB |

With REGEN up, the board's version gets worse: notch 3 at −3 to +9 dB.

## Proposed fix: U5B (spare) as a non-inverting REGEN summer ahead of AP1

```
DRY (U3A) ── 10k ──┐
                   ├── U5B + ;  U5B − : 6k8 from out, 10k to VREF  (gain 1.68)  ──► X
REGEN wiper ─ R30 15k ┘
X ──► AP1 input (C6, R27)  and  ► MIX pot (RV6 pin 3, instead of DRY)
```

- AP1 becomes a clean all-pass: R30 no longer touches its − input.
- The mixer's dry signal is taken from X, so any level change from REGEN appears in both dry and wet equally. The notches stay deep at every REGEN setting.
- **Polarity matters.** An *inverting* summer flips REGEN into positive feedback at low frequencies (+23 dB bass boom at max in simulation). The non-inverting version keeps the original's polarity.

Simulated results (6-stage, MIX max):

| REGEN | Notches (Iabc 200 µA) | Regen peak | Bass (20 Hz) |
|---|---|---|---|
| min | −39 / −34 / −33 dB | +9.3 dB (the mixer's ×2.9 makeup) | +9.2 dB |
| half | −37 / −34 / −33 dB | +13.2 dB | +9.2 dB |
| max | −39 / −38 / −37 dB | **+18.9 dB** between the notches | +4.8 dB (no boom) |

**Parts:** +3 resistors (10k, 6k8, 10k) on U5B, which is already on the board as a parked follower. Re-route around U5.

## Other notes

- **OTA input level:** V− = 0.0645 × (Vin + Vout). A 0.5 V peak guitar signal gives ~65 mV at the OTA, past its ~±25 mV linear range, so hard playing will add some OTA grit (common in OTA phasers). If it's too much: 2k → 1k5 (needs ~1.3× more Iabc for the same notches; the range allows it).
- Not simulated: the PHASE/FILTER switch mode, and LFO-to-audio ticking (check on the bench: decoupling and the VCLEAN rail are in place).

## Applied (2026-10-15)

- **Schematic:** U5B is the REGEN summer.
  - R48 10k (DRY → U5B +), R30 now goes to U5B + (net REGEN_SUM), R49 6k8 (out → −), R50 10k (− → VREF).
  - The new net X (U5B out) feeds C6 / R27 (AP1) and RV6 pin 3 (MIX).
  - ERC 0; the netlist diff contains only these changes.
- **PCB:** R48–R50 placed beside U5 (R49 between pins 6 and 7); all pad nets synced from the netlist.
  - Full re-route (Freerouting, 400 passes): **DRC 0 errors, 0 unconnected, parity 0**; 74 vias (was 53); silkscreen warnings only.
- **Toggle footprints:** `Casualty:SW_Taiway_100_DPDT_PC` now has UF1's slots: 3.4 × 2.2 pads, 2.6 × 1.1 oval drills.
- **CV IN / LFO OUT pads (2026-10-15):**
  - J6 CV IN → R51 10k → CV node (sums with the RANGE / LFO divider).
  - J7 LFO OUT ← R52 1k ← U6B output.
  - J6 and J7 sit on the left board edge (x 112.5, y 102.5 / 114).
  - Full re-route: DRC 0 / 0 unconnected / parity 0, 75 vias.
