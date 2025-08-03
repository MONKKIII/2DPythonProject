# RPG Multijoueur 2D

Un petit jeu RPG multijoueur en réseau LAN créé avec Python et Pygame.

## Fonctionnalités

- **Multijoueur en réseau LAN** : Plusieurs joueurs peuvent se connecter au même serveur
- **4 Classes de personnages** : Guerrier, Mage, Archer, Voleur avec capacités spéciales
- **Système de niveaux** : Gagnez de l'expérience en tuant des monstres
- **Amélioration des statistiques** : Dépensez vos points de compétence pour améliorer votre personnage
- **Combat en temps réel** : Attaquez les monstres avec différentes stratégies
- **Système de critiques** : Coups critiques selon votre classe
- **Capacités spéciales** : Chaque classe a une capacité unique avec cooldown
- **Respawn automatique** : Les monstres et joueurs réapparaissent automatiquement

## Installation

1. Assurez-vous que Python 3.7+ est installé
2. Installez Pygame :
   ```
   pip install pygame
   ```

## Comment jouer

### Démarrer le serveur
```bash
python server.py
```
Le serveur se lance sur `localhost:12345` par défaut.

### Lancer le client
```bash
python client.py
```

Pour se connecter à un serveur distant :
```bash
python client.py <IP_DU_SERVEUR>
```

### Contrôles du jeu

- **WASD** ou **Flèches directionnelles** : Déplacer votre personnage
- **Espace** : Attaquer le monstre le plus proche (portée de 50 pixels)
- **Q** : Utiliser la capacité spéciale de votre classe
- **Clic gauche** : Attaquer un monstre spécifique
- **Tab** : Ouvrir/fermer le panneau d'amélioration des statistiques

### Sélection de classe

1. **Guerrier** : Tank avec beaucoup de HP et capacité Charge
2. **Mage** : Sorts puissants avec Boule de Feu
3. **Archer** : Critiques élevés avec Tir Multiple  
4. **Voleur** : Très rapide avec Furtivité

### Système de progression

1. **Choisissez votre classe** au début du jeu
2. **Tuez des monstres** pour gagner de l'XP
3. **Montez de niveau** pour obtenir des points de compétence
4. **Améliorez vos statistiques** :
   - **1** : Attaque (+2)
   - **2** : Défense (+2) 
   - **3** : Vitesse (+1)
   - **4** : HP Maximum (+15)
   - **5** : Mana Maximum (+10)
   - **6** : Chance Critique (+5%)

### Statistiques des personnages

- **HP** : Points de vie (vous mourrez si ça atteint 0)
- **Mana** : Points de magie pour les capacités spéciales
- **Attaque** : Dégâts infligés aux monstres
- **Défense** : Réduction des dégâts reçus
- **Vitesse** : Vitesse de déplacement
- **Critique** : Chance d'infliger des dégâts doublés
- **Niveau** : Votre niveau actuel
- **XP** : Expérience actuelle/requise pour le prochain niveau

## Architecture technique

### Serveur (`server.py`)
- Gère la logique du jeu (combats, niveaux, monstres)
- Synchronise l'état du jeu entre tous les clients
- Gère les connexions multiples avec des threads
- Respawn automatique des monstres

### Client (`client.py`)
- Interface graphique Pygame
- Communication réseau avec le serveur
- Gestion des entrées utilisateur
- Affichage en temps réel

### Communication réseau
- Protocole TCP avec JSON
- Messages : `join`, `move`, `attack_monster`, `upgrade_stat`
- État du jeu synchronisé à 30 FPS

## Personnalisation

Vous pouvez facilement modifier :

- **Statistiques des monstres** dans `server.py` (fonction `spawn_monsters`)
- **Vitesse du jeu** en changeant le FPS dans la boucle principale
- **Équilibrage** des niveaux et des dégâts
- **Apparence** en modifiant les couleurs et tailles dans `client.py`

## Problèmes connus

- ~~Les joueurs morts doivent redémarrer le client pour ressusciter~~ ✅ **CORRIGÉ** : Respawn automatique après 5 secondes
- Pas de sauvegarde de progression (tout est réinitialisé au redémarrage)
- Les monstres n'ont pas d'IA avancée

## Améliorations récentes

- ✅ **Système de classes** : 4 classes jouables avec capacités spéciales uniques
- ✅ **Combat amélioré** : Système de critiques et de mana
- ✅ **Capacités spéciales** : Chaque classe a sa capacité avec cooldown
- ✅ **Interface améliorée** : Sélection de classe, barres de mana, couleurs par classe
- ✅ **Multijoueur stable** : Correction des problèmes de blocage avec plusieurs joueurs
- ✅ **Meilleure gestion réseau** : Messages plus fiables, buffers améliorés
- ✅ **Respawn automatique** : Les joueurs ressuscitent automatiquement
- ✅ **Gestion d'erreurs** : Meilleure stabilité et logging des erreurs
- ✅ **Tests inclus** : Scripts de test pour vérifier le multijoueur

## Extensions possibles

1. **Sauvegarde** : Sauvegarder la progression des joueurs
2. **Objets et équipement** : Ajouter un système d'inventaire
3. **Sorts et compétences** : Différentes classes de personnages
4. **Cartes plus grandes** : Système de caméra et exploration
5. **PvP** : Combat entre joueurs
6. **Guildes** : Système de groupes de joueurs

## Dépannage

### Erreur de connexion
- Vérifiez que le serveur est démarré
- Vérifiez l'adresse IP et le port
- Assurez-vous que le pare-feu autorise les connexions

### Lag ou saccades
- Réduisez le nombre de monstres dans `spawn_monsters()`
- Augmentez l'intervalle de mise à jour du serveur

Amusez-vous bien ! 🎮
