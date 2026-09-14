# Open-Phase Transformer Detection Repository
This repository is a companion to the paper:

**Tom Dunbar, _Model-Informed Phasor-Signature Matching for Detection and Classification of Open-Phase Conditions on Unloaded Transformers_, Rev 0.**

Rev 0 of paper has been submitted to IEEE Transactions on Power Delivery for peer review.  

## Scope
The materials in this repository such as code, numerical inputs, sensitivity analysis, and related reference material are seperate from the paper. The paper stands on its own.
This repository is only intened to ease review and implementation of the paper.

The code in this repository is a transparent research implementation. It is not intenteded as protection or control system software.

The manuscript itself is not maintained in this repository. A public preprint or publication link will be added here when available.

## Repository contents

| Path | Contents |
|---|---|
| [`src/`](src/) | Reusable numerical functions for the open-phase hypothesis operators and common-rotation-invariant residual calculations. |
| [`examples/`](examples/) | Executable Rev 0 field-test and finite-$r$ sensitivity calculations. |
| [`data/`](data/) | Numerical inputs for the field-test example, with provenance notes. |
| [`references/`](references/) | Rev 0 reference list, source links, and redistributable reference PDFs. |
| [`requirements.txt`](requirements.txt) | Python runtime dependency information. |
| [`CITATION.cff`](CITATION.cff) | Citation metadata for this software repository. |
| [`LICENSE`](LICENSE) | MIT License for the repository software. |


## Field-test Proof of Concept Script

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

The script contains assertions against the Rev 0 values and reports `PASS` when they are reproduced.

See [`examples/README.md`](examples/README.md) for additional details.

## Finite-$r$ Sensitivity Analysis Script

```bash
python examples/finite_r_sensitivity.py
```

This script keeps the measured field-test current fixed while replacing the large-$|r|$ approximation with selected finite positive-real values of $r$. For each case it uses

$$
q(r)=\frac{1-r}{r+2}
$$

to reconstruct the hypothesis bank and recompute the residuals.

The calculation is a sensitivity check on the large-$|r|$ approximation used in Rev 0.

See [`examples/README.md`](examples/README.md) for additional details.

## Data

The field-test example is reconstructed from previously published open-phase test information. The numerical inputs and their provenance are documented in [`data/README.md`](data/README.md).

The healthy and measured states use independent arbitrary angular references. The measured Phase-C-open current magnitude is known, but its angle is treated as indeterminate, consistent with the source material.

## References
For the complete Rev 0 bibliography and source links, see [`references/README.md`](../references/README.md).

# Related Documents
The broader open-phase project also includes separate supporting documents:

- **Transformer sequence-component companion**  
   Supporting technical material on transformer sequence models and estimation of the effective zero-/positive-sequence input relationship used by the detection method. A public link will be added when available.

- **Engineering critique of reference-fingerprint open-phase detection**  
   Separate technical analysis of reference-current/fingerprint-based open-phase detection. A public link will be added when available.

These documents are intentionally maintained as separate scholarly works. This repository does not depend on the companion or critique documents.

# Citation

If you use the detection methodology, please cite the associated research paper once a public citation is available.

If you use or adapt the software in this repository, citation metadata are provided in [`CITATION.cff`](CITATION.cff).

# License and third-party material

The software in this repository is released under the [MIT License](LICENSE).

That license applies only to material for which the repository author holds the relevant rights. It does not relicense third-party publications, figures, or other source material. The [`references/`](references/) directory includes local copies only where redistribution appears appropriate; otherwise it provides links to the original source.
