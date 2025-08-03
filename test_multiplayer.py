#!/usr/bin/env python3
"""
Test multijoueur pour vérifier que plusieurs clients peuvent se connecter
"""
import socket
import json
import threading
import time
import random

class TestClient:
    def __init__(self, name, host='localhost', port=12345):
        self.name = name
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.player_id = None
        self.running = True
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"[{self.name}] Connecté au serveur")
            
            # Start listening thread
            threading.Thread(target=self.listen, daemon=True).start()
            
            # Join game
            self.send_message({
                'type': 'join',
                'name': self.name
            })
            
            return True
        except Exception as e:
            print(f"[{self.name}] Erreur connexion: {e}")
            return False
    
    def listen(self):
        buffer = ""
        while self.connected and self.running:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                
                while '\n' in buffer:
                    message_str, buffer = buffer.split('\n', 1)
                    if message_str.strip():
                        try:
                            message = json.loads(message_str.strip())
                            self.process_message(message)
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"[{self.name}] Erreur traitement: {e}")
                            continue
                            
            except Exception as e:
                print(f"[{self.name}] Erreur écoute: {e}")
                break
        
        self.connected = False
    
    def process_message(self, message):
        msg_type = message.get('type')
        
        if msg_type == 'joined':
            self.player_id = message['player_id']
            print(f"[{self.name}] Rejoint avec ID: {self.player_id}")
            
        elif msg_type == 'game_state':
            players_count = len(message['players'])
            monsters_count = len(message['monsters'])
            if random.random() < 0.01:  # Print occasionally
                print(f"[{self.name}] État: {players_count} joueurs, {monsters_count} monstres")
                
        elif msg_type == 'combat_result':
            print(f"[{self.name}] Combat: {message.get('log', 'Combat')}")
    
    def send_message(self, message):
        if self.connected:
            try:
                message_str = json.dumps(message) + '\n'
                self.socket.send(message_str.encode('utf-8'))
            except Exception as e:
                print(f"[{self.name}] Erreur envoi: {e}")
                self.connected = False
    
    def simulate_gameplay(self, duration=30):
        """Simulate random gameplay for testing"""
        start_time = time.time()
        
        while self.connected and self.running and (time.time() - start_time) < duration:
            try:
                # Random movement
                if random.random() < 0.3:
                    x = random.randint(50, 750)
                    y = random.randint(50, 550)
                    self.send_message({
                        'type': 'move',
                        'x': x,
                        'y': y
                    })
                
                # Random monster attack
                if random.random() < 0.1:
                    monster_id = f"monster_{random.randint(0, 4)}"
                    self.send_message({
                        'type': 'attack_monster',
                        'monster_id': monster_id
                    })
                
                # Random stat upgrade
                if random.random() < 0.05:
                    stat = random.choice(['attack', 'defense', 'speed', 'hp'])
                    self.send_message({
                        'type': 'upgrade_stat',
                        'stat': stat
                    })
                
                time.sleep(0.1)  # 10 FPS for testing
                
            except Exception as e:
                print(f"[{self.name}] Erreur simulation: {e}")
                break
        
        print(f"[{self.name}] Fin de simulation")
    
    def disconnect(self):
        self.running = False
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

def test_multiple_clients(num_clients=3, duration=30):
    """Test avec plusieurs clients simultanés"""
    print(f"🧪 Test multijoueur avec {num_clients} clients pendant {duration} secondes")
    
    clients = []
    
    # Créer et connecter les clients
    for i in range(num_clients):
        client = TestClient(f"TestPlayer{i+1}")
        if client.connect():
            clients.append(client)
            time.sleep(0.5)  # Petit délai entre les connexions
        else:
            print(f"❌ Impossible de connecter le client {i+1}")
            return False
    
    print(f"✅ {len(clients)} clients connectés")
    
    # Lancer les simulations
    threads = []
    for client in clients:
        thread = threading.Thread(target=client.simulate_gameplay, args=(duration,))
        thread.start()
        threads.append(thread)
    
    # Attendre la fin
    for thread in threads:
        thread.join()
    
    # Déconnecter les clients
    for client in clients:
        client.disconnect()
    
    print("🎉 Test terminé avec succès!")
    return True

def main():
    print("=== Test Multijoueur RPG ===")
    print()
    
    # Test basique de connexion
    print("1. Test de connexion simple...")
    simple_client = TestClient("SimpleTest")
    if simple_client.connect():
        print("✅ Connexion simple réussie")
        time.sleep(2)
        simple_client.disconnect()
    else:
        print("❌ Échec de la connexion simple")
        return
    
    print()
    
    # Test multijoueur
    print("2. Test multijoueur...")
    if test_multiple_clients(num_clients=3, duration=10):
        print("✅ Test multijoueur réussi")
    else:
        print("❌ Échec du test multijoueur")

if __name__ == "__main__":
    main()
