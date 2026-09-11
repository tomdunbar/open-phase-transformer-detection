# Open-Phase Transformer Detection

Companion software, numerical inputs, and reference material for the manuscript:

**Tom Dunbar, _Model-Informed Phasor-Signature Matching for Detection and Classification of Open-Phase Conditions on Unloaded Transformers_, Rev 0.**

Rev 0 is frozen for peer review. The manuscript stands on its own; this repository contains the code and numerical inputs used to calculate the field-test example and finite-$r$ sensitivity analysis noted in the paper.

The manuscript itself is not maintained in this repository. A public preprint or publication link will be added here when available.

## Repository contents

| Path | Contents |
|---|---|
| [`src/`](src/) | Reusable numerical functions for the open-phase hypothesis operators and common-rotation-invariant residual calculations. |
| [`examples/`](examples/) | Executable Rev 0 field-test and finite-$r$ sensitivity calculations. |
| [`data/`](data/) | Numerical inputs for the field-test example, with provenance notes. |
| [`references/`](references/) | Rev 0 reference list, source links, and redistributable reference PDFs. |
| [`docs/`](docs/) | Related scholarly documents. |
| [`requirements.txt`](requirements.txt) | Python runtime dependency information. |
| [`CITATION.cff`](CITATION.cff) | Citation metadata for this software repository. |
| [`LICENSE`](LICENSE) | MIT License for the repository software. |

## Reproducing the Rev 0 calculations

The examples are intentionally kept close to the equations and numerical values in the manuscript rather than developed as a general protection-software package.

numpy is required to run the scripts.

### Field-test proof of concept

```bash
python examples/field_test_example.py
```

This script:

- loads the healthy and measured field-test phasors from `data/field_test_phasors.csv`;
- constructs the parameter-free large-$|r|$ hypothesis bank using $q=-1$;
- predicts the healthy and Phase-A-, Phase-B-, and Phase-C-open current vectors;
- removes arbitrary common phasor rotation using the closed-form minimal residual;
- treats the measured Phase-C angle as unknown; and
- evaluates the exact most favorable residual for each hypothesis.

The Rev 0 minimum residuals are:

| Hypothesis | Minimum residual (A) |
|---|---:|
| Healthy | 1.203 |
| Phase A open | 2.019 |
| Phase B open | 1.447 |
| Phase C open | 0.178 |

The Phase-C-open hypothesis is the best match, with a minimum margin of approximately **1.025 A** to the closest competing hypothesis.

The script contains assertions against the Rev 0 values and reports `PASS` when they are reproduced.

### Finite-$r$ sensitivity analysis

```bash
python examples/finite_r_sensitivity.py
```

This script keeps the measured field-test current fixed while replacing the large-$|r|$ approximation with selected finite positive-real values of $r$. For each case it uses

$$
q(r)=\frac{1-r}{r+2}
$$

to reconstruct the hypothesis bank and recompute the residuals.

The calculation is a sensitivity check on the large-$|r|$ approximation used in Rev 0. It is **not** an independent validation of the transformer model.

See [`examples/README.md`](examples/README.md) for additional details.

## Data provenance

The field-test example is reconstructed from previously published open-phase test information. The numerical inputs and their provenance are documented in [`data/README.md`](data/README.md).

The healthy and measured states use independent arbitrary angular references because the detector removes common phasor rotation before comparing the vectors. The measured Phase-C-open current magnitude is known, but its angle is treated as indeterminate, consistent with the source material.

See [`references/README.md`](references/README.md) for the complete Rev 0 bibliography and source links.

## Scope

This repository implements the model-informed open-phase detection calculations developed for an **energized, unloaded transformer with a single open source conductor and no simultaneous phase-to-ground fault**.

It is a transparent research implementation, not production protection or control software.

The analytical and practical limitations of the method—including transformer-model approximations, source and grounding variation, loading, capacitance, sensor error, and the need for broader validation—are discussed in the manuscript.

## Citation

If you use the detection methodology, please cite the associated research paper once a public citation is available.

If you use or adapt the software in this repository, citation metadata are provided in [`CITATION.cff`](CITATION.cff).

## License and third-party material

The software in this repository is released under the [MIT License](LICENSE).

That license applies only to material for which the repository author holds the relevant rights. It does not relicense third-party publications, figures, or other source material. The [`references/`](references/) directory includes local copies only where redistribution appears appropriate; otherwise it provides links to the original source.
