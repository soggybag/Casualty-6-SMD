# Casualty 6 SMD v1.0: archived revision

- **Git tag:** `v1.0` (commit `64fdb4c`, 2026-10-19)
- **Tag note:** v1.0: first JLC order (RANGE fix, R53, U1-U6 rotation offsets), 2026-10
- **Archived:** 2026-10-23 with `_tools/archive_version.py`

## Finding a part

1. Open `Casualty6_ibom.html` in a browser. Type a reference (R14) or a value (100k) in the filter box; the part lights up on the board.
   - Hover over a pad to see its net.
   - F / B switch sides.
2. Find the same reference in `Casualty6_schematic.pdf` with Cmd-F.
3. `Casualty6_board_front.pdf` / `_back.pdf` are printable: page 1 has the outlines and references, page 2 the copper. The back is mirrored, as you see it holding the board.

## Files

- `Casualty6_board_back.pdf`
- `Casualty6_board_front.pdf`
- `Casualty6_ibom.html`
- `Casualty6_render_bottom.png`
- `Casualty6_render_top.png`
- `Casualty6_schematic.pdf`
- `docs`/
- `parts.csv`
- `production`/

`production/` holds the files sent to JLCPCB for this revision: Casualty6.zip, Casualty6_hand_solder.csv, bom.csv, designators.csv, netlist.ipc, positions.csv.
