Projet à vocation scolaire : il s'agit de réaliser une infrastructure vulnérable et accéssible au travers de notre réseau informatique.

La structure de l'infra mise en place doit ressembler à celle suivante : 

```
CLIENT (Keylogger)
    ↓
    Envoie les touches à PORT 5000
    ↓
SERVEUR 5000 (API Flask)
    ├─ Reçoit les données
    ├─ Les stocke
    └─ Expose /api/victims, /api/logs
    
DASHBOARD 8000 (Interface Web)
    ├─ Consulte le serveur 5000
    ├─ Affiche les données
    └─ Interface pour voir les logs

```
```
1. CAPTURE (on_press)
   └─→ Chaque touche → log_queue

2. ENVOI (sender)
   └─→ Attend 10 touches (BATCH_SIZE)
   └─→ Les envoie au serveur
   └─→ Boucle infinie

3. MAIN
   └─→ Démarre le thread d'envoi
   └─→ Écoute le clavier en continu
```
