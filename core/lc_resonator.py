"""LC resonator utilities."""

import math

def resonance_frequency(inductance_henry: float, capacitance_farad: float) -> float:
    """
    Compute the resonance frequency (Hz) of an LC oscillator.
    Formula: f = 1 / (2*pi*sqrt(L*C))
    """
    if inductance_henry <= 0 or capacitance_farad <= 0:
        raise ValueError("Inductance and capacitance must be positive.")
    return 1.0 / (2.0 * math.pi * math.sqrt(inductance_henry * capacitance_farad))


def angular_frequency(inductance_henry: float, capacitance_farad: float) -> float:
    """Return the angular resonance frequency (rad/s)."""
    return 2.0 * math.pi * resonance_frequency(inductance_henry, capacitance_farad)

