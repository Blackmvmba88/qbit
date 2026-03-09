#!/usr/bin/env python3
"""
Build a SoundCloud paste-ready block using:
- metadata JSON dumped by grab_sc_form.js (fields.json)
- lyrics from transcribe_latest.py (out/<slug>.lyrics.txt)
Choose latest lyrics file if slug isn't provided.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from datetime import datetime

BASE = Path('.')
FIELDS = BASE / 'automation_sc/fields.json'
OUT = Path('out')
DEFAULT_TAGS = ['Reggae','Latin','World','Roots','Vibe','2026']


def pick_latest_lyrics() -> Path:
    files = sorted(OUT.glob('*.lyrics.txt'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise SystemExit('No lyrics files in out/')
    return files[0]


def load_fields():
    if not FIELDS.exists():
        return {}
    data = json.loads(FIELDS.read_text())
    return data

def extract_value(fields, key_like: str):
    for f in fields.get('fields', []):
        hay = ' '.join([
            f.get('name',''), f.get('id',''), f.get('aria',''),
            ' '.join(f.get('labels', [])), f.get('placeholder','')
        ]).lower()
        if key_like in hay:
            return f.get('value','')
    return ''

def main():
    fields = load_fields()
    lyrics_path = pick_latest_lyrics()
    lyrics = lyrics_path.read_text().strip()
    slug = lyrics_path.stem.replace('.lyrics','')
    title = extract_value(fields, 'title') or slug.replace('-', ' ').title()
    artist = extract_value(fields, 'artist') or 'Iyari Gomez'
    genre = extract_value(fields, 'genre') or 'Reggae'
    tags = extract_value(fields, 'tag') or ' '.join(f"#{t}" for t in DEFAULT_TAGS)
    label = extract_value(fields, 'label') or 'BlackMamba RECORDS'
    p_line = extract_value(fields, 'p line') or '2026 BlackMamba RECORDS'
    release_date = extract_value(fields, 'release date') or datetime.utcnow().strftime('%-d %b %Y')

    block = f"""Titulo: {title}
Artista: {artist}
Género: {genre}
Tags: {tags}
Sello / P-line: {label} / {p_line}
Lanzamiento: {release_date}

Descripción (pegar en SC):
{lyrics}

Créditos:
Prod / Mix / Master: (rellenar)
Label: {label}
"""
    out = OUT / f"{slug}.payload.txt"
    out.write_text(block)
    print(block)
    print("\nGuardado en", out)

if __name__ == '__main__':
    main()
