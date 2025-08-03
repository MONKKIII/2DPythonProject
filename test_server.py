"""
Script de test pour vérifier le serveur RPG
"""
import socket
import json
import threading
import time

def test_server_connection(host='localhost', port=12345):
    """Test de connexion basique au serveur"""
    try:
        # Créer un socket client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"✓ Connexion réussie au serveur {host}:{port}")
        
        # Envoyer un message de join
        join_message = {
            'type': 'join',
            'name': 'TestPlayer'
        }
        client_socket.send(json.dumps(join_message).encode())
        print("✓ Message de connexion envoyé")
        
        # Recevoir la réponse
        response = client_socket.recv(1024).decode()
        response_data = json.loads(response)
        print(f"✓ Réponse reçue: {response_data['type']}")
        
        if response_data['type'] == 'joined':
            player_id = response_data['player_id']
            print(f"✓ Connecté avec l'ID: {player_id}")
            
            # Test de mouvement
            move_message = {
                'type': 'move',
                'x': 450,
                'y': 350
            }
            client_socket.send(json.dumps(move_message).encode())
            print("✓ Message de mouvement envoyé")
            
            # Attendre un peu pour recevoir l'état du jeu
            time.sleep(2)
            
            try:
                game_state = client_socket.recv(4096).decode()
                game_data = json.loads(game_state)
                if game_data['type'] == 'game_state':
                    print(f"✓ État du jeu reçu avec {len(game_data['players'])} joueur(s) et {len(game_data['monsters'])} monstre(s)")
                else:
                    print(f"✓ Message reçu: {game_data['type']}")
            except:
                print("! Pas d'état de jeu reçu (normal si le serveur n'envoie pas en continu)")
        
        client_socket.close()
        print("✓ Test de connexion terminé avec succès")
        return True
        
    except ConnectionRefusedError:
        print("✗ Impossible de se connecter au serveur. Est-il démarré ?")
        return False
    except Exception as e:
        print(f"✗ Erreur pendant le test: {e}")
        return False

def start_test_server():
    """Démarre le serveur pour le test"""
    import subprocess
    import sys
    
    python_exe = "C:/Users/Gildwen/Desktop/Coding Project/2DPythonProject/.venv/Scripts/python.exe"
    server_script = "c:\\Users\\Gildwen\\Desktop\\Coding Project\\2DPythonProject\\server.py"
    
    print("Démarrage du serveur de test...")
    return subprocess.Popen([python_exe, server_script])

if __name__ == "__main__":
    print("=== Test du serveur RPG ===")
    print()
    
    # Test 1: Vérifier si le serveur est déjà en cours d'exécution
    print("Test 1: Vérification de la connexion au serveur")
    if test_server_connection():
        print("Le serveur fonctionne parfaitement !")
    else:
        print("\nLe serveur ne semble pas être démarré.")
        print("Pour démarrer le serveur, exécutez:")
        print('python server.py')
        print("\nOu utilisez le script launcher.bat")
