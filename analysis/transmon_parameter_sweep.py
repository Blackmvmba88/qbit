"""Parameter sweep for transmon properties."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

from core.transmon import PLANCK, transmon_properties


def sweep(ej_ec_values, ec_over_h_ghz: float, n_cut: int):
    EC = PLANCK * ec_over_h_ghz * 1e9
    rows = []
    for ratio in ej_ec_values:
        EJ = ratio * EC
        props = transmon_properties(EJ, EC, n_cut=n_cut)
        rows.append(
            {
                "EJ_over_EC": ratio,
                "E01_GHz": props["E01_GHz"],
                "alpha_MHz": props["alpha_GHz"] * 1e3,
                "charge_dispersion_kHz": props["charge_dispersion_kHz"],
            }
        )
    return rows


def write_csv(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["EJ_over_EC", "E01_GHz", "alpha_MHz", "charge_dispersion_kHz"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Sweep transmon properties over EJ/EC ratios.")
    parser.add_argument("--ej-ec-start", type=float, default=20.0, help="Start ratio (inclusive).")
    parser.add_argument("--ej-ec-stop", type=float, default=80.0, help="Stop ratio (inclusive).")
    parser.add_argument("--num", type=int, default=16, help="Number of points in the sweep.")
    parser.add_argument("--ec-over-h-ghz", type=float, default=0.25, help="EC/h in GHz.")
    parser.add_argument("--n-cut", type=int, default=25, help="Charge basis cutoff.")
    parser.add_argument("--out", type=Path, default=Path("data/transmon_sweep.csv"), help="Output CSV path.")
    args = parser.parse_args()

    ratios = np.linspace(args.ej_ec_start, args.ej_ec_stop, args.num)
    rows = sweep(ratios, args.ec_over_h_ghz, args.n_cut)
    write_csv(rows, args.out)

    print(f"Wrote {len(rows)} rows to {args.out}")
    if len(rows) >= 2:
        print(f"EJ/EC range: {rows[0]['EJ_over_EC']:.2f} .. {rows[-1]['EJ_over_EC']:.2f}")
        print(f"E01 range (GHz): {rows[0]['E01_GHz']:.3f} .. {rows[-1]['E01_GHz']:.3f}")
        print(f"alpha range (MHz): {rows[0]['alpha_MHz']:.1f} .. {rows[-1]['alpha_MHz']:.1f}")


if __name__ == "__main__":
    main()

