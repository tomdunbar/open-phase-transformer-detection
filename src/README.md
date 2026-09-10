# Source code

This directory will contain the reusable implementation of the model-informed open-phase detection calculations.

The initial release is expected to include functions for:

- constructing predicted current vectors for each fault hypothesis;
- applying common phasor-angle alignment;
- calculating scalar residuals;
- ranking hypotheses and calculating the detection margin; and
- evaluating transformer-model parameter choices used in the paper.

The source code should remain small and readable enough that an engineer can inspect the calculation directly.
