A. Description
Projet pédagogique démontrant les risques de sécurité liés aux keyloggers.
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
├── SERVEUR DISTANT (192.168.30.129)
│   ├── web.py                   # API Backend (port 5000)
│   ├── dashboard.py             # Interface Web (port 8000)
│   └── controller.py            # Contrôleur Console (optionnel)
│
└── MACHINE VICTIME
    └── v3_keylogger_simple.py   # Keylogger Client
```

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
Architecture finale
```

PORT 5000 (web.py)
  ├─ Reçoit POST /api/logs du keylogger
  ├─ Stocke les données
  └─ Sert GET pour dashboard et controller

PORT 8000 (dashboard.py)
  ├─ Interface web joliment formatée
  └─ Consulte le port 5000

Console (controller.py)
  ├─ Menu interactif
  └─ Consulte le port 5000
```
