"""Simulate dispersive readout response for qubit states |0> and |1>."""

import numpy as np
import matplotlib.pyplot as plt

from core.readout import dispersive_shift, readout_response, state_distinguishability


def main() -> None:
    omega_r = 6.5e9      # Hz
    omega_q = 5.2e9      # Hz
    g = 100e6            # Hz
    kappa = 1e6          # Hz (linewidth)
    drive_eps = 1.0e6    # arbitrary drive amplitude

    delta = omega_q - omega_r
    chi = dispersive_shift(g, delta)

    # Sweep drive frequency around cavity
    span = 30e6
    omega_ds = np.linspace(omega_r - span, omega_r + span, 400)
    alpha_g = []
    alpha_e = []
    for od in omega_ds:
        alpha_g.append(readout_response(omega_r, chi, od, kappa, drive_eps, qubit_state=0))
        alpha_e.append(readout_response(omega_r, chi, od, kappa, drive_eps, qubit_state=1))
    alpha_g = np.array(alpha_g)
    alpha_e = np.array(alpha_e)

    amp_g = np.abs(alpha_g)
    amp_e = np.abs(alpha_e)
    phase_g = np.angle(alpha_g)
    phase_e = np.angle(alpha_e)

    # Distinguishability at cavity resonance
    d_peak = state_distinguishability(alpha_g[np.argmax(amp_g)], alpha_e[np.argmax(amp_e)])

    print("Dispersive readout demo")
    print(f"omega_r = {omega_r/1e9:.3f} GHz, omega_q = {omega_q/1e9:.3f} GHz, g = {g/1e6:.1f} MHz")
    print(f"Delta = {delta/1e9:.3f} GHz, chi = {chi/1e6:.3f} MHz")
    print(f"Peak distinguishability |alpha_e - alpha_g| ≈ {d_peak:.3e}")

    plt.figure(figsize=(6, 4))
    plt.plot((omega_ds - omega_r) / 1e6, amp_g, label="|0>")
    plt.plot((omega_ds - omega_r) / 1e6, amp_e, label="|1>")
    plt.xlabel("Drive detuning from ωr (MHz)")
    plt.ylabel("|alpha|")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("plots/readout_amp.png", dpi=160)

    plt.figure(figsize=(6, 4))
    plt.plot((omega_ds - omega_r) / 1e6, phase_g, label="|0>")
    plt.plot((omega_ds - omega_r) / 1e6, phase_e, label="|1>")
    plt.xlabel("Drive detuning from ωr (MHz)")
    plt.ylabel("Phase (rad)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("plots/readout_phase.png", dpi=160)

    print("Saved plots/readout_amp.png and plots/readout_phase.png")


if __name__ == "__main__":
    main()

