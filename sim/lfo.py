"""Casualty 6 LFO: U6A Schmitt (R37/R38/R39 220k, C9 10n Miller), timing C10+C11 via R41 1k + RATE (RV1 C500k rheostat)
in parallel with the SHAPE steering (RV2 B1M + D1/D2), U6B gain 1..3.1 (WIDTH RV3 100k / R42 47k), RANGE RV4 B50k + R43 47k -> CV.
Op-amps: behavioural, 1.2-7.8 V output (TL072 on 9 V), 13 V/us."""
import sys; sys.path.insert(0, '.')
from ng import run
def net(C, rate, shape=0.5):
    ra = max(1e3 * (1 - shape) * 1000, 10); rb = max(1e3 * shape * 1000, 10)   # RV2 1M split (charge via D2 side, discharge via D1 side)
    return f"""casualty lfo
.model D1N4148 D(Is=2.52n Rs=0.568 N=1.752 Cjo=4p)
V9 v9 0 9
* U6A Schmitt: + = R37 to GND, R38 to +9, R39 from out; - = C9 from out, R40 from cap
R37 p 0 220k
R38 p v9 220k
R39 p o1 220k
C9 m o1 10n
R40 m cap 220k
Bo1 o1i 0 V=4.5+3.3*tanh(2e4*(V(p)-V(m)))
Ro1 o1i o1 100
Co1 o1 0 100p
* timing
R41 o1 dn 1k
RRATE dn cap {max(rate,1)}
D2 dn sa D1N4148
RSa sa cap {ra}
D1 sb dn D1N4148
RSb cap sb {rb}
Ccap cap 0 {C}
.ic v(cap)=4.5
"""
def period(C, rate, shape=0.5, t=60):
    out = run(net(C, rate, shape).splitlines() + ['.end'], [f'tran 1m {t} 0 1m uic',
        'meas tran tr1 when v(cap)=4.5 rise=4', 'meas tran tr2 when v(cap)=4.5 rise=6', 'meas tran vmax max v(cap) from=20', 'meas tran vmin min v(cap) from=20', 'bg_run' if False else ''])
    vals = {}
    for l in out:
        l = l.replace('stdout ', '', 1)
        for k in ('tr1', 'tr2', 'vmax', 'vmin'):
            if l.strip().startswith(k + ' ') or l.strip().startswith(k + '\t') or l.strip().startswith(k + '='):
                try: vals[k] = float(l.split('=')[1].split()[0])
                except Exception: pass
    return vals
if __name__ == '__main__':
    for C, lab in ((44e-6, '2x22u nominal (44u)'), (28e-6, '2x22u derated ~64% (28u)'), (47e-6, '47u electrolytic (original)')):
        for rate in (0, 25e3, 100e3, 500e3):
            v = period(C, rate, t=120 if rate >= 100e3 else 40)
            if 'tr1' in v and 'tr2' in v:
                T = (v['tr2'] - v['tr1']) / 2
                print(f"{lab:28s} RATE {rate/1e3:5.0f}k  f = {1/T:6.2f} Hz   cap {v.get('vmin',0):.2f}-{v.get('vmax',0):.2f} V")
            else:
                print(f"{lab:28s} RATE {rate/1e3:5.0f}k  no oscillation / too slow  {v}")
