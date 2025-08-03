# Configuration du jeu RPG Multijoueur

# Paramètres réseau
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# Paramètres de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_UPDATE_RATE = 30  # FPS pour les mises à jour du serveur

# Paramètres des joueurs
PLAYER_START_HP = 100
PLAYER_START_ATTACK = 10
PLAYER_START_DEFENSE = 5
PLAYER_START_SPEED = 5
PLAYER_SIZE = 15
ATTACK_RANGE = 50

# Paramètres de progression
XP_BASE = 100
XP_MULTIPLIER = 1.5
SKILL_POINTS_PER_LEVEL = 3
HP_BONUS_PER_LEVEL = 10

# Amélioration des statistiques (coût en points de compétence : bonus)
STAT_UPGRADES = {
    'attack': (1, 2),      # 1 point pour +2 attaque
    'defense': (1, 2),     # 1 point pour +2 défense
    'speed': (1, 1),       # 1 point pour +1 vitesse
    'hp': (1, 15)          # 1 point pour +15 HP max
}

# Paramètres des monstres
MONSTER_COUNT = 5
MONSTER_SIZE = 10
MONSTER_RESPAWN_TIME = 10  # secondes

# Statistiques des monstres (min, max)
MONSTER_HP_RANGE = (30, 60)
MONSTER_ATTACK_RANGE = (8, 15)
MONSTER_DEFENSE_RANGE = (2, 8)
MONSTER_XP_RANGE = (15, 30)

# Couleurs (R, G, B)
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0),
    'GRAY': (128, 128, 128),
    'GRASS': (34, 139, 34)
}
