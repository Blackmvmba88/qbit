"""Estimate dispersive shift chi and resonator pull due to qubit state."""

from core.cqed import dispersive_shift, resonator_frequencies_with_qubit


def main() -> None:
    omega_r = 6.5  # GHz resonator
    omega_q = 7.5  # GHz qubit
    g = 0.05       # GHz coupling

    delta = omega_q - omega_r
    chi = dispersive_shift(g, delta)
    omega_g, omega_e = resonator_frequencies_with_qubit(omega_r, chi)

    print("Dispersive shift estimation")
    print(f"omega_r = {omega_r:.3f} GHz, omega_q = {omega_q:.3f} GHz, g = {g:.3f} GHz")
    print(f"Delta = {delta:.3f} GHz")
    print(f"chi = g^2/Delta ≈ {chi:.6f} GHz")
    print(f"Resonator freq |g>: {omega_g:.6f} GHz")
    print(f"Resonator freq |e>: {omega_e:.6f} GHz")


if __name__ == "__main__":
    main()

