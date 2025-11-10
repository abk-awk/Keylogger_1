# simulated_keylogger.py
# Programme pédagogique : SIMULATION du traitement d'événements clavier
# Ne capture PAS le clavier réel ; utilise une liste d'événements simulés.

import threading
import time
import os

# variables globales
log = ""  # buffer en mémoire
path = os.path.join(os.getcwd(), "simulated_log.txt")  # fichier de sortie

# Liste d'événements simulés (chaque "key" est soit une string de 1 char,
# soit des tokens spéciaux comme "<SPACE>", "<ENTER>", "<BACKSPACE>", "<LEFT>")
simulated_events = [
    "H", "e", "l", "l", "o", "<SPACE>",
    "W", "o", "r", "l", "d", "<ENTER>",
    "T", "e", "s", "t", "<BACKSPACE>", "t",
    "<LEFT>", "!", "<ENTER>"
]

def processkeys_simulated(key):
    """
    Simule le comportement d'un callback qui reçoit un 'key' objet.
    key peut être :
      - une chaîne d'un seul caractère (ex: 'a')
      - un token spécial : '<SPACE>', '<ENTER>', '<BACKSPACE>', etc.
    """
    global log
    try:
        # Si key est une chaîne simple d'1 caractère -> concatène
        if isinstance(key, str) and len(key) == 1:
            log += key
        else:
            # gérer les tokens spéciaux
            if key == "<SPACE>":
                log += " "
            elif key == "<ENTER>":
                log += "\n"
            elif key == "<BACKSPACE>":
                # retirer dernier caractère si possible
                if len(log) > 0:
                    log = log[:-1]
            else:
                # autres touches (flèche, ctrl...) -> on ignore (remplace par "")
                log += ""
    except Exception as e:
        # En contexte réel, on capterait AttributeError pour key.char manquant.
        # Ici on affiche l'erreur pour debug pédagogique.
        print("Exception in processkeys_simulated:", e)

def report():
    """
    Fonction qui écrit périodiquement le buffer `log` dans le fichier `path`.
    Ensuite vide le buffer (ou on peut choisir de ne pas vider, selon la logique).
    Lancé dans un thread séparé pour simuler l'écriture en parallèle.
    """
    global log, path
    while True:
        time.sleep(2)  # intervalle d'écriture simulé (2s)
        # obtenir copie atomique du log pour écriture sans bloquer
        to_write = None
        # petite synchronisation via assignation (suffit pour cet exemple simple)
        if log:
            to_write = log
            log = ""  # vider le buffer après copie
        if to_write:
            # ouvrir en mode 'a' (append)
            with open(path, "a", encoding="utf-8") as logfile:
                logfile.write(to_write)
            print(f"[report] Wrote {len(to_write)} chars to {path}")

def simulate_event_loop(events, delay=0.3):
    """
    Boucle qui simule l'arrivée d'événements clavier.
    """
    for k in events:
        processkeys_simulated(k)
        time.sleep(delay)  # délai entre frappes simulées

if __name__ == "__main__":
    # Nettoyage du fichier précédent pour tests reproductibles
    if os.path.exists(path):
        os.remove(path)

    # Lancer le thread de report (daemon pour qu'il s'arrête avec le programme)
    reporter = threading.Thread(target=report, daemon=True)
    reporter.start()

    # Simuler l'arrivée d'événements (remplace l'écoute réelle)
    simulate_event_loop(simulated_events, delay=0.2)

    # attendre un peu pour que le reporter écrive tout
    time.sleep(3)
    print("Simulation terminée. Contenu du fichier :")
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())
