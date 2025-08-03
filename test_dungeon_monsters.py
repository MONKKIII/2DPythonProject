#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test pour vérifier que les monstres de donjon n'apparaissent pas dans le monde
"""

import threading
import time
import sys
import socket
import json
from unittest.mock import Mock, patch

# Ajouter le chemin du serveur
sys.path.append('.')

def test_dungeon_monster_isolation():
    """Test que les monstres de donjon restent dans leur instance"""
    print("🧪 Test: Isolation des monstres de donjon")
    
    # Importer le serveur
    import server
    
    # Créer un serveur de test
    mock_server = server.GameServer("localhost", 0)
    
    # Créer un joueur fictif
    class MockPlayer:
        def __init__(self, name, x, y, player_class):
            self.id = name
            self.name = name
            self.x = x
            self.y = y
            self.player_class = player_class
            self.socket = Mock()
            self.hp = 100
            self.max_hp = 100
            self.level = 5  # Niveau suffisant pour entrer en donjon
            self.xp = 0
            self.xp_to_next = 100
            self.mana = 100
            self.max_mana = 100
            self.attack = 10
            self.defense = 5
            self.critical_chance = 0.1
            self.speed = 5
            self.skill_points = 0
            self.alive = True
            self.inventory = {}
            self.equipped = {}
            self.gold = 0
            self.dungeon_instance = None
            self.last_ability_use = 0
    
    player = MockPlayer("TestPlayer", 1600, 1200, "Warrior")
    mock_server.players["TestPlayer"] = player
    mock_server.clients[player.socket] = player
    
    print("  🏰 Test: Création d'instance de donjon...")
    
    # Compter les monstres avant création du donjon
    world_monsters_before = len([m for m in mock_server.monsters.values() 
                                if not hasattr(m, 'dungeon_instance') or not m.dungeon_instance])
    total_monsters_before = len(mock_server.monsters)
    
    print(f"    📊 Monstres monde avant: {world_monsters_before}")
    print(f"    📊 Total monstres avant: {total_monsters_before}")
    
    # Faire entrer le joueur dans un donjon
    mock_server.enter_dungeon(player, "goblin_cave")
    
    # Vérifier qu'une instance a été créée
    assert len(mock_server.dungeon_instances) == 1, "Instance de donjon non créée"
    
    # Récupérer l'instance créée
    instance_id = list(mock_server.dungeon_instances.keys())[0]
    instance = mock_server.dungeon_instances[instance_id]
    
    print(f"    ✅ Instance créée: {instance_id}")
    print(f"    📊 Monstres dans l'instance: {len(instance.monsters)}")
    
    # Vérifier que les monstres de donjon ont l'attribut dungeon_instance
    dungeon_monsters_with_instance = 0
    for monster_id, monster in mock_server.monsters.items():
        if hasattr(monster, 'dungeon_instance') and monster.dungeon_instance == instance_id:
            dungeon_monsters_with_instance += 1
    
    print(f"    📊 Monstres avec dungeon_instance: {dungeon_monsters_with_instance}")
    
    # Vérifier que les monstres de donjon ne sont pas comptés comme monstres du monde
    world_monsters_after = len([m for m in mock_server.monsters.values() 
                               if not hasattr(m, 'dungeon_instance') or not m.dungeon_instance])
    
    print(f"    📊 Monstres monde après: {world_monsters_after}")
    
    # Le nombre de monstres du monde ne devrait pas avoir changé
    assert world_monsters_before == world_monsters_after, f"Monstres du monde ont changé: {world_monsters_before} → {world_monsters_after}"
    
    # Il devrait y avoir plus de monstres au total (monstres de donjon ajoutés)
    total_monsters_after = len(mock_server.monsters)
    assert total_monsters_after > total_monsters_before, f"Pas de nouveaux monstres: {total_monsters_before} → {total_monsters_after}"
    
    # Tous les monstres de donjon devraient avoir l'attribut dungeon_instance
    assert dungeon_monsters_with_instance >= 5, f"Pas assez de monstres de donjon marqués: {dungeon_monsters_with_instance}"
    
    print("    ✅ Monstres de donjon correctement isolés")
    
    print("  🚪 Test: Nettoyage lors de sortie de donjon...")
    
    # Faire sortir le joueur du donjon
    mock_server.leave_dungeon(player)
    
    # Vérifier que l'instance a été supprimée
    assert len(mock_server.dungeon_instances) == 0, "Instance de donjon non supprimée"
    
    # Vérifier que les monstres de donjon ont été supprimés
    remaining_monsters = len(mock_server.monsters)
    print(f"    📊 Monstres restants: {remaining_monsters}")
    print(f"    📊 Monstres attendus: {total_monsters_before}")
    
    assert remaining_monsters == total_monsters_before, f"Monstres de donjon non supprimés: {remaining_monsters} vs {total_monsters_before}"
    
    print("    ✅ Nettoyage des monstres de donjon: OK")
    
    return True

def test_boss_minions_isolation():
    """Test que les serviteurs invoqués par les boss restent dans leur instance"""
    print("🧪 Test: Isolation des serviteurs de boss")
    
    import server
    
    # Créer un boss de test avec dungeon_instance
    boss = server.Monster(
        id="test_boss",
        x=100, y=100,
        hp=500, max_hp=500,
        attack=30, defense=10,
        xp_reward=100,
        is_boss=True,
        boss_abilities=["summon_minions"]
    )
    boss.dungeon_instance = "test_dungeon_1"
    
    # Créer un serveur de test
    mock_server = server.GameServer("localhost", 0)
    mock_server.monsters["test_boss"] = boss
    
    # Créer un joueur cible fictif
    class MockPlayer:
        def __init__(self):
            self.id = "test_player"
            self.name = "Test Player"
            self.x = 100
            self.y = 100
            self.hp = 100
            self.max_hp = 100
            self.level = 1
            self.xp = 0
            self.xp_to_next = 100
            self.mana = 50
            self.max_mana = 50
            self.attack = 10
            self.defense = 5
            self.critical_chance = 0.1
            self.speed = 5
            self.skill_points = 0
            self.alive = True
            self.player_class = "Warrior"
            self.inventory = {}
            self.equipped = {}
            self.gold = 0
            self.socket = Mock()
            self.dungeon_instance = "test_dungeon_1"
            self.last_ability_use = 0
    
    target_player = MockPlayer()
    
    # Compter les monstres avant invocation
    monsters_before = len(mock_server.monsters)
    
    # Utiliser la capacité summon_minions
    mock_server.use_boss_ability(boss, target_player)
    
    # Vérifier que des serviteurs ont été créés
    monsters_after = len(mock_server.monsters)
    assert monsters_after > monsters_before, "Aucun serviteur créé"
    
    print(f"    📊 Serviteurs créés: {monsters_after - monsters_before}")
    
    # Vérifier que tous les nouveaux monstres ont la même dungeon_instance que le boss
    for monster_id, monster in mock_server.monsters.items():
        if monster_id != "test_boss":  # Exclure le boss original
            if hasattr(monster, 'dungeon_instance'):
                assert monster.dungeon_instance == "test_dungeon_1", f"Serviteur {monster_id} mal assigné: {monster.dungeon_instance}"
            else:
                # Si pas d'attribut dungeon_instance, c'est un monstre du monde (pas grave pour ce test)
                pass
    
    print("    ✅ Serviteurs correctement assignés à l'instance")
    
    return True

def main():
    """Lance tous les tests"""
    print("🚀 Tests d'isolation des monstres de donjon")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    try:
        if test_dungeon_monster_isolation():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test isolation monstres donjon échoué: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        if test_boss_minions_isolation():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test isolation serviteurs échoué: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)
    print(f"🏁 RÉSULTATS: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("✅ Tous les tests d'isolation des monstres passent!")
        return True
    else:
        print("❌ Certains tests d'isolation ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
