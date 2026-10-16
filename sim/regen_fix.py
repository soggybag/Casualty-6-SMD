"""Proposed fix: U5B (spare) as an inverting summer ahead of AP1: X = -(DRY + PHASE_OUT x 10k / (R30 + RV5 part)).
AP1 is then a clean all-pass (R27 = R29 = 10k, nothing else on its - input). The mixer takes X as its dry signal.
Regen modelled as a fraction r of PHASE_OUT through R30 15k (r = 0 off, r = 1 max = 0.67 loop gain)."""
import sys; sys.path.insert(0, '.')
from ng import run
def net(iabc, r, stages=4):
    gm = iabc / 0.052
    L = ['casualty fix', 'Vin dry 0 dc 0 ac 1',
         'Rsa dry sm 10k', 'Rsf x sm 10k', f'Brg rg 0 V={r}*V(po)', 'R30 rg sm 15k', 'E5 x 0 0 sm 1e6',
         'C6 x ap1p 4.7n', 'R28 ap1p 0 10k', 'R27 x ap1m 10k', 'R29 ap1 ap1m 10k', 'E1 ap1 0 ap1p ap1m 1e6']
    prev = 'ap1'
    for s in range(1, stages + 1):
        n = f's{s}'
        L += [f'C{n} {prev} x{n} 33n', f'R{n}a {prev} m{n} 27k', f'R{n}b {n} m{n} 27k', f'R{n}c m{n} 0 2k',
              f'G{n} 0 x{n} 0 m{n} {gm}', f'E{n} {n} 0 x{n} 0 1']
        prev = n
    L += [f'Epo po 0 {prev} 0 1', f'C7 {prev} ap2p 47n', 'R32 ap2p 0 10k', f'R31 {prev} ap2m 10k', 'R33 wet ap2m 10k', 'E2 wet 0 ap2p ap2m 1e6',
          'Bmix out 0 V=-(68/47)*(V(wet)+V(x))', '.end']
    return L
def resp(**kw):
    out = run(net(**kw), ['ac dec 200 20 20k', 'print vdb(out)'])
    rows = []
    for l in out:
        l = l.replace('stdout ', '', 1).split()
        if len(l) == 3 and l[0].isdigit(): rows.append((float(l[1]), float(l[2])))
    return rows
if __name__ == '__main__':
    for r in (0.0, 0.5, 1.0):
        for ia in (17e-6, 200e-6, 700e-6):
            rows = resp(iabc=ia, r=r); mx = max(rows, key=lambda x: x[1]); mn = [rows[i] for i in range(1, len(rows)-1) if rows[i][1] < rows[i-1][1] and rows[i][1] <= rows[i+1][1]]
            print(f"regen {r:.1f}  Iabc {ia*1e6:4.0f} uA  peak {mx[1]:+5.1f} dB at {mx[0]:6.0f} Hz   notches " + ', '.join(f'{f:5.0f} Hz ({d:+.0f})' for f, d in mn))
