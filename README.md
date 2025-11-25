Avianca mock backend API
========================

This is a minimal Flask-based mock API that implements the endpoints expected by your frontend.

How to run locally:
-------------------
1. python -m venv .venv
2. source .venv/bin/activate   (Linux/macOS) or .venv\Scripts\activate (Windows)
3. pip install -r requirements.txt
4. python app_api.py

For Render:
-----------
- The included render.yaml instructs Render to install dependencies and run `gunicorn wsgi:app`.
- If you prefer, set the Start Command to: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`

Endpoints implemented (mock):
- GET  /api/status
- GET  /api/flights/search
- POST /api/login
- POST /api/consultar_comboboxes
- POST /api/obtener_reserva
- POST /api/reservar
- POST /api/anular_reserva
- POST /api/generar_codigo
- POST /api/generar_matricula
- POST /api/consultar_pasajero