#!/usr/bin/env python3
"""Batch wrapper over blender-headless-web pipeline.

For each .blend in a directory, runs the official pipeline script to export
GLB + thumbnail + metadata and a self-contained viewer under
<workspace>/web/<piece>/.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

PIPELINE = Path("/Users/blackmamba/.codex/skills/blender-headless-web/scripts/pipeline.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch export .blend files to web viewers")
    parser.add_argument("--blends-dir", required=True, help="Directory containing .blend files")
    parser.add_argument("--workspace", default=".", help="Workspace root where web/ will be created")
    parser.add_argument("--web-dir", default="web", help="Base web directory under workspace")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subdirectories for .blend files")
    parser.add_argument("--draco", action="store_true", help="Request Draco compression if supported")
    parser.add_argument("--overwrite-viewer", action="store_true", help="Overwrite viewer files when present")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--samples", type=int, default=120)
    parser.add_argument("--frame", type=int, default=1)
    parser.add_argument("--format", choices=["JPEG", "PNG", "WEBP"], default="JPEG")
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--limit", type=int, default=0, help="Process at most N blends (0 = all)")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def discover_blends(root: Path, recursive: bool) -> List[Path]:
    pattern = "**/*.blend" if recursive else "*.blend"
    return sorted(p for p in root.glob(pattern) if p.is_file())


def run_pipeline(blend: Path, workspace: Path, web_dir: str, args: argparse.Namespace) -> subprocess.CompletedProcess:
    piece = blend.stem
    piece_web = workspace / web_dir / piece
    piece_assets = piece_web / "assets"
    piece_assets.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(PIPELINE),
        "--blend",
        str(blend.resolve()),
        "--workspace",
        str(workspace),
        "--web-dir",
        str(piece_web.relative_to(workspace)),
        "--assets-dir",
        "assets",
        "--frame",
        str(max(1, args.frame)),
        "--width",
        str(max(16, args.width)),
        "--height",
        str(max(16, args.height)),
        "--samples",
        str(max(1, args.samples)),
        "--format",
        args.format,
        "--quality",
        str(max(1, min(100, args.quality))),
    ]

    if args.draco:
        cmd.append("--draco")
    if args.overwrite_viewer:
        cmd.append("--overwrite-viewer")
    if args.verbose:
        cmd.append("--verbose")

    return subprocess.run(cmd, capture_output=not args.verbose, text=True)


def main() -> int:
    args = parse_args()

    blends_dir = Path(args.blends_dir).expanduser().resolve()
    if not blends_dir.is_dir():
        print(f"[error] blends-dir no existe: {blends_dir}")
        return 1

    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    blends = discover_blends(blends_dir, args.recursive)
    if not blends:
        print(f"[warn] No se encontraron .blend en {blends_dir}")
        return 0

    if args.limit > 0:
        blends = blends[: args.limit]

    results = []
    for blend in blends:
        print(f"[run] {blend}")
        res = run_pipeline(blend, workspace, args.web_dir, args)
        results.append((blend, res.returncode, res.stderr))
        if res.returncode != 0 and not args.verbose:
            print(f"  -> fallo (code {res.returncode}): {res.stderr.strip() if res.stderr else 'sin stderr'}")

    ok = sum(1 for _, code, _ in results if code == 0)
    fail = len(results) - ok
    print(f"[done] {ok} ok / {fail} fallos")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
