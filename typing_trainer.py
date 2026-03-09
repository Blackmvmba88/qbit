#!/usr/bin/env python3
"""
Terminal typing drill for taquimecanografía.
- Sin dependencias externas (solo estándar de Python).
- Mide WPM y precisión por sesión.
- Permite usar un archivo de frases propio con --archivo texto.txt.
- Guarda historial opcional en ~/.cache/typing-trainer/sessions.csv
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List, Optional

# ANSI color helpers (sin dependencias externas).
class Color:
    RESET = "\033[0m"
    NEON_PINK = "\033[95;1m"
    NEON_CYAN = "\033[96;1m"
    NEON_LIME = "\033[92;1m"
    NEON_YELLOW = "\033[93;1m"
    DIM = "\033[2m"


def c(text: str, color: str) -> str:
    return f"{color}{text}{Color.RESET}"

# Pequeño banco de palabras y frases en español.
SPANISH_PHRASES = [
    "El veloz murciélago hindú comía feliz cardillo y kiwi.",
    "Jovencillo emponzoñado de whisky: ¡qué figurota exhibe!",
    "La cigüeña tocaba el saxofón detrás del palenque de paja.",
    "Miércoles y jueves serán los días con mayor flujo vehicular.",
    "Practicar todos los días sostiene el hábito de escribir rápido.",
    "Siempre coloca los dedos base en las teclas guía: a s d f y ñ l k.",
    "Respira hondo, baja la tensión en hombros y muñecas.",
    "El ritmo constante importa más que la velocidad máxima.",
    "Quien teclea despacio al principio gana precisión para siempre.",
    "Cada error es una señal; corrige la postura y continúa.",
]

# Descompone frases en palabras limpias para construir prompts aleatorios.
def build_word_bank(phrases: Iterable[str]) -> List[str]:
    bank = []
    for sentence in phrases:
        cleaned = ''.join(ch.lower() if ch.isalpha() or ch == ' ' else ' ' for ch in sentence)
        for word in cleaned.split():
            if len(word) > 1:  # evita partículas de una sola letra
                bank.append(word)
    return bank

WORD_BANK = build_word_bank(SPANISH_PHRASES)


TYPEWRITER_ART = [
    "      ______________",
    "     / ____________ \\",
    "    / /##########\\ \\",
    "    | |##|    |##| |",
    "    | |##|____|##| |",
    "    \\ \\##########/ /",
    "     \\____________/",
    "      |  |    |  |",
    "      |__|____|__|",
    "      [__________]",
]


def generate_prompt(word_count: int, custom_lines: Optional[List[str]]) -> str:
    """Crea un texto breve para practicar."""
    if custom_lines:
        return random.choice(custom_lines).strip()
    words = random.choices(WORD_BANK, k=word_count)
    prompt = ' '.join(words)
    return prompt[0].upper() + prompt[1:] + '.'


def print_banner(log_summary: Optional[tuple[int, float, float]]):
    colors = [Color.NEON_PINK, Color.NEON_CYAN, Color.NEON_LIME, Color.NEON_YELLOW]
    print()
    for i, line in enumerate(TYPEWRITER_ART):
        print(c(line, colors[i % len(colors)]))
    print(c("    máquina de escribir en modo neón — foco y ritmo\n", Color.NEON_LIME))
    if log_summary:
        sessions, minutes, last_wpm = log_summary
        print(c(f"Historial: {sessions} sesiones · {minutes:.1f} min · última {last_wpm:.1f} WPM\n", Color.DIM))


def measure(prompt: str, typed: str, elapsed_sec: float):
    # Evita divisiones enormes si el usuario pega texto en milisegundos.
    elapsed_sec = max(elapsed_sec, 0.2)

    correct = sum(1 for a, b in zip(prompt, typed) if a == b)
    extra = max(0, len(typed) - len(prompt))
    missing = max(0, len(prompt) - len(typed))
    errors = (len(prompt) - correct) + extra
    accuracy = (correct / len(prompt) * 100) if prompt else 0.0
    words_typed = len(typed) / 5  # estándar de 5 chars = 1 palabra
    minutes = elapsed_sec / 60
    wpm = words_typed / minutes if minutes > 0 else 0.0
    return {
        "elapsed_sec": elapsed_sec,
        "correct": correct,
        "errors": errors,
        "missing": missing,
        "accuracy": accuracy,
        "wpm": wpm,
    }


def ensure_log_path() -> Path:
    path = Path.home() / ".cache" / "typing-trainer"
    path.mkdir(parents=True, exist_ok=True)
    return path / "sessions.csv"


def load_log_summary(path: Optional[Path]) -> Optional[tuple[int, float, float]]:
    if not path or not path.exists():
        return None
    total_sessions = 0
    total_seconds = 0.0
    last_wpm = 0.0
    try:
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_sessions += 1
                total_seconds += float(row.get("elapsed_sec", 0.0) or 0.0)
                last_wpm = float(row.get("wpm", 0.0) or 0.0)
    except Exception:
        return None
    if total_sessions == 0:
        return None
    return total_sessions, total_seconds / 60, last_wpm


def log_session(path: Path, prompt: str, typed: str, stats: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow([
                "timestamp", "prompt_chars", "typed_chars", "elapsed_sec",
                "accuracy_pct", "wpm", "errors"
            ])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            len(prompt),
            len(typed),
            f"{stats['elapsed_sec']:.2f}",
            f"{stats['accuracy']:.2f}",
            f"{stats['wpm']:.2f}",
            stats['errors'],
        ])


def read_custom_lines(path: Optional[str]) -> Optional[List[str]]:
    if not path:
        return None
    lines = []
    file_path = Path(path).expanduser()
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
    if not lines:
        raise ValueError(f"El archivo {file_path} no contiene texto aprovechable.")
    return lines


def run_once(prompt: str) -> tuple[str, float, datetime]:
    print(c("\n⏩ Texto a copiar:\n", Color.NEON_CYAN))
    print(c(f"  {prompt}\n", Color.NEON_PINK))
    input(c("Presiona Enter para empezar, mide desde tu primer tecla…", Color.NEON_YELLOW))
    print(c("\nEscribe y termina con Enter.\n", Color.NEON_YELLOW))
    start_ts = datetime.now()
    start = time.perf_counter()
    try:
        typed = sys.stdin.readline().rstrip("\n")
    except KeyboardInterrupt:
        print("\nInterrumpido.")
        sys.exit(1)
    elapsed = time.perf_counter() - start
    return typed, elapsed, start_ts


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="Drill de mecanografía en terminal")
    parser.add_argument("--palabras", type=int, default=18,
                        help="Cantidad aproximada de palabras por ejercicio (cuando no hay archivo)")
    parser.add_argument("--archivo", type=str, default=None,
                        help="Ruta a archivo de texto con frases personalizadas (una por línea)")
    parser.add_argument("--sin-log", action="store_true",
                        help="No guardar historial en ~/.cache/typing-trainer/sessions.csv")
    args = parser.parse_args(argv)

    custom_lines = read_custom_lines(args.archivo)
    log_path = ensure_log_path() if not args.sin_log else None
    log_summary = load_log_summary(log_path)

    print_banner(log_summary)
    print(c("=== Taquimecanografía en terminal ===", Color.NEON_LIME))
    print(c("Ctrl+C para salir en cualquier momento.\n", Color.DIM))

    while True:
        prompt = generate_prompt(args.palabras, custom_lines)
        typed, elapsed, started_at = run_once(prompt)
        stats = measure(prompt, typed, elapsed)
        ended_at = started_at + timedelta(seconds=elapsed)

        print(c("\n📊 Resultados:", Color.NEON_LIME))
        print(f"  Reloj:     {started_at:%H:%M:%S} → {ended_at:%H:%M:%S}")
        print(f"  Tiempo:    {stats['elapsed_sec']:.2f} s")
        print(f"  Precisión: {stats['accuracy']:.1f}% (errores: {stats['errors']})")
        print(f"  Velocidad: {stats['wpm']:.1f} WPM")

        if log_path:
            log_session(log_path, prompt, typed, stats)
            print(f"  Guardado en {log_path}")
            log_summary = load_log_summary(log_path)
            if log_summary:
                sessions, minutes, last_wpm = log_summary
                print(c(f"  Acumulado: {sessions} sesiones · {minutes:.1f} min · última {last_wpm:.1f} WPM", Color.DIM))

        again = input("\nOtra ronda? [Enter = sí, q = salir]: ").strip().lower()
        if again == 'q':
            break

    print("\nBuen hábito mantenido. ¡Sigue así!\n")


if __name__ == "__main__":
    main()
