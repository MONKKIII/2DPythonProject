# 🎮 RPG Multijoueur 2D en Python

Un jeu de rôle multijoueur en temps réel développé avec Python et Pygame, offrant une expérience RPG complète avec combat, exploration et progression de personnage.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Lancement du jeu](#-lancement-du-jeu)
- [Contrôles](#-contrôles)
- [Donjons et Boss](#-donjons-et-boss)
- [Inventaire et Objets](#-inventaire-et-objets)
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
- **Système de donjons complet** avec 3 donjons, boss et mécaniques spéciales

### � **Système de donjons avancé**
- **3 donjons uniques** : Caverne des Gobelins, Temple des Ombres, Antre du Dragon
- **Instances privées** pour chaque groupe (max 4 joueurs par donjon)
- **Boss épiques** avec capacités spéciales et mécaniques uniques
- **Progression par niveau** : niveaux 3, 7 et 12 requis
- **Isolation complète** : monstres de donjon ne peuvent pas s'échapper
- **Notifications de donjon** avec système de logs spécialisé
- **Portails visuels** sur la carte du monde

### 🎒 **Système d'inventaire optimisé**
- **Interface compacte** 400x400px sans chevauchement avec l'UI
- **Défilement intelligent** : 6 objets visibles max avec navigation fluide
- **Système de stacks universel** avec limites par rareté
- **Limites par rareté** : Common (50), Uncommon (20), Rare (10), Epic (5), Legendary (2)
- **4 types d'objets** : Armes, Armures, Consommables, Accessoires
- **Équipement automatique** avec recalcul des statistiques
- **5 niveaux de rareté** avec drops pondérés et couleurs distinctives
- **Navigation par flèches/molette** pour inventaires volumineux

### 🗺️ **Exploration et monde**
- **9 biomes distincts** : Plaines, Forêt, Montagnes, Désert, Côte, Volcan, Glace, Marais, Cristal
- **Mini-carte interactive** avec affichage des zones et portails de donjons
- **Système de caméra** fluide qui suit le joueur
- **Monstres spécialisés** par biome avec stats adaptées
- **Portails de donjons** visibles sur la carte avec indicateurs de niveau

### 🎨 **Interface utilisateur optimisée**
- **Interface épurée** avec logs de combat masquables (touche L)
- **Panneau d'inventaire intégré** avec stats complètes du joueur
- **Barres HP/Mana visuelles** en bas d'écran avec indicateurs colorés
- **Système de notifications** pour donjons et événements spéciaux
- **Contrôles masquables** (touche H) pour un écran propre
- **Indicateurs de défilement** pour inventaires volumineux

## 🔧 Prérequis

- **Python 3.8+** (testé avec Python 3.13.2)
- **Pygame 2.0+** (testé avec Pygame 2.6.1)
- **Environnement virtuel recommandé** pour l'isolation des dépendances

## 📦 Installation

1. **Cloner le repository**
```bash
git clone https://github.com/MONKKIII/2DPythonProject.git
cd 2DPythonProject
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv .venv
# Sur Windows
.venv\Scripts\activate
# Sur Linux/Mac
source .venv/bin/activate
```

3. **Installer les dépendances**
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
| **Clic gauche** | Attaquer monstre / Ramasser objet / Inventaire |
| **Tab** | Ouvrir/fermer le panneau de stats |
| **I** | Ouvrir/fermer l'inventaire (réinitialise le défilement) |
| **Flèches HAUT/BAS** | Défiler dans l'inventaire |
| **Molette souris** | Défiler rapidement dans l'inventaire |
| **M** | Afficher/masquer la mini-carte |
| **H** | Afficher/masquer l'aide |
| **L** | Afficher/masquer les logs de combat |
| **P** | Afficher la liste des donjons |
| **E** | Entrer dans un donjon (près d'un portail) |
| **R** | Quitter le donjon actuel |

## 🏰 Donjons et Boss

### **Caverne des Gobelins** (Niveau 3+)
- **Position** : Centre-gauche de la carte (1600, 1200)
- **Boss** : Roi Gobelin - Invoquer des sbires gobelins
- **Difficulté** : Débutant - Parfait pour apprendre les mécaniques
- **Récompenses** : Équipement de base et or

### **Temple des Ombres** (Niveau 7+)
- **Position** : Nord-centre de la carte (800, 400)  
- **Boss** : Maître des Ombres - Attaques d'ombre à distance
- **Difficulté** : Intermédiaire - Nécessite coordination et esquive
- **Récompenses** : Équipement magique et objets rares

### **Antre du Dragon** (Niveau 12+)
- **Position** : Sud-est de la carte (2400, 1600)
- **Boss** : Dragon Ancien - Souffle de feu et spawn massif de lézards
- **Difficulté** : Expert - Combat de groupe recommandé
- **Récompenses** : Équipement légendaire et grandes quantités d'or

### **Mécaniques de donjons**
- **Instances privées** : Chaque groupe a son donjon personnel
- **Maximum 4 joueurs** par instance de donjon
- **Boss avec capacités spéciales** : patterns d'attaque uniques
- **Spawn de sbires** : les boss invoquent des alliés pendant le combat
- **Notifications contextuelles** : alertes pour événements importants
- **Isolation complète** : monstres de donjon ne peuvent pas s'échapper
- **Récompenses basées sur la contribution** : XP et objets pour tous les participants

## 🎒 Inventaire et Objets

### **Interface d'inventaire optimisée**
- **Taille compacte** : 400x400px, ne chevauche plus avec l'UI
- **Défilement intelligent** : Maximum 6 objets visibles simultanément
- **Navigation fluide** : Flèches HAUT/BAS et molette de souris
- **Indicateur de position** : Affiche "objets X-Y sur Z total"
- **Réinitialisation automatique** : Retour en haut à chaque ouverture
- **Design épuré** : Interface sans encombrement visuel

### **Système de stacking avancé**
- **Limites par rareté** : 
  - Common : 50 objets par stack
  - Uncommon : 20 objets par stack  
  - Rare : 10 objets par stack
  - Epic : 5 objets par stack
  - Legendary : 2 objets par stack
- **Auto-groupement** : Objets identiques fusionnent automatiquement
- **Vérification des limites** : Prévention du dépassement de stack
- **Indicateurs visuels** : Affichage (quantité/maximum) pour chaque stack

### **Types d'objets et interactions**
- **Armes** : Clic pour équiper, améliore l'attaque
- **Armures** : Clic pour équiper, améliore la défense  
- **Consommables** : Clic pour utiliser, effets temporaires
- **Accessoires** : Clic pour équiper, bonus divers
- **Couleurs de rareté** : Gris→Vert→Bleu→Violet→Orange
- **Actions contextuelles** : [CLIC: équiper/utiliser/déséquiper]

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

### **Système de donjons**
- **3 donjons progressifs** avec conditions de niveau
- **Instances isolées** : chaque groupe a son donjon privé
- **Boss uniques** avec capacités spéciales et patterns d'attaque
- **Mécaniques spéciales** : Spawn de sbires, capacités de zone, buffs de boss
- **Nettoyage automatique** : suppression des monstres orphelins
- **Notifications contextuelles** : spawn de boss, capacités utilisées, completion

### **Objets et économie**
- **Drop rate** : 30% par monstre tué
- **Rareté pondérée** : Common 60%, Uncommon 25%, Rare 12%, Epic 2%, Legendary 1%
- **Auto-stack intelligent** avec vérification des limites
- **Inventaire avec défilement** : navigation fluide pour grands inventaires
- **Système d'or** intégré (prêt pour économie future)
- **Équipement contextuel** : clic pour équiper/utiliser/déséquiper

### **Monde et exploration**
- **9 zones thématiques** avec monstres spécialisés
- **Portails de donjons** : 3 emplacements fixes sur la carte
- **Noms raccourcis** dans les logs (ex: "Slime" au lieu de "Slime_plains_1")
- **Respawn par zone** respectant les types de monstres
- **Coordonnées monde** : 3200×2400 avec limites de mouvement
- **Système d'instances** : monde principal et instances de donjons séparées

## 🔧 Architecture technique

### **Serveur (`server.py`)**
- **Modèle client-serveur** avec threading
- **Communication TCP** via JSON + délimiteurs
- **Game loop 30 FPS** avec états synchronisés
- **Threading sécurisé** avec locks pour données partagées
- **Gestion d'erreurs robuste** avec timeouts et reconnexions
- **Système d'instances** : gestion séparée monde/donjons
- **Nettoyage automatique** : suppression périodique des monstres orphelins
- **Isolation des données** : états de jeu complètement séparés par instance

### **Client (`client.py`)**
- **Pygame 2.6.1** pour rendu et input
- **Système de caméra** avec conversion coordonnées monde/écran
- **Interface modulaire** avec panneaux masquables et défilants
- **Gestion d'état** locale avec synchronisation serveur
- **Optimisations d'affichage** (culling, cache)
- **Notifications contextuelles** : donjons, boss, événements
- **Navigation d'inventaire** avec défilement fluide et indicateurs

### **Structure des données**
```python
# Classes principales avec dataclasses
@dataclass
class Player:
    # Stats, inventaire, équipement, position, instance_id...

@dataclass 
class Monster:
    # HP, attaque, défense, récompenses XP, dungeon_instance...

@dataclass
class Item:
    # Type, rareté, stats, effets, stackable...

@dataclass
class ItemStack:
    # Gestion des quantités et limites

@dataclass
class DungeonInstance:
    # Boss, joueurs, monstres, état de completion...

@dataclass
class Boss:
    # Capacités spéciales, cooldowns, patterns d'attaque...
```

### **Système d'instances de donjons**
- **Isolation complète** : chaque instance a ses propres monstres et boss
- **Gestion automatique** : création/suppression dynamique des instances
- **Sécurisation des données** : protection contre les fuites entre instances
- **Nettoyage préventif** : détection et suppression des monstres orphelins
- **Synchronisation** : états de donjons synchronisés entre joueurs

## 🚧 Développement

### **Fonctionnalités complétées**
- ✅ Multijoueur stable avec 4 classes
- ✅ Combat et capacités spéciales  
- ✅ Grand monde avec 9 biomes et 74 monstres
- ✅ Système d'objets universel avec stacking intelligent
- ✅ Interface optimisée avec inventaire défilant
- ✅ Logs de combat compacts et masquables
- ✅ **Système de donjons complet** avec 3 donjons et boss
- ✅ **Instances isolées** avec gestion automatique des monstres
- ✅ **Interface d'inventaire optimisée** avec défilement fluide
- ✅ **Mécaniques de boss** avec capacités spéciales
- ✅ **Notifications contextuelles** pour événements de donjons
- ✅ **Nettoyage automatique** pour éviter les fuites de monstres

### **Détails techniques validés**
- ✅ Isolation complète des instances de donjons
- ✅ Système de défilement d'inventaire (6 objets visibles max)
- ✅ Interface compacte 400x400px sans chevauchement
- ✅ Boss avec patterns d'attaque et spawn de sbires
- ✅ Nettoyage périodique des monstres orphelins
- ✅ Tests automatisés pour toutes les fonctionnalités critiques

### **Roadmap future**
- 🎯 **Combat PvP** entre joueurs
- � **Donjons étendus** : plus de niveaux et mécaniques
- 🎨 **Sprites et animations** (remplacer les cercles)
- 🏪 **NPCs marchands** et économie complète
- 👥 **Guildes et chat global**
- 🗺️ **Quêtes et objectifs avec récompenses**
- 🎵 **Système audio** : musiques et effets sonores
- 📊 **Statistiques avancées** : classements et achievements

### **Améliorations récentes**
- 🆕 **Système de donjons** : 3 donjons avec boss et mécaniques uniques
- 🆕 **Inventaire optimisé** : défilement intelligent, interface compacte
- 🆕 **Isolation d'instances** : monstres de donjons parfaitement contenus
- 🆕 **Interface épurée** : suppression des éléments encombrants
- 🆕 **Navigation avancée** : contrôles intuitifs pour inventaires volumineux

### **Contribuer**
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📊 Statistiques du projet

- **Lignes de code** : ~1500 (serveur) + ~1400 (client)
- **Classes définies** : 12+ dataclasses principales
- **Monstres** : 74 répartis sur 9 zones + boss de donjons
- **Donjons** : 3 avec mécaniques uniques et boss épiques
- **Objets** : 15+ types avec 5 raretés et stacking intelligent
- **Résolution** : 800×600 avec monde 3200×2400
- **Performance** : 30 FPS stable en multijoueur avec instances
- **Inventaire** : Défilement optimisé, max 6 objets visibles
- **Interface** : Design compact 400x400px sans chevauchement
- **Fonctionnalités** : 15+ commandes clavier et interactions souris
- **Tests** : Suite de tests automatisés pour isolation et fonctionnalités

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- **MONKKIII** - Développement initial et architecture
- **Communauté** - Contributions et suggestions

---

**🎮 Bon jeu et bonne exploration !**

*Dernière mise à jour : Août 2025 - Version avec donjons et inventaire optimisé*