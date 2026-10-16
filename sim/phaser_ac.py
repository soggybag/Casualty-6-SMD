"""Casualty 6 audio path, small-signal AC (VREF = AC ground):
DRY (input buffer) -> AP1 (U3B: C6 4n7 / R28 10k to +, R27 10k in, R29 10k fb, REGEN via R30 15k + RV5 into -)
-> OTA stages S1..S4 (cap from stage in to OTA out, 27k in / 27k fb / 2k to VREF at -, + = VREF, Darlington follower out)
-> PHASE_OUT -> AP2 (U4A: C7 47n / R32 10k to +, R31 10k in, R33 10k fb) -> WET
-> U4B mixer: -(68k/47k) x (WET + DRY x MIX).  gm = Iabc / 52 mV per OTA (LM13700, small signal)."""
import sys, math; sys.path.insert(0, '.')
from ng import run
def net(iabc, stages=4, regen_r=None, mix=1.0, ap1_fix=False):
    L = ['casualty phaser ac', 'Vin dry 0 dc 0 ac 1']
    # AP1 (U3B), ideal op-amp
    L += ['C6 dry ap1p 4.7n', 'R28 ap1p 0 10k', 'R27 dry ap1m 10k', 'R29 ap1 ap1m 10k', 'E1 ap1 0 ap1p ap1m 1e6']
    if regen_r is not None and not ap1_fix: L += [f'R30 ap1m 0 {regen_r}']   # REGEN off: wiper at VREF, 15k+ loads the - node
    prev = 'ap1'; gm = iabc / 0.052
    for s in range(1, stages + 1):
        n = f's{s}'
        L += [f'C{n} {prev} x{n} 33n', f'R{n}a {prev} m{n} 27k', f'R{n}b {n} m{n} 27k', f'R{n}c m{n} 0 2k',
              f'G{n} 0 x{n} 0 m{n} {gm}', f'E{n} {n} 0 x{n} 0 1', f'Rl{n} x{n} 0 1e12']
        prev = n
    L += ['C7 ' + prev + ' ap2p 47n', 'R32 ap2p 0 10k', f'R31 {prev} ap2m 10k', 'R33 wet ap2m 10k', 'E2 wet 0 ap2p ap2m 1e6']
    L += [f'Bmix out 0 V=-(68/47)*(V(wet)+{mix}*V(dry))']
    return L + ['.end']
def response(**kw):
    cols = {}
    for q in ('vdb(out)', 'vp(wet)', 'vdb(wet)'):
        out = run(net(**kw), ['ac dec 200 20 20k', f'print {q}'])
        for l in out:
            l = l.replace('stdout ', '', 1).split()
            if len(l) == 3 and l[0].isdigit():
                cols.setdefault(int(l[0]), [float(l[1])]).append(float(l[2]))
    return [tuple(v) for k, v in sorted(cols.items()) if len(v) == 4]
def notches(rows):
    res = []
    for i in range(1, len(rows) - 1):
        if rows[i][1] < rows[i-1][1] and rows[i][1] <= rows[i+1][1] and rows[i][1] < max(r[1] for r in rows) - 6:
            res.append((rows[i][0], rows[i][1]))
    return res
if __name__ == '__main__':
    for label, kw in (('REGEN at min (R30 15k loads AP1)', dict(regen_r=15e3)), ('AP1 unloaded (ideal)', dict(regen_r=None))):
        print('==', label)
        for stages in (4, 2):
            for ia in (17e-6, 60e-6, 200e-6, 700e-6):
                rows = response(iabc=ia, stages=stages, **kw)
                pk = max(r[1] for r in rows)
                n = notches(rows)
                wet_hi = [r[3] for r in rows if r[0] > 15e3][0]; wet_lo = [r[3] for r in rows if r[0] < 25][0]
                print(f"  {'6' if stages==4 else '4'}-stage  Iabc {ia*1e6:5.0f} uA  notches: " + ', '.join(f'{f:6.0f} Hz ({d-pk:+.0f} dB)' for f, d in n) + f"   | wet gain LF {wet_lo:+.1f} dB, HF {wet_hi:+.1f} dB")
