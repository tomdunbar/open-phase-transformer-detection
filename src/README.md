# Source code

`open_phase_detection.py` contains the reusable numerical functions used by the reproducibility examples.

The initial implementation includes:

- conversion from polar magnitude/angle to a complex phasor;
- the finite-`r` coefficient `q(r) = (1-r)/(r+2)`;
- healthy and phase-specific current operators;
- the parameter-free large-|r| operator bank (`q = -1`);
- phase-aligned residual calculation; and
- exact residual extrema when one measured phasor angle is unknown.

The module intentionally stays close to the equations in the associated manuscript rather than introducing a larger software framework.
