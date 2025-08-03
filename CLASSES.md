# 🎮 Nouvelles Fonctionnalités - Système de Classes

## 🏆 Classes de Personnages

Le jeu dispose maintenant de **4 classes distinctes** avec des capacités spéciales uniques !

### 🛡️ **Guerrier (Warrior)**
- **Spécialité** : Tanking et mêlée
- **Statistiques** : HP élevé (120), Attaque forte (12), Défense haute (8), Lent (4)
- **Capacité spéciale** : **Charge** (Q)
  - Coût : 20 mana
  - Effet : +5 attaque pendant 10 secondes
  - Cooldown : 3 secondes

### 🧙 **Mage**
- **Spécialité** : Sorts à distance et dégâts magiques
- **Statistiques** : HP faible (80), Attaque magique (15), Défense faible (3), Mana élevé (100)
- **Capacité spéciale** : **Boule de Feu** (Q)
  - Coût : 30 mana
  - Effet : 150% des dégâts d'attaque sur une cible
  - Cooldown : 3 secondes

### 🏹 **Archer**
- **Spécialité** : Attaques à distance et critiques
- **Statistiques** : HP modéré (90), Attaque (14), Vitesse élevée (8), Critique 20%
- **Capacité spéciale** : **Tir Multiple** (Q)
  - Coût : 25 mana
  - Effet : Attaque jusqu'à 3 monstres simultanément (70% dégâts)
  - Cooldown : 3 secondes

### 🗡️ **Voleur (Rogue)**
- **Spécialité** : Vitesse et critiques devastateurs
- **Statistiques** : HP faible (85), Vitesse très élevée (10), Critique 25%
- **Capacité spéciale** : **Furtivité** (Q)
  - Coût : 15 mana
  - Effet : +50% chance critique pendant 8 secondes
  - Cooldown : 3 secondes

## ⚔️ Nouveaux Mécanismes de Combat

### 💥 Système de Critiques
- Chaque classe a une chance de critique différente
- Les critiques infligent **200% des dégâts**
- Les critiques sont affichés avec "(CRITIQUE!)" dans les logs

### 🔮 Système de Mana
- Toutes les capacités spéciales consomment de la mana
- La mana se régénère automatiquement : **+2 mana toutes les 2 secondes**
- Barre de mana bleue affichée sous la barre de HP

### ⏱️ Cooldown des Capacités
- Toutes les capacités ont un cooldown de **3 secondes**
- Empêche le spam des capacités spéciales

## 🎯 Nouvelles Commandes

### Lors de la Sélection de Classe
- **1** : Choisir Guerrier
- **2** : Choisir Mage  
- **3** : Choisir Archer
- **4** : Choisir Voleur
- **Entrée** : Confirmer et rejoindre le jeu

### En Jeu
- **Q** : Utiliser la capacité spéciale de votre classe
- **5** : Améliorer Mana Max (+10) [Panneau Stats]
- **6** : Améliorer Chance Critique (+5%) [Panneau Stats]

## 🎨 Améliorations Visuelles

### Couleurs des Classes
- **Guerrier** : Rouge
- **Mage** : Bleu
- **Archer** : Vert
- **Voleur** : Violet
- **Votre personnage** : Jaune (peu importe la classe)

### Nouvelles Barres d'Interface
- **Barre HP** : Verte (comme avant)
- **Barre Mana** : Bleue (nouvelle)
- Affichage de la classe dans le nom du joueur

### Interface Améliorée
- Écran de sélection de classe avec descriptions
- Statistiques détaillées incluant mana et critique
- Affichage de la classe dans les contrôles

## 📊 Équilibrage des Classes

### Points Forts/Faibles

**Guerrier** ✅ Survivabilité, ❌ Vitesse
**Mage** ✅ Dégâts AoE, ❌ Fragilité  
**Archer** ✅ Critiques, ❌ HP moyen
**Voleur** ✅ Vitesse/Critiques, ❌ Très fragile

### Stratégies Recommandées

- **Guerrier** : Restez au front, utilisez Charge avant les gros combats
- **Mage** : Gardez vos distances, visez avec Boule de Feu
- **Archer** : Kite les monstres, utilisez Tir Multiple sur les groupes
- **Voleur** : Hit-and-run, utilisez Furtivité puis attaquez

## 🚀 Comment Tester

1. **Démarrez le serveur** : `python server.py`
2. **Lancez le client** : `python client.py`
3. **Choisissez votre classe** avec les touches 1-4
4. **Testez les capacités** avec la touche Q
5. **Expérimentez** les différents styles de jeu !

## 🔄 Compatibilité

- ✅ Compatible avec l'ancien système (les anciens clients utilisent la classe Guerrier par défaut)
- ✅ Multijoueur stable avec toutes les classes
- ✅ Sauvegarde des statistiques de classe

Le jeu est maintenant beaucoup plus riche en gameplay avec ces nouvelles classes ! Chaque classe offre une expérience de jeu unique. 🎉
