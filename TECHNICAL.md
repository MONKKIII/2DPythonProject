# Documentation Technique - RPG Multijoueur

## Architecture du Projet

### Vue d'ensemble
Ce projet implémente un RPG multijoueur 2D en temps réel utilisant une architecture client-serveur avec Python et Pygame.

### Structure des fichiers
```
2DPythonProject/
├── server.py          # Serveur de jeu (logique principale)
├── client.py          # Client Pygame (interface utilisateur)
├── config.py          # Configuration du jeu
├── launcher.py        # Script de lancement amélioré
├── launcher.bat       # Script batch pour Windows
├── test_server.py     # Tests de connexion
├── requirements.txt   # Dépendances Python
└── README.md         # Documentation utilisateur
```

## Architecture Réseau

### Protocole de Communication
- **Transport** : TCP (Socket)
- **Format** : JSON
- **Port par défaut** : 12345

### Messages Client → Serveur
```json
// Rejoindre le jeu
{
    "type": "join",
    "name": "NomDuJoueur"
}

// Mouvement
{
    "type": "move",
    "x": 450.0,
    "y": 300.0
}

// Attaquer un monstre
{
    "type": "attack_monster",
    "monster_id": "monster_0"
}

// Améliorer une statistique
{
    "type": "upgrade_stat",
    "stat": "attack"  // "attack", "defense", "speed", "hp"
}
```

### Messages Serveur → Client
```json
// Confirmation de connexion
{
    "type": "joined",
    "player_id": "player_0",
    "player": { /* données du joueur */ }
}

// État du jeu (30 FPS)
{
    "type": "game_state",
    "players": {
        "player_0": { /* données joueur */ }
    },
    "monsters": {
        "monster_0": { /* données monstre */ }
    }
}

// Résultat de combat
{
    "type": "combat_result",
    "log": "Alice attaque monster_0 pour 12 dégâts!",
    "player": { /* joueur mis à jour */ },
    "monster": { /* monstre mis à jour */ }
}
```

## Classes Principales

### Player (Dataclass)
```python
@dataclass
class Player:
    id: str              # Identifiant unique
    name: str            # Nom du joueur
    x: float = 400       # Position X
    y: float = 300       # Position Y
    hp: int = 100        # Points de vie actuels
    max_hp: int = 100    # Points de vie maximum
    level: int = 1       # Niveau du joueur
    xp: int = 0          # Expérience actuelle
    xp_to_next: int = 100 # XP requise pour le niveau suivant
    attack: int = 10     # Dégâts d'attaque
    defense: int = 5     # Réduction de dégâts
    speed: int = 5       # Vitesse de déplacement
    skill_points: int = 0 # Points de compétence disponibles
    alive: bool = True   # État vivant/mort
```

### Monster (Dataclass)
```python
@dataclass
class Monster:
    id: str              # Identifiant unique
    x: float             # Position X
    y: float             # Position Y
    hp: int              # Points de vie actuels
    max_hp: int          # Points de vie maximum
    attack: int          # Dégâts d'attaque
    defense: int         # Réduction de dégâts
    xp_reward: int       # XP donnée à la mort
    alive: bool = True   # État vivant/mort
    target_player: str = None # Joueur ciblé (non implémenté)
```

## Logique de Jeu

### Système de Combat
1. **Initiation** : Joueur attaque monstre (portée de 50 pixels)
2. **Calcul des dégâts** : `max(1, attaque_attaquant - defense_cible)`
3. **Application** : Réduction des HP de la cible
4. **Riposte** : Si le monstre survit, il contre-attaque
5. **Mort** : Si HP ≤ 0, la créature meurt

### Système d'Expérience
- **Gain XP** : Tuer un monstre donne son `xp_reward`
- **Montée de niveau** : Quand `xp >= xp_to_next`
- **Calcul du niveau suivant** : `xp_to_next *= 1.5`
- **Récompenses** : +3 points de compétence, +10 HP max, soins complets

### Système d'Amélioration
Chaque point de compétence permet :
- **Attaque** : +2 dégâts
- **Défense** : +2 réduction de dégâts
- **Vitesse** : +1 vitesse de déplacement
- **HP** : +15 HP maximum (+ soins immédiats)

### Respawn
- **Monstres** : Réapparaissent après 10 secondes à une position aléatoire
- **Joueurs** : Ressuscitent après 5 secondes avec 50% HP à une position aléatoire

## Threading et Concurrence

### Côté Serveur
- **Thread principal** : Accepte les nouvelles connexions
- **Thread par client** : Gère les messages d'un client spécifique
- **Thread de jeu** : Boucle principale à 30 FPS
- **Timers** : Respawn des entités

### Côté Client
- **Thread principal** : Interface Pygame et entrées utilisateur
- **Thread réseau** : Écoute les messages du serveur

## Gestion des Erreurs

### Déconnexions Client
- Détection automatique lors de l'envoi de messages
- Nettoyage des structures de données
- Fermeture propre des sockets

### Validation des Messages
- Vérification du format JSON
- Validation des types de messages
- Vérification de l'existence des entités

## Performance

### Optimisations Implémentées
- Envoi de l'état complet à 30 FPS seulement
- Messages de combat envoyés uniquement lors d'événements
- Troncature automatique des logs de combat (max 5 entrées)

### Limitations Actuelles
- Pas de système de zones (tous les joueurs voient tout)
- Pas de compression des messages réseau
- État complet envoyé à chaque frame (pas de delta)

## Sécurité

### Considérations
- Pas d'authentification (jeu local/LAN)
- Validation côté serveur des actions
- Pas de chiffrement (données en clair)
- Prévention des tricheries basiques

### Améliorations Possibles
- Authentification par mot de passe
- Chiffrement TLS
- Validation plus stricte des mouvements
- Rate limiting des actions

## Extensibilité

### Points d'Extension Faciles
1. **Nouvelles statistiques** : Ajouter dans les dataclasses
2. **Nouveaux types de monstres** : Modifier `spawn_monsters()`
3. **Nouveaux messages** : Ajouter dans `process_message()`
4. **Interface** : Modifier les fonctions `draw_*()` du client

### Améliorations Majeures Possibles
1. **Base de données** : Persistance des joueurs
2. **Cartes multiples** : Système de zones/instances
3. **IA des monstres** : Comportements complexes
4. **Objets et inventaire** : Système d'équipement
5. **Guildes et PvP** : Systèmes sociaux

## Tests et Débogage

### Scripts de Test
- `test_server.py` : Test de connexion et de communication basique
- `launcher.py` : Interface de lancement avec tests intégrés

### Débogage
- Logs serveur dans la console
- Affichage des erreurs réseau
- État du jeu visible dans l'interface client

## Déploiement

### Configuration Réseau
1. **LAN** : Utiliser l'IP locale du serveur
2. **Internet** : Configuration du routeur/pare-feu nécessaire
3. **Port forwarding** : Port 12345 TCP

### Prérequis Système
- Python 3.7+
- Pygame 2.6+
- Réseau fonctionnel entre les machines
