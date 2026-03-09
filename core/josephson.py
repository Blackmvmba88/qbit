"""Josephson junction relations."""

import math

# Magnetic flux quantum (Wb)
PHI0 = 2.067833848e-15


def josephson_energy(critical_current_amp: float, flux_quantum: float = PHI0) -> float:
    """
    Return Josephson energy EJ in joules using EJ = Phi0 * Ic / (2*pi).
    """
    if critical_current_amp <= 0:
        raise ValueError("Critical current must be positive.")
    return flux_quantum * critical_current_amp / (2.0 * math.pi)


def josephson_inductance(critical_current_amp: float, flux_quantum: float = PHI0) -> float:
    """
    Small-signal Josephson inductance: L_J = Phi0 / (2*pi*Ic).
    """
    if critical_current_amp <= 0:
        raise ValueError("Critical current must be positive.")
    return flux_quantum / (2.0 * math.pi * critical_current_amp)


__all__ = ["PHI0", "josephson_energy", "josephson_inductance"]

