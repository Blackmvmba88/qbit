"""Validation for LC resonance calculation."""

from core.lc_resonator import resonance_frequency


def run_validation() -> float:
    # Example parameters (typical microwave LC resonator scale)
    inductance_h = 10e-9   # 10 nH
    capacitance_f = 100e-15  # 100 fF

    calc = resonance_frequency(inductance_h, capacitance_f)
    expected = 1.0 / (2.0 * 3.141592653589793 * (inductance_h * capacitance_f) ** 0.5)
    rel_err = abs(calc - expected) / expected * 100.0
    return rel_err


def main() -> None:
    rel_err = run_validation()
    status = "PASS" if rel_err < 1e-9 else "FAIL"
    print("Validation", status)
    print(f"RMS error: {rel_err:.4e}%")


if __name__ == "__main__":
    main()

