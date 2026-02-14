A. Description

L'objectif est de passer d'un simple script de capture de frappes à une simulation cybersécurité plus réaliste, composée de plusieurs éléments interconnectés. 
Ceci constitue un projet pédagogique démontrant les risques de sécurité liés aux keyloggers.
Ce projet capture les frappes clavier sur une machine victime et les envoie à un serveur distant pour analyse. Il illustre comment un attaquant peut :

- Capturer les données sensibles (mots de passe, textes, etc.)
- Les transmettre vers un serveur malveillant
- Les consulter à distance via une interface web

⚠️ ATTENTION : À utiliser UNIQUEMENT sur vos propres machines pour apprendre !

B. Structure du projet 
```
keylogger_project/
├── README.md                    # Cette documentation
│
├── SERVEUR DISTANT ( IP serveur : X.X.X.X)
│   ├── web.py                   # API Backend (port 5000)
│   ├── dashboard.py             # Interface Web (port 8000)
│   └── controller.py            # Contrôleur Console (optionnel)
│
└── MACHINE VICTIME
    └── v3_keylogger_simple.py   # Keylogger Client
```

C. Installatin & configuration 

- Sur l'hôte de l'attaquant :

# 1. Installer les dépendances
```

pip3 install flask requests
```
# 2. Lancer l'API Backend pour la réception des données 

```
python3 web.py
```
# 3. Lancer le Dashboard 
```
python3 dashboard.py
```

# 4. Lancer le Contrôleur pour l
```
python3 controller.py --server http://192.168.30.129:5000

```
- Sur l'hôte victime

# 1. Copier le fichier v3_keylogger

# 2. Lancer le keylogger

```
python3 v3_keylogger_simple.py
```

D. Fonctionnement du système 

- Sur l'hôte attaquant
  
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
- Sur l'hôte victime 

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

