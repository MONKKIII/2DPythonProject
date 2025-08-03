#!/usr/bin/env python3
"""
Test script pour vérifier la syntaxe du système de donjons
"""

import sys
import ast

def check_syntax(filename):
    """Vérifie la syntaxe d'un fichier Python"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse le code pour vérifier la syntaxe
        ast.parse(source)
        print(f"✅ {filename}: Syntaxe correcte!")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filename}: Erreur de syntaxe à la ligne {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filename}: Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Vérification de la syntaxe des fichiers...")
    
    files_to_check = ["server.py", "client.py"]
    all_good = True
    
    for filename in files_to_check:
        if not check_syntax(filename):
            all_good = False
    
    if all_good:
        print("\n🎉 Tous les fichiers ont une syntaxe correcte!")
        print("\n📋 Nouvelles fonctionnalités ajoutées:")
        print("  🏰 Système de donjons avec 3 niveaux")
        print("  👹 Boss avec capacités spéciales")
        print("  🏆 Objets légendaires exclusifs")
        print("  💰 Récompenses bonus pour complétion")
        print("  🔄 Instances isolées pour groupes")
    else:
        print("\n⚠️ Des erreurs de syntaxe ont été détectées!")
        sys.exit(1)
