# Enclosure: Hammond/Tayda 1590BB

Casualty 6 face drilling, made 2026-10-18 from `Casualty6.kicad_pcb`:
- 16 mm pot shafts at the centre pin −14.6 mm;
- toggle bushings at the middle pins;
- LED centre;
- footswitch from the 1590BB drawing on Dwgs.User.

**Mapping:** X = 150 − x, Y = 120 − y. Outside view, origin = face centre (box outline 94 × 119.5 mm), +X right / +Y up.

## Face (outside view)

```
   RATE    SHAPE    WIDTH    RANGE      (Y +26.5; X −30 / −10 / +10 / +30)
       REGEN     MIX     LEVEL          (Y +1.5;  X −20 / 0 / +20)
     STAGES      LED      PHASE/FILTER  (Y −21.5; X −10 / 0 / +10)
               FOOTSWITCH               (Y −39)
```

| Hole | Ø mm |
|---|---|
| 16 mm pots (M7 bushing) | 7.5 |
| Taiway 100 mini toggles (1/4" bushing) | 6.5 |
| 3 mm LED | 3.2 |
| 3PDT footswitch | 12.2 |

**Files:**
- `Casualty6_1590BB_drill.csv`: Tayda Box Tool.
- `Casualty6_1590BB_drill_template.svg`: 1:1; check the 50 × 5 mm box.

**Jacks:** in, out and DC go on the top end, near the board's IG / OG / 9V pads. They're not in these files. Mark them from your jack hardware after a test fit.

**Check before ordering:** the pots are 20 mm apart on the top row. With knobs larger than ~18 mm they'll touch, so pick slim knobs or test-fit.
