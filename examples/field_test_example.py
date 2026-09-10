"""
Reproduce the published Phase-C-open field-test proof of concept.

Run from the repository root with:

    python examples/field_test_example.py

The example uses the public field-test/patent phasors reported in the
associated manuscript, constructs the parameter-free large-|r| hypothesis
bank (q = -1), and calculates the phase-aligned residual for each hypothesis.

The measured Phase-C current magnitude is known, but its relative angle was
not reported reliably.  Rather than selecting an arbitrary angle or using a
finite angular grid, this script calculates the exact minimum and maximum
residual over all possible Phase-C angles for each hypothesis.

Only NumPy is required.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.open_phase_detection import (  # noqa: E402
    large_r_operators,
    phasor,
    predict,
    residual_range_with_unknown_phase,
)


DATA_FILE = REPO_ROOT / "data" / "field_test_phasors.csv"

PHASES = ("A", "B", "C")
C_INDEX = 2


def load_field_test_data(path: Path):
    """Load healthy and measured Phase-C-open phasors from the CSV file."""
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
            measured[index] = phasor(magnitude, float(row["angle_deg"]))
        else:
            measured_c_magnitude = magnitude

    if measured_c_magnitude is None:
        raise ValueError("Measured Phase-C magnitude with unknown angle not found.")

    return healthy, measured, measured_c_magnitude


def polar_string(value: complex) -> str:
    """Format a complex phasor as magnitude ∠ angle."""
    magnitude = abs(value)
    if np.isclose(magnitude, 0.0):
        return "0"
    angle = np.rad2deg(np.angle(value)) % 360.0
    return f"{magnitude:.4f} ∠ {angle:.1f}°"


def print_vector(label: str, vector: np.ndarray) -> None:
    print(label)
    for phase, value in zip(PHASES, vector):
        print(f"  {phase}: {polar_string(value)} A")


def main() -> None:
    reference, measured_known, measured_c_magnitude = load_field_test_data(DATA_FILE)

    operators = large_r_operators()
    predictions = {
        name: predict(reference, operator)
        for name, operator in operators.items()
    }

    print("MODEL-INFORMED OPEN-PHASE DETECTION")
    print("Published Phase-C-open field-test proof of concept")
    print("=" * 66)
    print()

    print_vector("Healthy reference current:", reference)
    print()

    print_vector(
        "Predicted Phase-C-open current using the large-|r| operator (q = -1):",
        predictions["Phase C open"],
    )
    print()

    print("Measured Phase-C-open current:")
    print(f"  A: {polar_string(measured_known[0])} A")
    print(f"  B: {polar_string(measured_known[1])} A")
    print(f"  C: {measured_c_magnitude:.5f} A, angle unknown")
    print()

    results = {}
    for name, predicted in predictions.items():
        results[name] = residual_range_with_unknown_phase(
            predicted=predicted,
            measured=measured_known,
            unknown_index=C_INDEX,
            unknown_magnitude=measured_c_magnitude,
        )

    print("Phase-aligned residual over all possible measured Phase-C angles")
    print("-" * 78)
    print(
        f"{'Hypothesis':<18}"
        f"{'Min R (A)':>12}"
        f"{'Max R (A)':>12}"
        f"{'theta_C for min':>20}"
    )
    print("-" * 78)

    for name, result in results.items():
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

    print()

    ranked = sorted(results.items(), key=lambda item: item[1].minimum)
    winner_name, winner_result = ranked[0]
    runner_up_name, runner_up_result = ranked[1]
    minimum_margin = runner_up_result.minimum - winner_result.minimum

    print(f"Winning hypothesis: {winner_name}")
    print(f"Winning residual:   {winner_result.minimum:.6f} A")
    print(
        f"Closest competitor: {runner_up_name} "
        f"({runner_up_result.minimum:.6f} A)"
    )
    print(f"Minimum margin:     {minimum_margin:.6f} A")
    print()

    # Manuscript values are rounded to three decimals.  These checks make the
    # script a lightweight reproducibility test as well as a worked example.
    expected_minima = {
        "Healthy": 1.203,
        "Phase A open": 2.019,
        "Phase B open": 1.447,
        "Phase C open": 0.178,
    }
    expected_margin = 1.025

    tolerance = 0.0006
    for name, expected in expected_minima.items():
        actual = results[name].minimum
        if not np.isclose(actual, expected, atol=tolerance, rtol=0.0):
            raise AssertionError(
                f"{name}: calculated minimum residual {actual:.6f} A "
                f"does not reproduce manuscript value {expected:.3f} A."
            )

    if not np.isclose(minimum_margin, expected_margin, atol=tolerance, rtol=0.0):
        raise AssertionError(
            f"Calculated minimum margin {minimum_margin:.6f} A "
            f"does not reproduce manuscript value {expected_margin:.3f} A."
        )

    print("Reproducibility checks against manuscript values: PASS")
    print()
    print(
        "Note: the unknown measured Phase-C angle is optimized independently "
        "for each hypothesis. This gives every competing hypothesis its most "
        "favorable possible residual."
    )


if __name__ == "__main__":
    main()
