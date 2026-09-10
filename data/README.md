# Data and provenance

## `field_test_phasors.csv`

This file contains the compact numerical inputs used by `examples/field_test_example.py`.

The field test is described in:

- J. Blake et al., *Open phase detection for power transformers using VT triggered optical CTs and IEC 61850-9.2LE compliant relays*, Western Protective Relay Conference, 2016.
- J. Blake, *Methods and systems for open-phase detection in power transformers*, U.S. Patent 10,802,084 B2, Oct. 13, 2020.

The conference paper presents the healthy and Phase-C-open phasor diagrams. The patent provides numerical RMS current magnitudes and relative-angle information used in the manuscript reconstruction.

### Local angular references

The healthy and measured states do not require a common absolute angular reference because the detector explicitly removes arbitrary common phasor rotation.

For consistency with the current manuscript calculation:

- the healthy reference assigns `angle(I_A,R) = 260 deg`;
- the measured Phase-C-open state assigns `angle(I_A,M) = 250 deg`;
- the remaining reported/derived angles are expressed relative to those local choices.

These two local angular origins are independent and do not imply a physical 10-degree change between the healthy and faulted states.

### Unknown measured Phase-C angle

The measured Phase-C-open magnitude is `0.08174 A`, but the public source states that relative angles involving this small current could not be determined reliably. Its angle is therefore deliberately left blank in the CSV.

The example evaluates the exact residual extrema over every possible value of this angle. No graphical estimate of the Phase-C direction is used for classification.

### Third-party rights

This repository records numerical values and provenance needed to reproduce the calculation. It does not redistribute the source paper, patent figures, or other third-party graphical material. The repository's MIT license does not alter rights in the original publications.
