"""
Core calculations for model-informed open-phase detection.

This module implements the compact symmetric-transformer operators used in
the associated paper.  It is intentionally small and explicit so that the
reproducibility calculation can be inspected directly.

The current operators are

    q(r) = (1 - r) / (r + 2)

and

               [0  0  0]          [1  q  0]          [1  0  q]
    T_A(q)  =  [q  1  0]  T_B(q)= [0  0  0]  T_C(q)= [0  1  q]
               [q  0  1]          [0  q  1]          [0  0  0]

For the large-|r| limit used in the published field-test proof of concept,
q -> -1.

The phase-aligned residual for predicted vector p and measured vector m is

    R^2 = p^H p + m^H m - 2 |p^H m|,

which is the minimum Euclidean mismatch after arbitrary common phasor
rotation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np


Array = np.ndarray


def phasor(magnitude: float, angle_degrees: float) -> complex:
    """Return a complex phasor from magnitude and angle in degrees."""
    return magnitude * np.exp(1j * np.deg2rad(angle_degrees))


def q_from_r(r: complex) -> complex:
    """Return q(r) = (1-r)/(r+2) for a finite complex admittance ratio r."""
    if np.isclose(r + 2, 0):
        raise ValueError("q(r) is singular at r = -2.")
    return (1 - r) / (r + 2)


def operators_from_q(q: complex) -> Dict[str, Array]:
    """Return healthy, A-open, B-open, and C-open current operators."""
    return {
        "Healthy": np.eye(3, dtype=complex),
        "Phase A open": np.array(
            [[0, 0, 0],
             [q, 1, 0],
             [q, 0, 1]],
            dtype=complex,
        ),
        "Phase B open": np.array(
            [[1, q, 0],
             [0, 0, 0],
             [0, q, 1]],
            dtype=complex,
        ),
        "Phase C open": np.array(
            [[1, 0, q],
             [0, 1, q],
             [0, 0, 0]],
            dtype=complex,
        ),
    }


def large_r_operators() -> Dict[str, Array]:
    """Return the parameter-free large-|r| operator bank (q = -1)."""
    return operators_from_q(-1.0)


def predict(reference_current: Array, operator: Array) -> Array:
    """Apply a current operator to a three-phase healthy reference vector."""
    reference_current = np.asarray(reference_current, dtype=complex)
    operator = np.asarray(operator, dtype=complex)

    if reference_current.shape != (3,):
        raise ValueError("reference_current must be a length-3 vector.")
    if operator.shape != (3, 3):
        raise ValueError("operator must be a 3x3 matrix.")

    return operator @ reference_current


def phase_aligned_residual(predicted: Array, measured: Array) -> float:
    """
    Minimum Euclidean residual after arbitrary common phasor rotation.

    Equivalent to

        min_phi || measured - exp(j phi) predicted ||_2.

    The minimization is evaluated in closed form.
    """
    predicted = np.asarray(predicted, dtype=complex)
    measured = np.asarray(measured, dtype=complex)

    if predicted.shape != measured.shape:
        raise ValueError("predicted and measured vectors must have equal shape.")

    inner_product_magnitude = abs(np.vdot(predicted, measured))
    residual_squared = (
        np.vdot(predicted, predicted).real
        + np.vdot(measured, measured).real
        - 2.0 * inner_product_magnitude
    )

    # Roundoff can produce a tiny negative value for an exact match.
    return float(np.sqrt(max(0.0, residual_squared)))


@dataclass(frozen=True)
class UnknownPhaseResidual:
    """Residual extrema when one measured phasor angle is unknown."""

    minimum: float
    maximum: float
    angle_for_minimum_deg: Optional[float]
    angle_for_maximum_deg: Optional[float]


def residual_range_with_unknown_phase(
    predicted: Array,
    measured: Array,
    unknown_index: int,
    unknown_magnitude: float,
) -> UnknownPhaseResidual:
    """
    Find the exact residual range when one measured phase angle is unknown.

    Parameters
    ----------
    predicted:
        Three-phase predicted complex current vector.
    measured:
        Three-phase measured vector.  The value at unknown_index is ignored.
    unknown_index:
        Index (0=A, 1=B, 2=C) whose measured angle is unavailable.
    unknown_magnitude:
        Known magnitude of that measured current.

    Notes
    -----
    Let

        p^H m(theta) = S + conj(p_u) M_u exp(j theta),

    where u is the unknown-angle phase.  The residual is minimized when the
    second term aligns with S and maximized when it anti-aligns.  Therefore no
    numerical angular sweep is needed.
    """
    predicted = np.asarray(predicted, dtype=complex)
    measured = np.asarray(measured, dtype=complex)

    if predicted.shape != (3,) or measured.shape != (3,):
        raise ValueError("predicted and measured must be length-3 vectors.")
    if unknown_index not in (0, 1, 2):
        raise ValueError("unknown_index must be 0, 1, or 2.")
    if unknown_magnitude < 0:
        raise ValueError("unknown_magnitude must be nonnegative.")

    known = [i for i in range(3) if i != unknown_index]

    # Contribution from measured phases whose magnitude and angle are known.
    S = sum(np.conj(predicted[i]) * measured[i] for i in known)

    # Magnitude of the unknown-phase contribution to p^H m.
    d_magnitude = abs(predicted[unknown_index]) * unknown_magnitude

    measured_norm_squared = (
        sum(abs(measured[i]) ** 2 for i in known) + unknown_magnitude**2
    )
    norm_sum = (
        np.vdot(predicted, predicted).real + measured_norm_squared
    )

    max_inner_product = abs(S) + d_magnitude
    min_inner_product = abs(abs(S) - d_magnitude)

    r_min = float(np.sqrt(max(0.0, norm_sum - 2.0 * max_inner_product)))
    r_max = float(np.sqrt(max(0.0, norm_sum - 2.0 * min_inner_product)))

    # If the predicted current on the unknown phase is zero, its measured
    # angle cannot affect the inner product or the residual.
    if np.isclose(abs(predicted[unknown_index]), 0.0) or np.isclose(
        unknown_magnitude, 0.0
    ):
        theta_min = None
        theta_max = None
    elif np.isclose(abs(S), 0.0):
        # With S=0 the magnitude is angle-independent.
        theta_min = None
        theta_max = None
    else:
        theta_min = float(
            np.rad2deg(np.angle(S) + np.angle(predicted[unknown_index])) % 360.0
        )
        theta_max = float((theta_min + 180.0) % 360.0)

    return UnknownPhaseResidual(
        minimum=r_min,
        maximum=r_max,
        angle_for_minimum_deg=theta_min,
        angle_for_maximum_deg=theta_max,
    )
