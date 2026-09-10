# Open-Phase Transformer Detection

Supporting software and reproducibility materials for research on model-informed open-phase detection in unloaded three-phase transformers.

The central research manuscript is ***Model-Informed Open-Phase Detection of Unloaded Transformers***. This repository is intended to make the numerical examples and detection calculations in that work easy to inspect and reproduce.

## Project status

This repository is under active development. The associated manuscript is being prepared for peer review.

The transformer modeling companion and the engineering critique of the reference-fingerprint method are separate supporting works. Their permanent Zenodo citations will be added here when those works are published.

Only the journal manuscript is intended for formal peer review. The companion and critique should be cited as independently published technical works.

## Repository contents

```text
open-phase-transformer-detection/
├── README.md
├── CITATION.cff
├── LICENSE
├── .gitignore
├── requirements.txt
├── src/
│   └── README.md
├── examples/
│   └── README.md
├── data/
│   └── README.md
└── docs/
    └── README.md
```

As the implementation is completed:

* `src/` will contain the reusable open-phase detection calculations.
* `examples/` will contain executable reproductions of numerical examples from the paper.
* `data/` will contain the numerical inputs needed for those examples, together with provenance notes.
* `docs/` will contain links and citation information for the associated manuscript, transformer companion, and fingerprint-method critique.

## Associated research outputs

| Work                                                               | Role                                      | Permanent link                                        |
| ------------------------------------------------------------------ | ----------------------------------------- | ----------------------------------------------------- |
| *Model-Informed Open-Phase Detection of Unloaded Transformers*     | Primary research paper                    | To be added                                           |
| Transformer sequence-component companion                           | Supporting transformer-modeling reference | Zenodo DOI to be added                                |
| Engineering critique of reference-fingerprint open-phase detection | Supporting technical analysis             | Zenodo DOI to be added                                |
| Open-phase detection reproducibility software                      | Code associated with the research paper   | Zenodo DOI to be added after the first GitHub release |

## Reproducing the field-test example

The goal of the first software release is that a reader can reproduce the field-test calculation reported in the paper with a single example script.

The intended workflow will be:

```bash
python -m venv .venv
```

Activate the virtual environment, then install the required packages:

```bash
pip install -r requirements.txt
```

Run the field-test example:

```bash
python examples/field_test_example.py
```

The example will report the predicted current vectors, residual for each open-phase hypothesis, winning hypothesis, and margin to the nearest competing hypothesis.

Exact commands and expected numerical results will be updated when the implementation is frozen for the manuscript.

## Method scope

The implementation is intended as a transparent research and reproducibility reference, not as protection or control software.

The initial implementation focuses on unloaded transformers and the model-informed hypothesis-bank approach developed in the associated paper. Assumptions, transformer-model approximations, and applicability limits are documented in the paper and supporting transformer companion.

## Citation

Citation metadata for this repository is provided in [`CITATION.cff`](CITATION.cff).

After the first archival software release, this section will provide the Zenodo DOI for the exact version accompanying the submitted manuscript.

Readers should cite the research paper for the detection methodology and cite the archived software release when referring specifically to the implementation or reproduced calculations.

## Supporting technical works

### Transformer sequence-component companion

A senior-undergraduate-level companion develops the transformer sequence-component models used to estimate the effective positive- and zero-sequence excitation impedances required by the detection method.

**Citation:** to be added when the Zenodo record is published.

### Engineering critique of the reference-fingerprint method

A separate technical report examines conceptual, mathematical, and practical limitations of the previously published reference-fingerprint open-phase detection approach.

**Citation:** to be added when the Zenodo record is published.

## Data provenance

Any numerical values reconstructed from previously published figures or other third-party sources will be identified in `data/README.md` and in the associated paper.

Licensing statements in this repository apply only to material for which the repository author holds the relevant rights; they do not alter the rights or licenses of cited third-party source material.

## License

The software in this repository is released under the **MIT License**. See [`LICENSE`](LICENSE).

The separately published transformer companion and fingerprint-method critique are intended to be released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license through their respective Zenodo records.
