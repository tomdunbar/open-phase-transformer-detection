"""
Finite-r sensitivity of the published Phase-C-open field-test example.

Run from the repository root with:

    python examples/finite_r_sensitivity.py

This script keeps the measured field-test current fixed and changes only the
model-predicted hypothesis currents as r changes.

For each selected positive-real r,

    q(r) = (1-r)/(r+2)

is used to construct the healthy, Phase-A-open, Phase-B-open, and
Phase-C-open predictions from the same healthy reference current.  Those
predictions are compared against the same measured Phase-C-open field-test
vector used by field_test_example.py.

The measured Phase-C current magnitude is known, but its angle is not.
As in field_test_example.py, each hypothesis is therefore given its most
favorable possible measured Phase-C angle.  This is evaluated analytically
with residual_range_with_unknown_phase() rather than with an angular grid.

The purpose of this script is to test whether the field-test classification
depends critically on taking the large-|r| limit.  It is not an independent
validation of the transformer model.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.open_phase_detection import (  # noqa: E402
    operators_from_q,
    phasor,
    predict,
    q_from_r,
    residual_range_with_unknown_phase,
)


DATA_FILE = REPO_ROOT / "data" / "field_test_phasors.csv"

PHASES = ("A", "B", "C")
C_INDEX = 2

# Positive-real finite-r cases used to show how the field-test result changes
# as q moves away from the large-|r| limit q = -1.
R_VALUES = (4.0, 10.0, 20.0, 50.0, 100.0, 200.0)


def load_field_test_data(path: Path):
    """Load the healthy reference and measured Phase-C-open field-test data."""
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))

    by_state = {}
    for row in rows:
        by_state.setdefault(row["state"], {})[row["phase"]] = row

    healthy = np.empty(3, dtype=complex)
    measured = np.zeros(3, dtype=complex)

    for index, phase in enumerate(PHASES):
        row = by_state["healthy_reference"][phase]
        healthy[index] = phasor(
            float(row["magnitude_A"]),
            float(row["angle_deg"]),
        )

    measured_c_magnitude = None

    for index, phase in enumerate(PHASES):
        row = by_state["measured_C_open"][phase]
        magnitude = float(row["magnitude_A"])

        if row["angle_deg"].strip():
            measured[index] = phasor(
                magnitude,
                float(row["angle_deg"]),
            )
        else:
            measured_c_magnitude = magnitude

    if measured_c_magnitude is None:
        raise ValueError(
            "Measured Phase-C magnitude with unknown angle not found."
        )

    return healthy, measured, measured_c_magnitude


def polar_string(value: complex) -> str:
    """Format a complex phasor as magnitude ∠ angle."""
    magnitude = abs(value)

    if np.isclose(magnitude, 0.0):
        return "0"

    angle = np.rad2deg(np.angle(value)) % 360.0
    return f"{magnitude:.4f} ∠ {angle:.1f}°"


def print_vector(label: str, vector: np.ndarray) -> None:
    """Print a three-phase phasor vector."""
    print(label)
    for phase, value in zip(PHASES, vector):
        print(f"  {phase}: {polar_string(value)} A")


def evaluate_r(
    r: float,
    reference: np.ndarray,
    measured_known: np.ndarray,
    measured_c_magnitude: float,
):
    """Evaluate all hypotheses against the fixed field-test measurement."""
    q = q_from_r(r)
    operators = operators_from_q(q)

    predictions = {
        name: predict(reference, operator)
        for name, operator in operators.items()
    }

    residuals = {
        name: residual_range_with_unknown_phase(
            predicted=predicted,
            measured=measured_known,
            unknown_index=C_INDEX,
            unknown_magnitude=measured_c_magnitude,
        )
        for name, predicted in predictions.items()
    }

    ranked = sorted(
        residuals.items(),
        key=lambda item: item[1].minimum,
    )

    winner_name, winner_result = ranked[0]
    runner_up_name, runner_up_result = ranked[1]

    margin = runner_up_result.minimum - winner_result.minimum

    return q, predictions, residuals, winner_name, runner_up_name, margin


def print_case(
    r: float,
    reference: np.ndarray,
    measured_known: np.ndarray,
    measured_c_magnitude: float,
) -> tuple[float, float]:
    """Print one finite-r case in the same style as field_test_example.py."""
    (
        q,
        predictions,
        residuals,
        winner_name,
        runner_up_name,
        margin,
    ) = evaluate_r(
        r=r,
        reference=reference,
        measured_known=measured_known,
        measured_c_magnitude=measured_c_magnitude,
    )

    print(
        f"MODEL-INFORMED OPEN-PHASE DETECTION — "
        f"FIELD TEST WITH r={r:g}, q(r)={q.real:.6f}"
    )
    print("=" * 82)
    print()

    print_vector("Healthy reference current:", reference)
    print()

    print_vector(
        f"Predicted Phase-C-open current using finite-r operator "
        f"(q = {q.real:.6f}):",
        predictions["Phase C open"],
    )
    print()

    print("Measured Phase-C-open current:")
    print(f"  A: {polar_string(measured_known[0])} A")
    print(f"  B: {polar_string(measured_known[1])} A")
    print(f"  C: {measured_c_magnitude:.5f} A, angle unknown")
    print()

    print("Phase-aligned residual over all possible measured Phase-C angles")
    print("-" * 78)
    print(
        f"{'Hypothesis':<18}"
        f"{'Min R (A)':>12}"
        f"{'Max R (A)':>12}"
        f"{'theta_C for min':>20}"
    )
    print("-" * 78)

    for name in (
        "Healthy",
        "Phase A open",
        "Phase B open",
        "Phase C open",
    ):
        result = residuals[name]

        theta_text = (
            "independent"
            if result.angle_for_minimum_deg is None
            else f"{result.angle_for_minimum_deg:.2f}°"
        )

        print(
            f"{name:<18}"
            f"{result.minimum:>12.4f}"
            f"{result.maximum:>12.4f}"
            f"{theta_text:>20}"
        )

    winner_residual = residuals[winner_name].minimum
    runner_up_residual = residuals[runner_up_name].minimum

    print()
    print(f"Winning hypothesis: {winner_name}")
    print(f"Winning residual:   {winner_residual:.6f} A")
    print(
        f"Closest competitor: {runner_up_name} "
        f"({runner_up_residual:.6f} A)"
    )
    print(f"Minimum margin:     {margin:.6f} A")
    print()

    if winner_name != "Phase C open":
        raise AssertionError(
            f"For r={r:g}, the field-test data were classified as "
            f"{winner_name}, not Phase C open."
        )

    return residuals["Phase C open"].minimum, margin


def main() -> None:
    reference, measured_known, measured_c_magnitude = load_field_test_data(
        DATA_FILE
    )

    summary = []

    for r in R_VALUES:
        c_residual, margin = print_case(
            r=r,
            reference=reference,
            measured_known=measured_known,
            measured_c_magnitude=measured_c_magnitude,
        )

        summary.append(
            (
                r,
                q_from_r(r).real,
                c_residual,
                margin,
            )
        )

    print("SUMMARY: FIXED FIELD-TEST MEASUREMENT, FINITE POSITIVE-REAL r")
    print("=" * 82)
    print(
        f"{'r':>8}"
        f"{'q(r)':>12}"
        f"{'C-open R (A)':>18}"
        f"{'Minimum margin (A)':>22}"
        f"{'Winner':>18}"
    )
    print("-" * 82)

    for r, q, c_residual, margin in summary:
        print(
            f"{r:>8g}"
            f"{q:>12.3f}"
            f"{c_residual:>18.3f}"
            f"{margin:>22.3f}"
            f"{'Phase C open':>18}"
        )

    print()
    print(
        "PASS: Phase C open is the winning hypothesis for every finite-r "
        "case in the declared positive-real sensitivity sweep."
    )
    print()
    print(
        "Interpretation: the measured fault record is unchanged throughout "
        "this test. Only the model-predicted hypothesis currents change as "
        "r, and therefore q(r), changes."
    )


if __name__ == "__main__":
    main()
