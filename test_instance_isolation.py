#!/usr/bin/env python3
"""
Script de test pour vérifier l'isolation des instances de donjons
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_instance_separation():
    """Test la séparation des instances"""
    try:
        from server import GameServer, Player, DungeonInstance
        
        # Créer un serveur de test
        server = GameServer()
        
        # Créer des joueurs de test
        player1 = Player(id="player1", name="Alice")
        player2 = Player(id="player2", name="Bob") 
        player3 = Player(id="player3", name="Charlie")
        
        server.players["player1"] = player1
        server.players["player2"] = player2
        server.players["player3"] = player3
        
        # Player1 et Player2 dans le monde principal
        # Player3 dans un donjon
        player3.dungeon_instance = "test_instance"
        server.dungeon_instances["test_instance"] = DungeonInstance(
            instance_id="test_instance",
            dungeon_template_id="goblin_cave"
        )
        server.dungeon_instances["test_instance"].players = ["player3"]
        
        # Tester la création du game state du monde
        world_state = server.create_world_game_state()
        
        # Vérifier que seuls les joueurs du monde sont inclus
        assert "player1" in world_state['players'], "Player1 devrait être dans le monde"
        assert "player2" in world_state['players'], "Player2 devrait être dans le monde"
        assert "player3" not in world_state['players'], "Player3 ne devrait pas être dans le monde"
        
        print("✅ Séparation des joueurs monde/donjon : OK")
        
        # Tester la création du game state du donjon
        dungeon_state = server.create_dungeon_game_state("test_instance")
        
        # Vérifier que seul le joueur du donjon est inclus
        assert "player3" in dungeon_state['players'], "Player3 devrait être dans le donjon"
        assert "player1" not in dungeon_state['players'], "Player1 ne devrait pas être dans le donjon"
        assert "player2" not in dungeon_state['players'], "Player2 ne devrait pas être dans le donjon"
        
        print("✅ Séparation des joueurs donjon : OK")
        
        # Vérifier qu'il n'y a pas de portails dans les donjons
        assert len(dungeon_state['dungeons']) == 0, "Pas de portails dans les donjons"
        
        print("✅ Portails cachés dans les donjons : OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test séparation instances : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_monster_separation():
    """Test la séparation des monstres"""
    try:
        from server import GameServer, Monster, DungeonInstance
        
        server = GameServer()
        
        # Ajouter un monstre du monde
        world_monster = Monster(
            id="world_monster_1",
            x=500, y=500, hp=50, max_hp=50,
            attack=10, defense=5, xp_reward=20
        )
        server.monsters["world_monster_1"] = world_monster
        
        # Créer une instance de donjon avec un monstre
        instance = DungeonInstance(
            instance_id="test_dungeon",
            dungeon_template_id="goblin_cave"
        )
        
        dungeon_monster = Monster(
            id="dungeon_monster_1", 
            x=1600, y=1200, hp=100, max_hp=100,
            attack=15, defense=8, xp_reward=50
        )
        
        instance.monsters["dungeon_monster_1"] = dungeon_monster
        server.monsters["dungeon_monster_1"] = dungeon_monster
        server.dungeon_instances["test_dungeon"] = instance
        
        # Tester le game state du monde
        world_state = server.create_world_game_state()
        assert "world_monster_1" in world_state['monsters'], "Monstre du monde devrait être visible"
        assert "dungeon_monster_1" not in world_state['monsters'], "Monstre de donjon ne devrait pas être visible dans le monde"
        
        print("✅ Monstres du monde séparés : OK")
        
        # Tester le game state du donjon
        dungeon_state = server.create_dungeon_game_state("test_dungeon")
        assert "dungeon_monster_1" in dungeon_state['monsters'], "Monstre de donjon devrait être visible"
        assert "world_monster_1" not in dungeon_state['monsters'], "Monstre du monde ne devrait pas être visible dans le donjon"
        
        print("✅ Monstres de donjon séparés : OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test séparation monstres : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_syntax():
    """Test la syntaxe du serveur"""
    try:
        import server
        print("✅ Syntaxe du serveur : OK")
        return True
    except Exception as e:
        print(f"❌ Erreur syntaxe serveur : {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=== TEST DE L'ISOLATION DES INSTANCES ===\n")
    
    tests = [
        test_server_syntax,
        test_instance_separation,
        test_monster_separation
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== RÉSULTATS : {passed}/{len(tests)} tests réussis ===")
    
    if passed == len(tests):
        print("🎉 Isolation des instances implémentée avec succès !")
        print("\nAméliorations apportées :")
        print("1. ✅ Joueurs séparés par instance (monde vs donjon)")
        print("2. ✅ Monstres séparés par instance") 
        print("3. ✅ Game states spécifiques envoyés à chaque instance")
        print("4. ✅ Portails cachés dans les donjons")
        print("5. ✅ Isolation complète entre monde et donjons")
        print("\nMaintenant :")
        print("- Les joueurs en donjon ne voient que les autres joueurs du même donjon")
        print("- Les monstres du monde n'apparaissent pas dans les donjons")
        print("- Les monstres de donjon n'apparaissent pas dans le monde")
        print("- Chaque instance est complètement isolée")
    else:
        print("❌ Des erreurs doivent être corrigées.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
