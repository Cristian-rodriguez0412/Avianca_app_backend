from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
import random
import uuid
import os

app = Flask(app.py)
CORS(app)

# MAPEO CIUDADES → IATA
CITY_TO_IATA = {
    "bogota": "BOG",
    "bogotá": "BOG",
    "cartagena": "CTG",
    "medellin": "MDE",
    "medellín": "MDE",
    "cali": "CLO",
    "barranquilla": "BAQ",
}

# DATOS DE VUELOS REALES (BASE)
REAL_FLIGHTS = [
    {"origin": "BOG", "destination": "CTG", "duration": 95, "airline": "Avianca", "flight": "AV032", "base_price": 180},
    {"origin": "BOG", "destination": "MDE", "duration": 55, "airline": "LATAM", "flight": "LA204", "base_price": 95},
    {"origin": "MDE", "destination": "CTG", "duration": 70, "airline": "Avianca", "flight": "AV746", "base_price": 140},
    {"origin": "CLO", "destination": "BOG", "duration": 60, "airline": "Avianca", "flight": "AV838", "base_price": 120},
]

def generate_flights(origin, destination, date_str):
    try:
        date_obj = parse_date(date_str).date()
    except:
        date_obj = datetime.utcnow().date()

    # Buscar vuelos reales para esa ruta
    real_matches = [v for v in REAL_FLIGHTS if v["origin"] == origin and v["destination"] == destination]

    flights = []

    if real_matches:
        # Generar vuelos reales con 3 opciones por día
        for real in real_matches:
            for i in range(3):
                dep = datetime.combine(date_obj, datetime.min.time()) + timedelta(hours=6 + i * 3)
                arr = dep + timedelta(minutes=real["duration"])

                flights.append({
                    "id": str(uuid.uuid4()),
                    "flight_number": real["flight"],
                    "airline": real["airline"],
                    "origin": origin,
                    "destination": destination,
                    "departure": dep.isoformat(),
                    "arrival": arr.isoformat(),
                    "duration_minutes": real["duration"],
                    "price_usd": round(real["base_price"] + random.uniform(-10, 30), 2),
                    "seats_left": random.randint(5, 30)  # SIEMPRE DISPONIBLES
                })
    else:
        # Generar vuelos simulados
        for i in range(3):
            dep = datetime.combine(date_obj, datetime.min.time()) + timedelta(hours=7 + i * 3)
            duration = random.randint(60, 150)
            arr = dep + timedelta(minutes=duration)

            flights.append({
                "id": str(uuid.uuid4()),
                "flight_number": f"AV{random.randint(100,999)}",
                "airline": "Avianca",
                "origin": origin,
                "destination": destination,
                "departure": dep.isoformat(),
                "arrival": arr.isoformat(),
                "duration_minutes": duration,
                "price_usd": round(random.uniform(90, 300), 2),
                "seats_left": random.randint(10, 50)
            })

    return flights


@app.route("/api/flights/search", methods=["GET"])
def search_flights():
    origin_raw = request.args.get("from")
    destination_raw = request.args.get("to")
    date = request.args.get("date")

    if not origin_raw or not destination_raw or not date:
        return jsonify({"error": "Faltan parámetros"}), 400

    # Convertir ciudades a IATA
    origin = CITY_TO_IATA.get(origin_raw.lower(), origin_raw.upper())
    destination = CITY_TO_IATA.get(destination_raw.lower(), destination_raw.upper())

    flights = generate_flights(origin, destination, date)

    return jsonify({
        "meta": {"origin": origin, "destination": destination, "date": date},
        "results": flights
    })


@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "Avianca API funcionando"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
