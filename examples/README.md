# Examples

The scripts in this directory reproduce the numerical calculations associated with **Rev 0** of:

**Tom Dunbar, _Model-Informed Phasor-Signature Matching for Detection and Classification of Open-Phase Conditions on Unloaded Transformers_.**

Run the examples from the repository root after installing the packages in `requirements.txt`.

## Field-test proof of concept

```bash
python examples/field_test_example.py
```

`field_test_example.py` reproduces the Phase-C-open field-test calculation in Rev 0.

The script:

1. loads the healthy and measured field-test phasors from `data/field_test_phasors.csv`;
2. constructs the parameter-free large-$|r|$ hypothesis bank with $q=-1$;
3. applies the healthy and Phase-A-, Phase-B-, and Phase-C-open operators to the same healthy reference current;
4. removes arbitrary common phasor rotation using the closed-form minimal residual;
5. treats the measured Phase-C angle as unknown; and
6. evaluates the exact minimum and maximum residual over all possible values of that angle for each hypothesis.

The Rev 0 minimum residuals are:

| Hypothesis | Minimum residual (A) |
|---|---:|
| Healthy | 1.203 |
| Phase A open | 2.019 |
| Phase B open | 1.447 |
| Phase C open | 0.178 |

The Phase-C-open hypothesis is therefore the best match, with a minimum margin of approximately **1.025 A** to the closest competing hypothesis.

The script contains numerical assertions against these Rev 0 values and reports `PASS` when they are reproduced.

### Why no numerical angle sweep is required

For an unknown measured Phase-C angle, the complex inner product can be written schematically as

```text
S + conj(I_C,pred) |I_C,meas| exp(j theta_C)
```

where `S` contains the known Phase-A and Phase-B terms. The residual is minimized when the unknown contribution aligns with `S` and maximized when it anti-aligns. The script therefore evaluates the exact extrema rather than using an arbitrary angular grid.

For the Phase-C-open hypothesis, the predicted Phase-C current is zero, so the unknown measured Phase-C angle has no effect on its residual.

## Finite-$r$ sensitivity analysis

```bash
python examples/finite_r_sensitivity.py
```

`finite_r_sensitivity.py` evaluates how the field-test classification changes when the parameter-free large-$|r|$ approximation is replaced by selected finite positive-real values of $r$:

```text
r = 4, 10, 20, 50, 100, 200
```

For each value, the script calculates

$$
q(r)=\frac{1-r}{r+2},
$$

reconstructs the healthy and three open-phase hypothesis operators, and compares the resulting predicted currents with the **same measured Phase-C-open field-test vector** used in `field_test_example.py`.

Only the model-predicted hypothesis currents change as $r$ changes. The measured field-test record does not.

As in the Rev 0 proof of concept, the measured Phase-C current magnitude is known while its angle is treated as indeterminate. Each hypothesis is therefore given its most favorable possible Phase-C angle using the same closed-form residual calculation.

The script reports the Phase-C-open residual, the nearest competing residual margin, and the winning hypothesis for each selected value of $r$. It reports `PASS` when Phase C open remains the winning hypothesis throughout the declared sweep.

This calculation is a **sensitivity check on the large-$|r|$ approximation used in Rev 0**. It is not an independent validation of the transformer model or of the proposed detector over a broader application domain.

## Data and implementation

The numerical inputs and their provenance are documented in [`data/README.md`](../data/README.md).

Reusable numerical functions are in [`src/open_phase_detection.py`](../src/open_phase_detection.py), with a summary in [`src/README.md`](../src/README.md).
