from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Simple in-memory storage for mock reservations and passengers
RESERVATIONS = {}
PASSENGERS = {}

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

@app.route("/api/flights/search", methods=["GET"])
def search_flights():
    frm = request.args.get("from")
    to = request.args.get("to")
    date = request.args.get("date")
    flights = [
        {"flight_id": "AV100", "from": frm, "to": to, "date": date, "price": 120.0},
        {"flight_id": "AV200", "from": frm, "to": to, "date": date, "price": 150.0},
    ]
    return jsonify({"flights": flights})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user = data.get("user")
    token = str(uuid.uuid4())
    return jsonify({"token": token, "user": user})

@app.route("/api/consultar_comboboxes", methods=["POST"])
def consultar_comboboxes():
    return jsonify({
        "airlines": ["Avianca", "FlyHigh", "Skylines"],
        "classes": ["Economy", "Business", "First"],
        "airports": ["BOG", "MDE", "CTG", "CLO"]
    })

@app.route("/api/obtener_reserva", methods=["POST"])
def obtener_reserva():
    data = request.get_json() or {}
    code = data.get("code")
    res = RESERVATIONS.get(code)
    if not res:
        return jsonify({"error": "Reserva no encontrada"}), 404
    return jsonify(res)

@app.route("/api/reservar", methods=["POST"])
def reservar():
    data = request.get_json() or {}
    code = str(uuid.uuid4())[:8]
    RESERVATIONS[code] = {
        "code": code,
        "created_at": datetime.utcnow().isoformat(),
        "data": data
    }
    return jsonify({"success": True, "code": code, "reservation": RESERVATIONS[code]})

@app.route("/api/anular_reserva", methods=["POST"])
def anular_reserva():
    data = request.get_json() or {}
    code = data.get("code")
    if code in RESERVATIONS:
        del RESERVATIONS[code]
        return jsonify({"success": True, "code": code})
    return jsonify({"error": "Reserva no encontrada"}), 404

@app.route("/api/generar_codigo", methods=["POST"])
def generar_codigo():
    code = str(uuid.uuid4())[:8]
    return jsonify({"code": code})

@app.route("/api/generar_matricula", methods=["POST"])
def generar_matricula():
    matricula = "MAT-" + str(uuid.uuid4())[:6].upper()
    return jsonify({"matricula": matricula})

@app.route("/api/consultar_pasajero", methods=["POST"])
def consultar_pasajero():
    data = request.get_json() or {}
    doc = data.get("document")
    return jsonify({"document": doc, "name": "Juan Perez", "status": "OK"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Avianca mock backend running", "status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)