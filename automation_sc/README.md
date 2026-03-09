# SoundCloud auto-packager (sin credenciales)

Componentes:
- `grab_sc_form.js`: conecta a Chrome abierto con `--remote-debugging-port=9222` y vuelca los campos del formulario de edición de SoundCloud (DOM, no OCR) a JSON.
- `transcribe_latest.py`: toma el WAV más reciente en `~/Downloads`, transcribe con Whisper (medium, CPU int8) y guarda `out/<slug>.lyrics.txt`.
- `build_payload.py`: combina `fields.json` + letras para generar un bloque listo para pegar en SoundCloud (`out/<slug>.payload.txt`).

Prereqs:
- Node + `npx playwright install chromium` (si no está ya).
- Python venv en este folder (`.venv`) con `faster-whisper` ya instalado.
- Chrome abierto con tu sesión de SoundCloud y la página de edición de la pista, lanzado con `--remote-debugging-port=9222`.

Uso rápido:
```bash
# 0) Lanzar Chrome con depuración
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# 1) Volcar formulario (deja abierta la pestaña de edición de la pista)
node automation_sc/grab_sc_form.js > automation_sc/fields.json

# 2) Transcribir el WAV más reciente en Downloads
source .venv/bin/activate
python automation_sc/transcribe_latest.py

# 3) Generar bloque de metadatos para pegar en SC
python automation_sc/build_payload.py

# Archivos resultantes en ./out/
```

Notas:
- `grab_sc_form.js` no pide credenciales; usa tu sesión ya abierta.
- Si quieres cover auto, añade `OPENAI_API_KEY` y luego podemos extender con `imagegen`.
