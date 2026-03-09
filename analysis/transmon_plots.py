"""Plot transmon sweep results."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_csv(path: Path):
    with path.open() as f:
        reader = csv.DictReader(f)
        rows = [{k: float(v) for k, v in row.items()} for row in reader]
    return rows


def plot(rows, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    x = np.array([r["EJ_over_EC"] for r in rows])
    e01 = np.array([r["E01_GHz"] for r in rows])
    alpha = np.array([r["alpha_MHz"] for r in rows])
    disp = np.array([r["charge_dispersion_kHz"] for r in rows])

    plt.figure(figsize=(5.5, 3.5))
    plt.plot(x, e01, marker="o")
    plt.xlabel("EJ/EC")
    plt.ylabel("E01 (GHz)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    e01_path = out_dir / "e01_vs_ej_ec.png"
    plt.savefig(e01_path, dpi=160)

    plt.figure(figsize=(5.5, 3.5))
    plt.plot(x, alpha, marker="o", color="tomato")
    plt.xlabel("EJ/EC")
    plt.ylabel("alpha (MHz)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    alpha_path = out_dir / "alpha_vs_ej_ec.png"
    plt.savefig(alpha_path, dpi=160)

    plt.figure(figsize=(5.5, 3.5))
    plt.semilogy(x, np.abs(disp), marker="o", color="purple")
    plt.xlabel("EJ/EC")
    plt.ylabel("Charge dispersion (kHz)")
    plt.grid(True, alpha=0.3, which="both")
    plt.tight_layout()
    disp_path = out_dir / "dispersion_vs_ej_ec.png"
    plt.savefig(disp_path, dpi=160)

    return e01_path, alpha_path, disp_path


def main():
    parser = argparse.ArgumentParser(description="Plot transmon sweep CSV.")
    parser.add_argument("--csv", type=Path, default=Path("data/transmon_sweep.csv"), help="Input CSV path.")
    parser.add_argument("--out", type=Path, default=Path("plots"), help="Output directory for PNGs.")
    args = parser.parse_args()

    rows = load_csv(args.csv)
    if not rows:
        raise SystemExit(f"No data rows in {args.csv}")

    paths = plot(rows, args.out)
    print("Saved plots:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()

