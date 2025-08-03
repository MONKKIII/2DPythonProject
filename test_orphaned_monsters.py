#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test pour vérifier que les monstres orphelins de donjon sont supprimés
"""

import threading
import time
import sys
import socket
import json
from unittest.mock import Mock, patch

# Ajouter le chemin du serveur
sys.path.append('.')

def test_orphaned_monster_cleanup():
    """Test que les monstres orphelins sont détectés et supprimés"""
    print("🧪 Test: Nettoyage des monstres orphelins")
    
    # Importer le serveur
    import server
    
    # Créer un serveur de test
    mock_server = server.GameServer("localhost", 0)
    
    print("  📊 État initial:")
    initial_count = len(mock_server.monsters)
    print(f"    Monstres initiaux: {initial_count}")
    
    # Créer manuellement des monstres orphelins (simule des monstres qui sont restés après suppression d'instance)
    orphaned_monsters = [
        "dungeon_instance_999_mob_0",
        "dungeon_instance_999_mob_1", 
        "dungeon_instance_999_boss",
        "dungeon_instance_888_mob_0"
    ]
    
    print("  🏭 Ajout de monstres orphelins...")
    for monster_id in orphaned_monsters:
        orphaned_monster = server.Monster(
            id=monster_id,
            x=100, y=100,
            hp=50, max_hp=50,
            attack=10, defense=5,
            xp_reward=20
        )
        # Marquer comme appartenant à une instance qui n'existe pas
        orphaned_monster.dungeon_instance = "dungeon_instance_999" if "999" in monster_id else "dungeon_instance_888"
        mock_server.monsters[monster_id] = orphaned_monster
    
    print(f"    Monstres après ajout: {len(mock_server.monsters)}")
    print(f"    Monstres orphelins ajoutés: {len(orphaned_monsters)}")
    
    # Vérifier qu'aucune instance n'existe pour ces monstres
    print("  🔍 Vérification des instances:")
    for instance_id in ["dungeon_instance_999", "dungeon_instance_888"]:
        exists = instance_id in mock_server.dungeon_instances
        print(f"    Instance {instance_id} existe: {exists}")
        assert not exists, f"L'instance {instance_id} ne devrait pas exister"
    
    # Lancer le nettoyage
    print("  🧹 Lancement du nettoyage...")
    mock_server.cleanup_orphaned_dungeon_monsters()
    
    # Vérifier que les monstres orphelins ont été supprimés
    final_count = len(mock_server.monsters)
    print(f"    Monstres après nettoyage: {final_count}")
    
    # Le nombre final devrait être égal au nombre initial
    assert final_count == initial_count, f"Nombre incorrect après nettoyage: {final_count} vs {initial_count}"
    
    # Vérifier qu'aucun monstre orphelin ne reste
    remaining_orphans = [mid for mid in mock_server.monsters.keys() if mid.startswith("dungeon_instance_")]
    print(f"    Monstres orphelins restants: {len(remaining_orphans)}")
    
    if remaining_orphans:
        print(f"    ⚠️  Orphelins restants: {remaining_orphans}")
        # Vérifier si ce sont des monstres légitimes (appartenant à des instances existantes)
        legitimate_orphans = []
        for monster_id in remaining_orphans:
            parts = monster_id.split("_")
            if len(parts) >= 3:
                potential_instance_id = "_".join(parts[:3])
                if potential_instance_id in mock_server.dungeon_instances:
                    legitimate_orphans.append(monster_id)
        
        illegitimate_orphans = [m for m in remaining_orphans if m not in legitimate_orphans]
        assert len(illegitimate_orphans) == 0, f"Monstres orphelins illégitimes restants: {illegitimate_orphans}"
    
    print("    ✅ Nettoyage des orphelins: OK")
    return True

def test_world_filtering():
    """Test que le filtrage du monde exclut les monstres de donjon"""
    print("🧪 Test: Filtrage des monstres dans le monde")
    
    import server
    
    # Créer un serveur de test
    mock_server = server.GameServer("localhost", 0)
    
    # Ajouter quelques monstres de donjon simulés
    dungeon_monsters = [
        "dungeon_instance_123_mob_0",
        "dungeon_instance_123_boss"
    ]
    
    print("  🏭 Ajout de monstres de donjon simulés...")
    for monster_id in dungeon_monsters:
        dungeon_monster = server.Monster(
            id=monster_id,
            x=200, y=200,
            hp=75, max_hp=75,
            attack=15, defense=8,
            xp_reward=30
        )
        dungeon_monster.dungeon_instance = "dungeon_instance_123"
        mock_server.monsters[monster_id] = dungeon_monster
    
    print(f"    Total monstres: {len(mock_server.monsters)}")
    
    # Créer l'état du monde
    print("  🌍 Création de l'état du monde...")
    world_state = mock_server.create_world_game_state()
    world_monsters = world_state['monsters']
    
    print(f"    Monstres dans l'état du monde: {len(world_monsters)}")
    
    # Vérifier qu'aucun monstre de donjon n'apparaît dans l'état du monde
    dungeon_monsters_in_world = [mid for mid in world_monsters.keys() if mid.startswith("dungeon_instance_")]
    
    print(f"    Monstres de donjon dans le monde: {len(dungeon_monsters_in_world)}")
    
    if dungeon_monsters_in_world:
        print(f"    ❌ Monstres de donjon trouvés: {dungeon_monsters_in_world}")
    
    assert len(dungeon_monsters_in_world) == 0, f"Des monstres de donjon apparaissent dans le monde: {dungeon_monsters_in_world}"
    
    print("    ✅ Filtrage du monde: OK")
    return True

def main():
    """Lance tous les tests"""
    print("🚀 Tests de nettoyage des monstres orphelins")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    try:
        if test_orphaned_monster_cleanup():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test nettoyage orphelins échoué: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        if test_world_filtering():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test filtrage monde échoué: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print(f"🏁 RÉSULTATS: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("✅ Tous les tests de nettoyage passent!")
        print("🎯 Les monstres orphelins seront supprimés automatiquement")
        return True
    else:
        print("❌ Certains tests de nettoyage ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
