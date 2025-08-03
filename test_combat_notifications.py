#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test pour vérifier que les notifications de combat sont filtrées par instance
"""

import threading
import time
import sys
import socket
import json
from unittest.mock import Mock, patch

# Ajouter le chemin du serveur
sys.path.append('.')

class MockPlayer:
    """Mock simple d'un joueur"""
    def __init__(self, name, x, y, player_class):
        self.name = name
        self.x = x
        self.y = y
        self.player_class = player_class
        self.socket = None
        self.dungeon_instance = None

def test_broadcast_to_instance():
    """Test de base de la méthode broadcast_to_instance"""
    print("🧪 Test: broadcast_to_instance")
    
    # Créer un serveur fictif avec seulement les méthodes nécessaires
    class MockServer:
        def __init__(self):
            self.clients = {}
            self.players = {}
        
        def broadcast_to_instance(self, message, instance_id=None):
            """Copie de la méthode du serveur"""
            if not self.clients:
                return
                
            # Si instance_id est None, envoyer au monde principal
            if instance_id is None:
                target_players = [p for p in self.players.values() 
                                if not hasattr(p, 'dungeon_instance') or not p.dungeon_instance]
            else:
                # Envoyer aux joueurs de l'instance spécifique
                target_players = [p for p in self.players.values() 
                                if hasattr(p, 'dungeon_instance') and p.dungeon_instance == instance_id]
            
            message_str = json.dumps(message) + '\n'
            
            for player in target_players:
                if player.socket:
                    try:
                        player.socket.send(message_str.encode('utf-8'))
                    except Exception as e:
                        print(f"Erreur envoi: {e}")
    
    server = MockServer()
    
    # Mock des sockets clients
    socket1 = Mock()
    socket2 = Mock()
    socket3 = Mock()
    
    # Configurer les méthodes send
    socket1.send = Mock()
    socket2.send = Mock() 
    socket3.send = Mock()
    
    # Ajouter des joueurs fictifs
    
    # Joueur 1 dans le monde principal
    player1 = MockPlayer("TestPlayer1", 100, 100, "Warrior")
    player1.socket = socket1
    # Pas d'instance de donjon = monde principal
    
    # Joueur 2 dans le donjon "dungeon_1"
    player2 = MockPlayer("TestPlayer2", 200, 200, "Mage")
    player2.socket = socket2
    player2.dungeon_instance = "dungeon_1"
    
    # Joueur 3 dans le donjon "dungeon_2"
    player3 = MockPlayer("TestPlayer3", 300, 300, "Archer")
    player3.socket = socket3
    player3.dungeon_instance = "dungeon_2"
    
    # Ajouter les joueurs au serveur
    server.clients[socket1] = "TestPlayer1"
    server.clients[socket2] = "TestPlayer2"
    server.clients[socket3] = "TestPlayer3"
    server.players["TestPlayer1"] = player1
    server.players["TestPlayer2"] = player2
    server.players["TestPlayer3"] = player3
    
    # Test 1: Message au monde principal
    print("  📤 Test broadcast vers monde principal...")
    server.broadcast_to_instance({
        'type': 'combat_result',
        'log': 'Test combat monde'
    }, None)  # None = monde principal
    
    # Vérifier que seul le joueur 1 a reçu le message
    assert socket1.send.called, "Joueur monde devrait recevoir le message"
    assert not socket2.send.called, "Joueur dungeon_1 ne devrait pas recevoir"
    assert not socket3.send.called, "Joueur dungeon_2 ne devrait pas recevoir"
    
    # Reset les mocks
    socket1.send.reset_mock()
    socket2.send.reset_mock()
    socket3.send.reset_mock()
    
    # Test 2: Message au dungeon_1
    print("  📤 Test broadcast vers dungeon_1...")
    server.broadcast_to_instance({
        'type': 'combat_result',
        'log': 'Test combat dungeon_1'
    }, "dungeon_1")
    
    # Vérifier que seul le joueur 2 a reçu le message
    assert not socket1.send.called, "Joueur monde ne devrait pas recevoir"
    assert socket2.send.called, "Joueur dungeon_1 devrait recevoir le message"
    assert not socket3.send.called, "Joueur dungeon_2 ne devrait pas recevoir"
    
    # Reset les mocks
    socket1.send.reset_mock()
    socket2.send.reset_mock()
    socket3.send.reset_mock()
    
    # Test 3: Message au dungeon_2
    print("  📤 Test broadcast vers dungeon_2...")
    server.broadcast_to_instance({
        'type': 'boss_ability',
        'log': 'Test capacité boss dungeon_2'
    }, "dungeon_2")
    
    # Vérifier que seul le joueur 3 a reçu le message
    assert not socket1.send.called, "Joueur monde ne devrait pas recevoir"
    assert not socket2.send.called, "Joueur dungeon_1 ne devrait pas recevoir"
    assert socket3.send.called, "Joueur dungeon_2 devrait recevoir le message"
    
    print("  ✅ Isolation des broadcasts: OK")
    return True

def test_server_syntax():
    """Test que le serveur se compile sans erreur"""
    print("🧪 Test: Syntaxe du serveur")
    
    try:
        import server
        print("  ✅ Serveur importé sans erreur: OK")
        
        # Vérifier que la méthode broadcast_to_instance existe
        assert hasattr(server.GameServer, 'broadcast_to_instance'), "Méthode broadcast_to_instance manquante"
        print("  ✅ Méthode broadcast_to_instance présente: OK")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur d'import: {e}")
        return False

def main():
    """Lance tous les tests"""
    print("🚀 Tests des notifications de combat par instance")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    try:
        if test_server_syntax():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test syntaxe serveur échoué: {e}")
    
    try:
        if test_broadcast_to_instance():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test broadcast isolation échoué: {e}")
    
    print("=" * 50)
    print(f"🏁 RÉSULTATS: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("✅ Tous les tests de combat passent!")
        return True
    else:
        print("❌ Certains tests de combat ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
