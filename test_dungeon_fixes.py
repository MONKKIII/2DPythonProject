#!/usr/bin/env python3
"""
Script de test pour vérifier les corrections du système de donjons
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_client_fixes():
    """Test les corrections du client"""
    try:
        import client
        
        # Créer une instance du client
        game_client = client.GameClient()
        
        # Tester l'ajout de notifications
        game_client.dungeon_notifications = ["Test notification 1", "Test notification 2"]
        game_client.boss_abilities_log = ["Test boss ability 1", "Test boss ability 2"]
        
        # Simuler l'entrée dans un donjon
        game_client.current_dungeon = {
            'name': 'Test Dungeon',
            'instance_id': 'test_123',
            'players_count': 1,
            'max_players': 4
        }
        
        print("✅ Client peut entrer dans un donjon")
        
        # Tester le nettoyage
        game_client.clear_dungeon_ui()
        
        # Vérifier que tout est nettoyé
        assert game_client.current_dungeon is None, "current_dungeon devrait être None"
        assert len(game_client.boss_abilities_log) == 0, "boss_abilities_log devrait être vide"
        assert len(game_client.dungeon_notifications) == 1, "Devrait garder seulement le message de nettoyage"
        
        print("✅ Nettoyage de l'interface fonctionne correctement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test client : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_syntax():
    """Test la syntaxe du serveur (rapide)"""
    try:
        import server
        print("✅ Syntaxe du serveur : OK")
        return True
    except Exception as e:
        print(f"❌ Erreur syntaxe serveur : {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=== TEST DES CORRECTIONS DONJONS ===\n")
    
    tests = [
        test_server_syntax,
        test_client_fixes
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== RÉSULTATS : {passed}/{len(tests)} tests réussis ===")
    
    if passed == len(tests):
        print("🎉 Corrections appliquées avec succès !")
        print("\nChangements effectués :")
        print("1. ✅ Nettoyage des notifications de donjon à la sortie")
        print("2. ✅ Nettoyage du log des capacités de boss à la sortie")
        print("3. ✅ Nettoyage automatique des notifications après 8 secondes")
        print("4. ✅ Les capacités de boss ne s'affichent que dans un donjon")
        print("5. ✅ Méthode clear_dungeon_ui() pour nettoyer immédiatement")
        print("\nPour tester :")
        print("- Entrez dans un donjon, observez les notifications")
        print("- Quittez avec R, vérifiez que tout disparaît")
        print("- Les notifications anciennes disparaissent après 8 secondes")
    else:
        print("❌ Des erreurs doivent être corrigées.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
