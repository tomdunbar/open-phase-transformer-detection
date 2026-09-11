# Data and provenance

## `field_test_phasors.csv`

This file contains the numerical inputs used by `examples/field_test_example.py` for the field-test proof of concept in **Rev 0** of:

**Tom Dunbar, _Model-Informed Phasor-Signature Matching for Detection and Classification of Open-Phase Conditions on Unloaded Transformers_.**

The field-test reconstruction is based on References [4] and [5] of Rev 0:

- J. Blake, A. Rose, A. Baker, E. Hadley, C. Vo, M. Putt, D. Stewart, J. Schaefer, and A. Ishola-Salawu, “[OPEN phase detection for power transformers using VT triggered optical CTs and IEC 61850-9.2LE compliant relays](https://doi.org/10.1109/CPRE.2017.8090042),” in *Proc. 70th Annu. Conf. Protective Relay Engineers (CPRE)*, 2017, pp. 1–5, doi: 10.1109/CPRE.2017.8090042.
- J. Blake, “[Methods and systems for open-phase detection in power transformers](https://patents.google.com/patent/US10802084B2/en),” U.S. Patent 10,802,084 B2, Oct. 13, 2020.

The conference paper presents the healthy and Phase-C-open phasor diagrams. The patent provides numerical RMS current magnitudes and relative-angle information used in the Rev 0 reconstruction. The two public sources do not explicitly state that the plotted records are identical; Rev 0 explains the basis for treating them as consistent representations of the same field-test condition.

For the complete Rev 0 bibliography and source links, see [`references/README.md`](../references/README.md).

## Local angular references

The healthy and measured states do not require a common absolute angular reference because the detector removes arbitrary common phasor rotation before comparing current vectors.

For consistency with the Rev 0 calculation:

- the healthy reference assigns `angle(I_A,R) = 260 deg`;
- the measured Phase-C-open state assigns `angle(I_A,M) = 250 deg`; and
- the remaining reported or derived angles are expressed relative to those local choices.

These two angular origins are independent. They do **not** imply a physical 10-degree phase shift between the healthy and faulted states.

## Unknown measured Phase-C angle

The measured Phase-C-open current magnitude is `0.08174 A`, but the patent states that the current is too small to determine the associated relative angles reliably. Its angle is therefore deliberately left blank in the CSV.

For each competing hypothesis, the example evaluates the most favorable residual over all possible values of this unknown angle. Because the ideal Phase-C-open prediction has zero Phase-C current, the unknown angle does not affect the Phase-C-open residual.

## Third-party rights

This directory records numerical values and provenance needed for the companion calculations. It does not redistribute source-paper figures or other third-party graphical material.

The repository's MIT License applies only to material for which the repository author holds the relevant rights. It does not alter rights in the original publications or source material.
