from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
# URL de tu backend real
API_BASE = "https://avianca-connect-fly.lovable.app"


def safe_json(response):
    try:
        return response.json()
    except ValueError:
        # API devolvió HTML, no JSON
        return {
            "error": "La API devolvió HTML en vez de JSON",
            "status_code": response.status_code,
            "raw": response.text[:500]
        }

@app.route("/")
def home():
    try:
        r = requests.get(f"{API_BASE}/api/status")
        status = safe_json(r)
    except Exception as e:
        status = {"error": str(e)}

    return render_template("index.html", status=status)


@app.route("/buscar_vuelos", methods=["POST"])
def buscar_vuelos():
    origen = request.form["origen"]
    destino = request.form["destino"]
    fecha = request.form["fecha"]

    try:
        params = {"from": origen, "to": destino, "date": fecha}
        r = requests.get(f"{API_BASE}/api/flights/search", params=params)
        resultados = safe_json(r)
    except Exception as e:
        resultados = {"error": str(e)}

    return render_template(
        "flights.html",
        origen=origen,
        destino=destino,
        fecha=fecha,
        resultados=resultados
    )


if __name__ == "__main__":
    print("🔥 Frontend Flask conectado a backend Lovable")
    app.run(host="0.0.0.0", port=5000, debug=True)