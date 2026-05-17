import os
from flask import Flask, request, jsonify

app = Flask(__name__)
SECURE_TOKEN = "CZ_SOVEREIGN_HEXA_SHIELD_V2.9"

@app.route('/')
def home():
    return "CZ Sovereign Core Gatekeeper is LIVE."

@app.route('/cz-secure-node', methods=['POST'])
def secure_node():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {SECURE_TOKEN}":
        return jsonify({"status": "DENIED", "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    volume = data.get("evidence_volume", 100)
    noise = data.get("bias_noise", 0.0)

    cz_cost = (volume * 0.01) * 0.10 + (noise * 0.001)
    traditional_cost = (volume * 0.12) + 50.0
    savings = (1.0 - (cz_cost / traditional_cost)) * 100.0

    return jsonify({
        "status": "SUCCESS",
        "cz_cost": round(cz_cost, 4),
        "traditional_cost": round(traditional_cost, 2),
        "savings": f"{round(savings, 2)}%"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
