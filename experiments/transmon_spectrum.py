"""Baseline transmon spectrum demonstration."""

from core.transmon import (
    transmon_properties,
)
from core.josephson import PHI0


def main() -> None:
    # Target regime: EJ/EC = 50, EC/h = 0.25 GHz
    ec_over_h_ghz = 0.25
    EJ_over_EC = 50.0

    # Convert to joules
    from core.transmon import PLANCK

    EC = PLANCK * ec_over_h_ghz * 1e9
    EJ = EJ_over_EC * EC

    props = transmon_properties(EJ, EC, n_cut=25)

    critical_current = (2.0 * 3.141592653589793 * EJ) / PHI0

    print(f"EJ/EC = {EJ_over_EC:.0f}")
    print(f"E01 ≈ {props['E01_GHz']:.3f} GHz")
    print(f"alpha ≈ {props['alpha_GHz']*1e3:.0f} MHz")
    print(f"charge dispersion ≈ {props['charge_dispersion_kHz']:.1f} kHz")
    print(f"Implied critical current ≈ {critical_current*1e9:.1f} nA")


if __name__ == "__main__":
    main()
