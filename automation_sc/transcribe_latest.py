#!/usr/bin/env python3
"""
Transcribe the newest WAV in Downloads using faster-whisper (medium, CPU int8).
Outputs: out/{slug}.lyrics.txt and prints to stdout.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
from datetime import datetime

from faster_whisper import WhisperModel

DOWNLOADS = Path('/Users/blackmamba/Downloads')
OUT = Path('out')
OUT.mkdir(exist_ok=True)

def slugify(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = re.sub(r'-{2,}', '-', name).strip('-')
    return name or 'track'

def newest_wav() -> Path:
    wavs = sorted(DOWNLOADS.glob('*.wav'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not wavs:
        raise SystemExit('No WAV files in Downloads')
    return wavs[0]


def main():
    wav = newest_wav()
    slug = slugify(wav.stem)
    print(f"Using WAV: {wav}")
    model = WhisperModel('medium', device='cpu', compute_type='int8')
    segments, info = model.transcribe(str(wav), beam_size=5)
    lines = [seg.text.strip() for seg in segments if seg.text.strip()]
    text = '\n'.join(lines)
    out_txt = OUT / f"{slug}.lyrics.txt"
    out_meta = OUT / f"{slug}.lyrics.json"
    out_txt.write_text(text, encoding='utf-8')
    out_meta.write_text(json.dumps({
        "file": str(wav),
        "slug": slug,
        "language": info.language,
        "duration": info.duration,
        "created": datetime.utcnow().isoformat() + 'Z'
    }, indent=2), encoding='utf-8')
    print('\n--- LYRICS ---')
    print(text)
    print('\nSaved:', out_txt, out_meta)

if __name__ == '__main__':
    main()
