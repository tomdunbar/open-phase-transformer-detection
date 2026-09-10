# Examples

## Published Phase-C-open field test

`field_test_example.py` reproduces the field-test proof of concept reported in the associated manuscript.

From the repository root:

```bash
pip install -r requirements.txt
python examples/field_test_example.py
```

The script:

1. loads the healthy and measured field-test phasors from `data/field_test_phasors.csv`;
2. constructs the parameter-free large-|r| hypothesis bank, with `q = -1`;
3. applies each hypothesis operator to the same healthy reference current;
4. removes arbitrary common phasor rotation using the closed-form phase-aligned residual;
5. treats the measured Phase-C angle as unknown; and
6. reports the exact best- and worst-case residual over all possible values of that angle.

The expected minimum residuals are approximately:

| Hypothesis | Minimum residual (A) |
| --- | ---: |
| Healthy | 1.203 |
| Phase A open | 2.019 |
| Phase B open | 1.447 |
| Phase C open | 0.178 |

The Phase-C-open hypothesis therefore wins with a minimum margin of approximately `1.025 A` to the closest competing hypothesis.

The script contains numerical assertions against these manuscript values and prints `PASS` when they are reproduced.

### Why no numerical angle sweep is required

For an unknown measured Phase-C angle, the complex inner product can be written

```text
S + conj(I_C,pred) |I_C,meas| exp(j theta_C)
```

where `S` contains the known A- and B-phase terms. The residual is smallest when the unknown term aligns with `S` and largest when it anti-aligns. The script uses those exact extrema rather than choosing an angular step size.

For the Phase-C-open hypothesis, the predicted Phase-C current is exactly zero, so the measured Phase-C angle has no effect on its residual.
