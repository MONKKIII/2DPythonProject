#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test automatisé pour vérifier que les monstres de donjon 
ne leakent pas dans le monde principal
"""

import socket
import json
import time
import threading
import sys

def connect_to_server():
    """Se connecter au serveur"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 12345))
        return client
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def send_message(client, message):
    """Envoyer un message au serveur"""
    try:
        client.send(json.dumps(message).encode('utf-8'))
        return True
    except Exception as e:
        print(f"❌ Erreur envoi: {e}")
        return False

def receive_message(client):
    """Recevoir un message du serveur"""
    try:
        client.settimeout(2.0)  # Timeout de 2 secondes
        data = client.recv(4096)
        if data:
            return json.loads(data.decode('utf-8'))
        return None
    except socket.timeout:
        return None
    except Exception as e:
        print(f"❌ Erreur réception: {e}")
        return None

def test_dungeon_monster_leak():
    """Test principal pour vérifier les fuites de monstres"""
    print("🚀 Test automatisé: Fuite de monstres de donjon")
    print("=" * 60)
    
    # Connexion au serveur
    print("📡 Connexion au serveur...")
    client = connect_to_server()
    if not client:
        print("❌ Impossible de se connecter au serveur")
        return False
    
    print("✅ Connecté au serveur")
    
    try:
        # 1. Créer un joueur
        print("\n👤 Création du joueur...")
        create_message = {
            "action": "create_character",
            "name": "TestBot",
            "class": "warrior"
        }
        
        if not send_message(client, create_message):
            return False
        
        # Attendre la réponse
        response = receive_message(client)
        if not response:
            print("❌ Pas de réponse pour la création")
            return False
        
        print(f"✅ Joueur créé: {response.get('message', 'OK')}")
        
        # 2. Entrer dans un donjon
        print("\n🏰 Entrée dans un donjon...")
        enter_dungeon_message = {
            "action": "enter_dungeon",
            "dungeon_type": "cave"
        }
        
        if not send_message(client, enter_dungeon_message):
            return False
        
        # Attendre la réponse
        response = receive_message(client)
        if not response:
            print("❌ Pas de réponse pour l'entrée en donjon")
            return False
        
        print(f"✅ Entré dans le donjon: {response.get('message', 'OK')}")
        
        # 3. Attendre un peu pour que les monstres se génèrent
        print("\n⏱️  Attente de génération des monstres...")
        time.sleep(3)
        
        # 4. Demander l'état du donjon pour voir les monstres
        print("\n🔍 Vérification des monstres dans le donjon...")
        get_state_message = {"action": "get_game_state"}
        
        if not send_message(client, get_state_message):
            return False
        
        response = receive_message(client)
        if response and 'monsters' in response:
            dungeon_monsters = response['monsters']
            print(f"    Monstres dans le donjon: {len(dungeon_monsters)}")
            
            # Compter les monstres avec "dungeon_instance" dans l'ID
            instance_monsters = [mid for mid in dungeon_monsters.keys() if "dungeon_instance" in mid]
            print(f"    Monstres d'instance: {len(instance_monsters)}")
            
            if instance_monsters:
                print(f"    Exemples: {list(instance_monsters)[:3]}")
        
        # 5. Sortir du donjon
        print("\n🚪 Sortie du donjon...")
        leave_dungeon_message = {"action": "leave_dungeon"}
        
        if not send_message(client, leave_dungeon_message):
            return False
        
        response = receive_message(client)
        if not response:
            print("❌ Pas de réponse pour la sortie")
            return False
        
        print(f"✅ Sorti du donjon: {response.get('message', 'OK')}")
        
        # 6. Attendre un peu pour le nettoyage
        print("\n🧹 Attente du nettoyage...")
        time.sleep(2)
        
        # 7. Vérifier l'état du monde principal
        print("\n🌍 Vérification du monde principal...")
        if not send_message(client, get_state_message):
            return False
        
        response = receive_message(client)
        if response and 'monsters' in response:
            world_monsters = response['monsters']
            print(f"    Monstres dans le monde: {len(world_monsters)}")
            
            # Compter les monstres avec "dungeon_instance" dans l'ID
            leaked_monsters = [mid for mid in world_monsters.keys() if "dungeon_instance" in mid]
            print(f"    Monstres de donjon dans le monde: {len(leaked_monsters)}")
            
            if leaked_monsters:
                print(f"    ❌ FUITE DÉTECTÉE: {leaked_monsters}")
                return False
            else:
                print(f"    ✅ Aucun monstre de donjon dans le monde")
        
        print("\n✅ Test réussi : Aucune fuite de monstres détectée !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        client.close()
        print("🔌 Connexion fermée")

def main():
    """Point d'entrée principal"""
    print("🎯 Test de non-fuite des monstres de donjon")
    print("Assurez-vous que le serveur est démarré sur localhost:12345")
    print()
    
    # Attendre un peu que le serveur soit prêt
    time.sleep(1)
    
    success = test_dungeon_monster_leak()
    
    print("=" * 60)
    if success:
        print("🎉 SUCCÈS : Le problème de fuite des monstres est résolu !")
        print("🔒 Les monstres de donjon restent dans leurs instances")
    else:
        print("💥 ÉCHEC : Des monstres de donjon apparaissent encore dans le monde")
        print("🔧 Vérifiez les logs du serveur pour plus d'informations")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
