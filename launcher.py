#!/usr/bin/env python3
"""
Script de lancement pour le RPG multijoueur
"""
import os
import sys
import subprocess
import time
import socket

def check_server_running(host='localhost', port=12345):
    """Vérifie si le serveur est en cours d'exécution"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def start_server():
    """Démarre le serveur"""
    python_exe = "C:/Users/Gildwen/Desktop/Coding Project/2DPythonProject/.venv/Scripts/python.exe"
    server_script = "server.py"
    
    print("🚀 Démarrage du serveur RPG...")
    process = subprocess.Popen([python_exe, server_script])
    
    # Attendre que le serveur soit prêt
    for i in range(10):
        if check_server_running():
            print("✅ Serveur démarré avec succès!")
            return process
        time.sleep(0.5)
        print(f"⏳ Attente du serveur... ({i+1}/10)")
    
    print("❌ Erreur: Le serveur n'a pas pu démarrer")
    return None

def start_client(server_ip='localhost'):
    """Démarre un client"""
    python_exe = "C:/Users/Gildwen/Desktop/Coding Project/2DPythonProject/.venv/Scripts/python.exe"
    client_script = "client.py"
    
    print(f"🎮 Démarrage du client (connexion à {server_ip})...")
    
    if server_ip == 'localhost':
        subprocess.run([python_exe, client_script])
    else:
        subprocess.run([python_exe, client_script, server_ip])

def main():
    print("=" * 50)
    print("    🎮 RPG MULTIJOUEUR - LANCEUR 🎮")
    print("=" * 50)
    print()
    
    while True:
        print("Que voulez-vous faire ?")
        print("1. 🖥️  Démarrer le serveur")
        print("2. 🎮 Lancer un client (localhost)")
        print("3. 🌐 Lancer un client (IP personnalisée)")
        print("4. 🔍 Tester le serveur")
        print("5. 📋 Voir les instructions")
        print("6. ❌ Quitter")
        print()
        
        try:
            choice = input("Votre choix (1-6): ").strip()
            print()
            
            if choice == '1':
                if check_server_running():
                    print("⚠️  Un serveur semble déjà être en cours d'exécution")
                    if input("Voulez-vous continuer quand même ? (o/N): ").lower().startswith('o'):
                        start_server()
                else:
                    start_server()
                    input("\n⏸️  Appuyez sur Entrée pour revenir au menu...")
                
            elif choice == '2':
                if not check_server_running():
                    print("❌ Aucun serveur détecté sur localhost:12345")
                    if input("Voulez-vous démarrer le serveur d'abord ? (O/n): ").lower() != 'n':
                        server_process = start_server()
                        if server_process:
                            print("🎮 Lancement du client dans 2 secondes...")
                            time.sleep(2)
                            start_client()
                else:
                    start_client()
                
            elif choice == '3':
                server_ip = input("Entrez l'adresse IP du serveur: ").strip()
                if server_ip:
                    start_client(server_ip)
                else:
                    print("❌ Adresse IP invalide")
                
            elif choice == '4':
                print("🔍 Test de connexion au serveur...")
                subprocess.run([
                    "C:/Users/Gildwen/Desktop/Coding Project/2DPythonProject/.venv/Scripts/python.exe",
                    "test_server.py"
                ])
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
                
            elif choice == '5':
                print_instructions()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
                
            elif choice == '6':
                print("👋 Au revoir!")
                break
                
            else:
                print("❌ Choix invalide!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print("\n" + "-" * 50 + "\n")

def print_instructions():
    print("📋 INSTRUCTIONS DU JEU")
    print("=" * 30)
    print()
    print("🎮 CONTRÔLES:")
    print("  • WASD ou Flèches : Déplacer votre personnage")
    print("  • Espace : Attaquer le monstre le plus proche")
    print("  • Clic gauche : Attaquer un monstre spécifique")
    print("  • Tab : Ouvrir/fermer le panneau des statistiques")
    print()
    print("📈 PROGRESSION:")
    print("  • Tuez des monstres pour gagner de l'XP")
    print("  • Montez de niveau pour obtenir des points de compétence")
    print("  • Améliorez vos statistiques dans le panneau (Tab):")
    print("    - 1 : Attaque (+2)")
    print("    - 2 : Défense (+2)")
    print("    - 3 : Vitesse (+1)")
    print("    - 4 : HP Maximum (+15)")
    print()
    print("⚔️  COMBAT:")
    print("  • Approchez-vous des monstres rouges")
    print("  • Votre attaque diminue leurs HP")
    print("  • Ils ripostent automatiquement")
    print("  • Les monstres réapparaissent après 10 secondes")
    print()
    print("🌐 MULTIJOUEUR:")
    print("  • Un joueur démarre le serveur")
    print("  • Les autres se connectent avec l'IP du serveur")
    print("  • Vous voyez les autres joueurs en violet")
    print("  • Votre personnage est en bleu")

if __name__ == "__main__":
    # Changer vers le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
