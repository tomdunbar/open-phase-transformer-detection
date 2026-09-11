# Source code

`open_phase_detection.py` contains the reusable numerical functions used by the Rev 0 companion calculations.

The module includes:

- conversion from polar magnitude and angle to a complex phasor;
- the finite-$r$ coefficient $q(r)=(1-r)/(r+2)$;
- healthy and phase-specific open-phase current operators;
- the parameter-free large-$|r|$ operator bank with $q=-1$;
- application of an operator to a healthy reference-current vector;
- the common-rotation-invariant minimal residual; and
- exact residual extrema when one measured phasor angle is unknown.

The implementation intentionally stays close to the equations in the associated manuscript rather than introducing a larger software framework. It is intended to make the Rev 0 numerical calculations transparent and easy to inspect.

The executable examples are documented in [`examples/README.md`](../examples/README.md).
