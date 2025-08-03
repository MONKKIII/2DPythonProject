# 🎮 RPG Multijoueur 2D en Python

Un jeu de rôle multijoueur en temps réel développé avec Python et Pygame, offrant une expérience RPG complète avec combat, exploration et progression de personnage.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Lancement du jeu](#-lancement-du-jeu)
- [Contrôles](#-contrôles)
- [Classes de personnages](#-classes-de-personnages)
- [Système de jeu](#-système-de-jeu)
- [Architecture technique](#-architecture-technique)
- [Développement](#-développement)

## ✨ Fonctionnalités

### 🎯 **Gameplay principal**
- **Multijoueur en temps réel** via TCP avec synchronisation stable
- **4 classes de personnages** uniques avec capacités spéciales
- **Grand monde ouvert** de 3200x2400 pixels divisé en 9 biomes
- **74 monstres** répartis par zones avec respawn intelligent
- **Système de combat** avec attaques normales, critiques et capacités

### 🎒 **Système d'objets avancé**
- **Inventaire universel** avec système de stacks intelligents
- **Limites par rareté** : Common (50), Uncommon (20), Rare (10), Epic (5), Legendary (2)
- **4 types d'objets** : Armes, Armures, Consommables, Accessoires
- **Équipement automatique** avec recalcul des statistiques
- **5 niveaux de rareté** avec drops pondérés

### 🗺️ **Exploration et monde**
- **9 biomes distincts** : Plaines, Forêt, Montagnes, Désert, Côte, Volcan, Glace, Marais, Cristal
- **Mini-carte interactive** avec affichage des zones
- **Système de caméra** fluide qui suit le joueur
- **Monstres spécialisés** par biome avec stats adaptées

### 🎨 **Interface utilisateur optimisée**
- **Interface épurée** avec logs de combat masquables (touche L)
- **Panneau d'inventaire intégré** (400x500) avec toutes les stats
- **Barres HP/Mana visuelles** en bas d'écran avec indicateurs
- **Contrôles masquables** (touche H) pour un écran propre
- **Affichage des limites de stack** (quantité/max)

## 🔧 Prérequis

- **Python 3.8+**
- **Pygame 2.0+**

## 📦 Installation

1. **Cloner le repository**
```bash
git clone https://github.com/MONKKIII/2DPythonProject.git
cd 2DPythonProject
```

2. **Installer les dépendances**
```bash
pip install pygame
```

## 🚀 Lancement du jeu

### Démarrer le serveur
```bash
python server.py
```
Le serveur se lance sur `localhost:12345`

### Lancer le client
```bash
python client.py
```

**Note :** Vous pouvez lancer plusieurs clients pour jouer en multijoueur !

## 🎮 Contrôles

| Touche | Action |
|--------|--------|
| **WASD** / **Flèches** | Déplacement |
| **Espace** | Attaquer le monstre le plus proche |
| **Q** | Utiliser la capacité spéciale |
| **Clic gauche** | Attaquer monstre / Ramasser objet |
| **Tab** | Ouvrir/fermer le panneau de stats |
| **I** | Ouvrir/fermer l'inventaire |
| **M** | Afficher/masquer la mini-carte |
| **H** | Afficher/masquer l'aide |
| **L** | Afficher/masquer les logs de combat |

## ⚔️ Classes de personnages

### 🛡️ **Warrior (Guerrier)**
- **HP** : 120 | **Mana** : 30 | **Critique** : 5%
- **Capacité** : ⚡ **Charge** (20 mana) - +5 ATK pendant 10s
- **Style** : Tank avec haute défense et attaque soutenue

### 🧙 **Mage**
- **HP** : 80 | **Mana** : 100 | **Critique** : 15%
- **Capacité** : 🔥 **Boule de Feu** (30 mana) - 150% dégâts à distance
- **Style** : Burst damage élevé avec grande réserve de mana

### 🏹 **Archer**
- **HP** : 90 | **Mana** : 50 | **Critique** : 20%
- **Capacité** : 🏹 **Tir Multiple** (25 mana) - Touche 3 cibles max
- **Style** : Attaques multiples avec haute chance critique

### 🗡️ **Rogue**
- **HP** : 85 | **Mana** : 40 | **Critique** : 25%
- **Capacité** : 👤 **Furtivité** (15 mana) - +50% critique pendant 8s
- **Style** : Vitesse et critiques dévastateurs

## 🌍 Système de jeu

### **Progression**
- **Système XP** avec level-up automatique
- **Points de compétence** à distribuer (3 par niveau)
- **6 statistiques** : Attaque, Défense, Vitesse, HP, Mana, Critique
- **Respawn** automatique après K.O. (5 secondes)

### **Combat**
- **Dégâts calculés** : (Attaque - Défense) × Multiplicateur critique
- **Logs compacts** avec emojis : ⚔️ 🛡️ ⚡ 🔥 🏹 👤
- **Cooldown des capacités** : 3 secondes
- **Régénération de mana** : +2 toutes les 2 secondes

### **Objets et économie**
- **Drop rate** : 30% par monstre tué
- **Rareté pondérée** : Common 60%, Uncommon 25%, Rare 12%, Epic 2%, Legendary 1%
- **Auto-stack intelligent** avec vérification des limites
- **Système d'or** intégré (prêt pour économie future)

### **Monde et exploration**
- **9 zones thématiques** avec monstres spécialisés
- **Noms raccourcis** dans les logs (ex: "Slime" au lieu de "Slime_plains_1")
- **Respawn par zone** respectant les types de monstres
- **Coordonnées monde** : 3200×2400 avec limits de mouvement

## 🔧 Architecture technique

### **Serveur (`server.py`)**
- **Modèle client-serveur** avec threading
- **Communication TCP** via JSON + délimiteurs
- **Game loop 30 FPS** avec états synchronisés
- **Threading sécurisé** avec locks pour données partagées
- **Gestion d'erreurs robuste** avec timeouts et reconnexions

### **Client (`client.py`)**
- **Pygame 2.6.1** pour rendu et input
- **Système de caméra** avec conversion coordonnées monde/écran
- **Interface modulaire** avec panneaux masquables
- **Gestion d'état** locale avec synchronisation serveur
- **Optimisations d'affichage** (culling, cache)

### **Structure des données**
```python
# Classes principales avec dataclasses
@dataclass
class Player:
    # Stats, inventaire, équipement, position...

@dataclass 
class Monster:
    # HP, attaque, défense, récompenses XP...

@dataclass
class Item:
    # Type, rareté, stats, effets, stackable...

@dataclass
class ItemStack:
    # Gestion des quantités et limites
```

## 🚧 Développement

### **Fonctionnalités complétées**
- ✅ Multijoueur stable avec 4 classes
- ✅ Combat et capacités spéciales  
- ✅ Grand monde avec 9 biomes et 74 monstres
- ✅ Système d'objets universel avec stacking
- ✅ Interface optimisée avec stats intégrées
- ✅ Logs de combat compacts et masquables

### **Roadmap future**
- 🎯 **Combat PvP** entre joueurs
- 🏰 **Système de donjons** avec boss
- 🎨 **Sprites et animations** (remplacer les cercles)
- 🏪 **NPCs marchands** et économie
- 👥 **Guildes et chat global**
- 🗺️ **Quêtes et objectifs**

### **Contribuer**
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📊 Statistiques du projet

- **Lignes de code** : ~1200 (serveur) + ~1200 (client)
- **Classes définies** : 8 dataclasses principales
- **Monstres** : 74 répartis sur 9 zones
- **Objets** : 12 types avec 5 raretés
- **Résolution** : 1024×768 avec monde 3200×2400
- **Performance** : 30 FPS stable en multijoueur

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **MONKKIII** - Développement initial et architecture
- **Communauté** - Contributions et suggestions

---

**🎮 Bon jeu et bonne exploration !**

*Dernière mise à jour : Août 2025*