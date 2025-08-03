#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement du système de donjons
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_server_syntax():
    """Test la syntaxe du serveur"""
    try:
        import server
        print("✅ Syntaxe du serveur : OK")
        return True
    except Exception as e:
        print(f"❌ Erreur syntaxe serveur : {e}")
        return False

def test_client_syntax():
    """Test la syntaxe du client"""
    try:
        import client
        print("✅ Syntaxe du client : OK")
        return True
    except Exception as e:
        print(f"❌ Erreur syntaxe client : {e}")
        return False

def test_dungeon_system():
    """Test l'initialisation du système de donjons"""
    try:
        from server import GameServer
        server = GameServer()
        
        # Vérifier que les donjons sont initialisés
        assert len(server.dungeons) == 3, f"Attendu 3 donjons, trouvé {len(server.dungeons)}"
        assert 'goblin_cave' in server.dungeons, "Donjon 'goblin_cave' manquant"
        assert 'shadow_temple' in server.dungeons, "Donjon 'shadow_temple' manquant"
        assert 'dragon_lair' in server.dungeons, "Donjon 'dragon_lair' manquant"
        
        # Vérifier les objets légendaires
        legendary_items = [item for item in server.items.values() if item.rarity == "legendary"]
        assert len(legendary_items) >= 5, f"Attendu au moins 5 objets légendaires, trouvé {len(legendary_items)}"
        
        print("✅ Système de donjons : OK")
        print(f"   - {len(server.dungeons)} donjons configurés")
        print(f"   - {len(legendary_items)} objets légendaires")
        return True
        
    except Exception as e:
        print(f"❌ Erreur système de donjons : {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("=== TEST DU SYSTÈME DE DONJONS ===\n")
    
    tests = [
        test_server_syntax,
        test_client_syntax,
        test_dungeon_system
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== RÉSULTATS : {passed}/{len(tests)} tests réussis ===")
    
    if passed == len(tests):
        print("🎉 Tous les tests sont passés ! Le système de donjons est prêt.")
        print("\nPour tester :")
        print("1. Lancez le serveur : python server.py")
        print("2. Lancez le client : python client.py")
        print("3. Créez un personnage niveau 3+ et dirigez-vous vers un portail")
        print("4. Utilisez les touches E (entrer), P (liste), R (sortir)")
    else:
        print("❌ Des erreurs doivent être corrigées avant de tester le jeu.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
