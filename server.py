import socket
import threading
import json
import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
import traceback

@dataclass
class Item:
    id: str
    name: str
    item_type: str  # "weapon", "armor", "consumable", "accessory"
    rarity: str  # "common", "uncommon", "rare", "epic", "legendary"
    stats: Dict[str, int] = field(default_factory=dict)  # {"attack": 5, "defense": 2}
    effects: Dict[str, int] = field(default_factory=dict)  # Pour les consommables {"heal": 50}
    slot: str = ""  # "weapon", "armor", "accessory" pour l'équipement
    description: str = ""
    usable: bool = False  # True for consumables
    stackable: bool = False  # True pour les objets stackables (consommables)
    max_stack: int = 1  # Nombre maximum d'objets par stack

@dataclass
class ItemStack:
    item: Item
    quantity: int = 1

@dataclass
class Player:
    id: str
    name: str
    x: float = 1600  # Centre du monde (3200/2)
    y: float = 1200  # Centre du monde (2400/2)
    hp: int = 100
    max_hp: int = 100
    level: int = 1
    xp: int = 0
    xp_to_next: int = 100
    attack: int = 10
    defense: int = 5
    speed: int = 5
    skill_points: int = 0
    alive: bool = True
    player_class: str = "Warrior"  # "Warrior", "Mage", "Archer", "Rogue"
    mana: int = 50
    max_mana: int = 50
    critical_chance: float = 0.1  # 10% chance de critique
    last_ability_use: float = 0  # Timestamp pour cooldown des capacités
    inventory: Dict[str, ItemStack] = field(default_factory=dict)  # Dict des stacks avec ID comme clé
    equipped: Dict[str, Item] = field(default_factory=dict)  # {"weapon": Item, "armor": Item}
    gold: int = 0  # Monnaie du jeu
    socket: Any = None  # Référence socket pour communication

@dataclass
class DroppedItem:
    drop_id: str
    item_id: str
    x: float
    y: float
    drop_time: float  # Pour la disparition automatique

@dataclass
class Monster:
    id: str
    x: float
    y: float
    hp: int
    max_hp: int
    attack: int
    defense: int
    xp_reward: int
    alive: bool = True
    target_player: str = None

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: Dict[socket.socket, Player] = {}
        self.players: Dict[str, Player] = {}
        self.monsters: Dict[str, Monster] = {}
        self.items: Dict[str, Item] = {}  # Tous les objets du jeu
        self.dropped_items: Dict[str, DroppedItem] = {}  # Objets au sol
        self.item_counter = 0  # Pour générer des IDs uniques
        self.running = True
        self.lock = threading.Lock()  # Pour la synchronisation
        
        # Classes de personnages
        self.class_stats = {
            "Warrior": {"hp": 120, "attack": 12, "defense": 8, "speed": 4, "mana": 30, "crit": 0.05},
            "Mage": {"hp": 80, "attack": 15, "defense": 3, "speed": 6, "mana": 100, "crit": 0.15},
            "Archer": {"hp": 90, "attack": 14, "defense": 5, "speed": 8, "mana": 50, "crit": 0.20},
            "Rogue": {"hp": 85, "attack": 13, "defense": 4, "speed": 10, "mana": 40, "crit": 0.25}
        }
        
        # Spawn initial monsters
        self.spawn_monsters()
        
        # Initialize items database
        self.init_items()
        
    def spawn_monsters(self):
        """Spawn random monsters on the map"""
        # Spawn différents types de monstres selon les zones
        self.spawn_zone_monsters()
        
        # Ajouter quelques monstres aléatoires supplémentaires
        for i in range(20):
            monster_id = f"monster_random_{i}"
            self.monsters[monster_id] = Monster(
                id=monster_id,
                x=random.randint(100, 3100),
                y=random.randint(100, 2300),
                hp=random.randint(30, 60),
                max_hp=random.randint(30, 60),
                attack=random.randint(8, 15),
                defense=random.randint(2, 8),
                xp_reward=random.randint(15, 30)
            )
    
    def spawn_zone_monsters(self):
        """Spawn des monstres spécifiques dans chaque zone"""
        zone_width = 3200 // 3  # 1066
        zone_height = 2400 // 3  # 800
        
        zones = [
            # (zone_name, x_start, y_start, monster_prefix, count, level_range)
            ("plains", 0, 0, "Slime", 8, (20, 40)),
            ("forest", zone_width, 0, "Loup", 10, (35, 55)),
            ("mountains", zone_width*2, 0, "Orc", 12, (50, 70)),
            ("desert", 0, zone_height, "Momie", 10, (45, 65)),
            ("coast", zone_width, zone_height, "Pirate", 8, (55, 75)),
            ("volcano", zone_width*2, zone_height, "Drake", 6, (70, 90)),
            ("ice", 0, zone_height*2, "Yeti", 8, (40, 60)),
            ("swamp", zone_width, zone_height*2, "Troll", 7, (60, 80)),
            ("crystal", zone_width*2, zone_height*2, "Golem", 5, (80, 100))
        ]
        
        for zone_name, x_start, y_start, monster_type, count, (min_hp, max_hp) in zones:
            for i in range(count):
                monster_id = f"{monster_type}_{zone_name}_{i}"
                
                # Position dans la zone
                x = random.randint(x_start + 50, min(x_start + zone_width - 50, 3150))
                y = random.randint(y_start + 50, min(y_start + zone_height - 50, 2350))
                
                # Stats basées sur la zone
                hp = random.randint(min_hp, max_hp)
                attack = random.randint(8 + (min_hp // 10), 15 + (max_hp // 10))
                defense = random.randint(2 + (min_hp // 20), 8 + (max_hp // 15))
                xp = random.randint(15 + (min_hp // 5), 30 + (max_hp // 3))
                
                self.monsters[monster_id] = Monster(
                    id=monster_id,
                    x=x,
                    y=y,
                    hp=hp,
                    max_hp=hp,
                    attack=attack,
                    defense=defense,
                    xp_reward=xp
                )
    
    def init_items(self):
        """Initialize the items database"""
        # Armes (stackables avec limite raisonnable)
        self.items["iron_sword"] = Item("iron_sword", "Épée en Fer", "weapon", "common", {"attack": 3}, {}, "weapon", "Une épée basique mais solide", False, True, 10)
        self.items["magic_staff"] = Item("magic_staff", "Bâton Magique", "weapon", "uncommon", {"attack": 5, "max_mana": 20}, {}, "weapon", "Amplifie la magie", False, True, 5)
        self.items["elven_bow"] = Item("elven_bow", "Arc Elfique", "weapon", "rare", {"attack": 4, "critical_chance": 10}, {}, "weapon", "Arc léger et précis", False, True, 3)
        self.items["poison_daggers"] = Item("poison_daggers", "Dagues Empoisonnées", "weapon", "rare", {"attack": 2, "critical_chance": 15}, {}, "weapon", "Lames trempées dans le poison", False, True, 3)
        
        # Armures (stackables avec limite raisonnable)
        self.items["leather_armor"] = Item("leather_armor", "Armure de Cuir", "armor", "common", {"defense": 2, "speed": 1}, {}, "armor", "Protection légère", False, True, 10)
        self.items["mage_robe"] = Item("mage_robe", "Robe de Mage", "armor", "uncommon", {"defense": 1, "max_mana": 30}, {}, "armor", "Tissus enchantés", False, True, 5)
        self.items["plate_armor"] = Item("plate_armor", "Armure de Plates", "armor", "rare", {"defense": 5, "speed": -1}, {}, "armor", "Protection lourde", False, True, 3)
        self.items["shadow_cloak"] = Item("shadow_cloak", "Cape d'Ombre", "armor", "epic", {"defense": 1, "critical_chance": 20}, {}, "armor", "Cape des assassins", False, True, 2)
        
        # Consommables (stackables avec limites élevées)
        self.items["health_potion"] = Item("health_potion", "Potion de Vie", "consumable", "common", {}, {"heal": 50}, "", "Restaure la santé", True, True, 50)
        self.items["mana_potion"] = Item("mana_potion", "Potion de Mana", "consumable", "common", {}, {"mana": 30}, "", "Restaure la mana", True, True, 50)
        self.items["strength_elixir"] = Item("strength_elixir", "Élixir de Force", "consumable", "uncommon", {}, {"temp_attack": 5}, "", "Bonus temporaire", True, True, 20)
        
        # Accessoires (stackables avec limite raisonnable)
        self.items["power_ring"] = Item("power_ring", "Anneau de Puissance", "accessory", "epic", {"attack": 2, "defense": 2, "speed": 2}, {}, "accessory", "Bonus à tout", False, True, 2)
        self.items["regen_amulet"] = Item("regen_amulet", "Amulette de Régénération", "accessory", "rare", {"hp_regen": 2}, {}, "accessory", "Régénère la vie", False, True, 3)
        self.items["speed_boots"] = Item("speed_boots", "Bottes de Vitesse", "accessory", "uncommon", {"speed": 3}, {}, "accessory", "Déplacement rapide", False, True, 5)
    
    def start_server(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Serveur démarré sur {self.host}:{self.port}")
        
        # Start game loop in separate thread
        threading.Thread(target=self.game_loop, daemon=True).start()
        
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                print(f"Nouvelle connexion depuis {address}")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                print(f"Erreur serveur: {e}")
                break
    
    def handle_client(self, client_socket):
        client_socket.settimeout(30.0)  # Timeout de 30 secondes
        buffer = ""
        try:
            while self.running:
                try:
                    data = client_socket.recv(4096).decode('utf-8')
                    if not data:
                        break
                    
                    buffer += data
                    
                    # Process complete JSON messages
                    while '\n' in buffer or '}' in buffer:
                        try:
                            # Try to find a complete JSON message
                            if '\n' in buffer:
                                message_str, buffer = buffer.split('\n', 1)
                            else:
                                # Look for complete JSON by counting braces
                                brace_count = 0
                                for i, char in enumerate(buffer):
                                    if char == '{':
                                        brace_count += 1
                                    elif char == '}':
                                        brace_count -= 1
                                        if brace_count == 0:
                                            message_str = buffer[:i+1]
                                            buffer = buffer[i+1:]
                                            break
                                else:
                                    break  # No complete message yet
                            
                            if message_str.strip():
                                message = json.loads(message_str.strip())
                                self.process_message(client_socket, message)
                        except json.JSONDecodeError:
                            # Invalid JSON, skip this message
                            continue
                        except Exception as e:
                            print(f"Erreur traitement message: {e}")
                            continue
                            
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"Erreur réception: {e}")
                    break
                
        except Exception as e:
            print(f"Erreur client: {e}")
            traceback.print_exc()
        finally:
            self.disconnect_client(client_socket)
    
    def process_message(self, client_socket, message):
        try:
            msg_type = message.get('type')
            
            if msg_type == 'join':
                with self.lock:
                    player_name = message.get('name', 'Player')
                    player_class = message.get('class', 'Warrior')
                    player_id = f"player_{len(self.players)}"
                    
                    # Apply class stats
                    if player_class in self.class_stats:
                        stats = self.class_stats[player_class]
                        player = Player(
                            id=player_id, 
                            name=player_name,
                            player_class=player_class,
                            hp=stats["hp"],
                            max_hp=stats["hp"],
                            attack=stats["attack"],
                            defense=stats["defense"],
                            speed=stats["speed"],
                            mana=stats["mana"],
                            max_mana=stats["mana"],
                            critical_chance=stats["crit"]
                        )
                    else:
                        player = Player(id=player_id, name=player_name)
                    
                    self.players[player_id] = player
                    self.clients[client_socket] = player
                    player.socket = client_socket  # Ajouter la référence socket
                    
                    # Initialiser les stats et l'inventaire
                    self.calculate_player_stats(player)
                    
                    print(f"Joueur {player_name} ({player_class}) connecté avec l'ID {player_id}")
                    
                    # Send welcome message
                    response = {
                        'type': 'joined',
                        'player_id': player_id,
                        'player': self.player_to_dict(player)
                    }
                    self.send_to_client(client_socket, response)
                
            elif msg_type == 'move':
                with self.lock:
                    player = self.clients.get(client_socket)
                    if player and player.alive:
                        new_x = max(15, min(3200 - 15, float(message.get('x', player.x))))
                        new_y = max(15, min(2400 - 15, float(message.get('y', player.y))))
                        player.x = new_x
                        player.y = new_y
                    
            elif msg_type == 'attack_monster':
                with self.lock:
                    player = self.clients.get(client_socket)
                    monster_id = message.get('monster_id')
                    if player and player.alive and monster_id in self.monsters:
                        monster = self.monsters[monster_id]
                        if monster.alive:
                            self.handle_combat(player, monster)
                    
            elif msg_type == 'upgrade_stat':
                with self.lock:
                    player = self.clients.get(client_socket)
                    stat = message.get('stat')
                    if player and player.skill_points > 0:
                        self.upgrade_player_stat(player, stat)
                        
            elif msg_type == 'use_ability':
                with self.lock:
                    player = self.clients.get(client_socket)
                    ability = message.get('ability')
                    target_id = message.get('target_id')
                    if player and player.alive:
                        self.use_player_ability(player, ability, target_id)
                        
            elif msg_type == 'pickup_item':
                with self.lock:
                    player = self.clients.get(client_socket)
                    item_drop_id = message.get('item_drop_id')
                    if player and item_drop_id in self.dropped_items:
                        self.pickup_item(player, item_drop_id)
                        
            elif msg_type == 'equip_item':
                with self.lock:
                    player = self.clients.get(client_socket)
                    item_id = message.get('item_id')
                    if player and item_id in player.inventory:
                        self.equip_item(player, item_id)
                        
            elif msg_type == 'unequip_item':
                with self.lock:
                    player = self.clients.get(client_socket)
                    slot = message.get('slot')
                    if player and slot in player.equipped:
                        self.unequip_item(player, slot)
                        
            elif msg_type == 'use_item':
                with self.lock:
                    player = self.clients.get(client_socket)
                    item_id = message.get('item_id')
                    if player and item_id in player.inventory:
                        self.use_item(player, item_id)
        except Exception as e:
            print(f"Erreur traitement message {message}: {e}")
            traceback.print_exc()
    
    def handle_combat(self, player: Player, monster: Monster):
        if not monster.alive or not player.alive:
            return
            
        # Check for critical hit
        is_critical = random.random() < player.critical_chance
        damage_multiplier = 2.0 if is_critical else 1.0
        
        # Player attacks monster
        base_damage = max(1, player.attack - monster.defense)
        damage_to_monster = int(base_damage * damage_multiplier)
        monster.hp -= damage_to_monster
        
        # Messages de combat raccourcis
        monster_name = monster.id.split('_')[0]  # Prendre juste le type (ex: "Slime" au lieu de "Slime_plains_1")
        combat_log = f"⚔️ {damage_to_monster}"
        if is_critical:
            combat_log += " CRIT!"
        
        if monster.hp <= 0:
            monster.alive = False
            player.xp += monster.xp_reward
            combat_log += f" | {monster_name} vaincu (+{monster.xp_reward} XP)"
            
            # Drop d'objet possible
            self.drop_item(monster.x, monster.y)
            
            # Check level up
            if player.xp >= player.xp_to_next:
                self.level_up_player(player)
                combat_log += f" | NIVEAU {player.level}!"
            
            # Respawn monster after 10 seconds
            threading.Timer(10.0, self.respawn_monster, args=(monster.id,)).start()
        else:
            # Monster attacks back
            damage_to_player = max(1, monster.attack - player.defense)
            player.hp -= damage_to_player
            combat_log += f" | 🛡️ -{damage_to_player} HP"
            
            if player.hp <= 0:
                player.alive = False
                player.hp = 0
                combat_log += " | K.O.!"
                # Schedule respawn after 5 seconds
                threading.Timer(5.0, self.respawn_player, args=(player,)).start()
        
        # Broadcast combat result
        self.broadcast_message({
            'type': 'combat_result',
            'log': combat_log,
            'player': self.player_to_dict(player),
            'monster': self.monster_to_dict(monster)
        })
    
    def level_up_player(self, player: Player):
        player.level += 1
        player.xp -= player.xp_to_next
        player.xp_to_next = int(player.xp_to_next * 1.5)
        player.skill_points += 3
        player.max_hp += 10
        player.hp = player.max_hp  # Full heal on level up
    
    def upgrade_player_stat(self, player: Player, stat: str):
        if player.skill_points <= 0:
            return
            
        player.skill_points -= 1
        
        if stat == 'attack':
            player.attack += 2
        elif stat == 'defense':
            player.defense += 2
        elif stat == 'speed':
            player.speed += 1
        elif stat == 'hp':
            player.max_hp += 15
            player.hp += 15
        elif stat == 'mana':
            player.max_mana += 10
            player.mana += 10
        elif stat == 'critical':
            player.critical_chance += 0.05  # +5% chance critique
    
    def use_player_ability(self, player: Player, ability: str, target_id: str = None):
        """Utilise une capacité spéciale selon la classe du joueur"""
        current_time = time.time()
        cooldown = 3.0  # 3 secondes de cooldown
        
        if current_time - player.last_ability_use < cooldown:
            return  # Capacité en cooldown
        
        ability_used = False
        ability_log = ""
        
        if player.player_class == "Warrior" and ability == "charge":
            if player.mana >= 20:
                player.mana -= 20
                player.attack += 5  # Bonus temporaire d'attaque
                ability_log = f"⚡ Charge (+5 ATK)"
                ability_used = True
                # Retirer le bonus après 10 secondes
                threading.Timer(10.0, lambda: setattr(player, 'attack', player.attack - 5)).start()
                
        elif player.player_class == "Mage" and ability == "fireball":
            if player.mana >= 30 and target_id in self.monsters:
                player.mana -= 30
                monster = self.monsters[target_id]
                if monster.alive:
                    damage = int(player.attack * 1.5)
                    monster.hp -= damage
                    target_name = target_id.split('_')[0]
                    ability_log = f"🔥 Boule de Feu {damage} dmg"
                    ability_used = True
                    
                    if monster.hp <= 0:
                        monster.alive = False
                        player.xp += monster.xp_reward
                        ability_log += f" | +{monster.xp_reward} XP"
                        # Drop d'objet possible
                        self.drop_item(monster.x, monster.y)
                        threading.Timer(10.0, self.respawn_monster, args=(target_id,)).start()
                        
        elif player.player_class == "Archer" and ability == "multishot":
            if player.mana >= 25:
                player.mana -= 25
                targets_hit = 0
                total_damage = 0
                for monster in self.monsters.values():
                    if monster.alive and targets_hit < 3:  # Max 3 cibles
                        damage = max(1, int(player.attack * 0.7))
                        monster.hp -= damage
                        total_damage += damage
                        targets_hit += 1
                        
                        if monster.hp <= 0:
                            monster.alive = False
                            player.xp += monster.xp_reward
                            # Drop d'objet possible
                            self.drop_item(monster.x, monster.y)
                            threading.Timer(10.0, self.respawn_monster, args=(monster.id,)).start()
                
                if targets_hit > 0:
                    ability_log = f"🏹 Tir Multiple x{targets_hit} ({total_damage} dmg)"
                    ability_used = True
                    
        elif player.player_class == "Rogue" and ability == "stealth":
            if player.mana >= 15:
                player.mana -= 15
                player.critical_chance += 0.5  # Bonus critique temporaire
                ability_log = f"👤 Furtivité (+50% crit)"
                ability_used = True
                # Retirer le bonus après 8 secondes
                threading.Timer(8.0, lambda: setattr(player, 'critical_chance', player.critical_chance - 0.5)).start()
        
        if ability_used:
            player.last_ability_use = current_time
            self.broadcast_message({
                'type': 'ability_used',
                'log': ability_log,
                'player': self.player_to_dict(player)
            })
    
    def regenerate_mana(self):
        """Régénère la mana de tous les joueurs"""
        with self.lock:
            for player in self.players.values():
                if player.alive and player.mana < player.max_mana:
                    player.mana = min(player.max_mana, player.mana + 2)
    
    def respawn_player(self, player: Player):
        """Respawn a dead player"""
        player.alive = True
        player.hp = player.max_hp // 2  # Respawn with half health
        player.x = random.randint(100, 700)
        player.y = random.randint(100, 500)
    
    def respawn_monster(self, monster_id: str):
        """Respawn un monstre en respectant son type et sa zone"""
        # Vérifier si c'est un monstre de zone spécifique
        if "_" in monster_id and not monster_id.startswith("monster_random"):
            parts = monster_id.split("_")
            monster_type = parts[0]
            zone_name = parts[1] if len(parts) > 1 else "unknown"
            
            # Déterminer la zone de respawn
            zone_width = 3200 // 3  # 1066
            zone_height = 2400 // 3  # 800
            
            zone_coords = {
                "plains": (0, 0),
                "forest": (zone_width, 0),
                "mountains": (zone_width*2, 0),
                "desert": (0, zone_height),
                "coast": (zone_width, zone_height),
                "volcano": (zone_width*2, zone_height),
                "ice": (0, zone_height*2),
                "swamp": (zone_width, zone_height*2),
                "crystal": (zone_width*2, zone_height*2)
            }
            
            # Stats par type de monstre
            monster_stats = {
                "Slime": (20, 40, 8, 12, 2, 5, 15, 25),
                "Loup": (35, 55, 10, 15, 3, 6, 20, 30),
                "Orc": (50, 70, 12, 18, 5, 9, 25, 35),
                "Momie": (45, 65, 11, 16, 4, 8, 22, 32),
                "Pirate": (55, 75, 13, 19, 6, 10, 28, 38),
                "Drake": (70, 90, 15, 22, 8, 12, 35, 50),
                "Yeti": (40, 60, 10, 14, 4, 7, 20, 30),
                "Troll": (60, 80, 14, 20, 7, 11, 30, 45),
                "Golem": (80, 100, 16, 24, 10, 15, 40, 60)
            }
            
            if zone_name in zone_coords and monster_type in monster_stats:
                x_start, y_start = zone_coords[zone_name]
                min_hp, max_hp, min_att, max_att, min_def, max_def, min_xp, max_xp = monster_stats[monster_type]
                
                x = random.randint(x_start + 50, min(x_start + zone_width - 50, 3150))
                y = random.randint(y_start + 50, min(y_start + zone_height - 50, 2350))
                
                hp = random.randint(min_hp, max_hp)
                attack = random.randint(min_att, max_att)
                defense = random.randint(min_def, max_def)
                xp_reward = random.randint(min_xp, max_xp)
                
                self.monsters[monster_id] = Monster(
                    id=monster_id,
                    x=x,
                    y=y,
                    hp=hp,
                    max_hp=hp,
                    attack=attack,
                    defense=defense,
                    xp_reward=xp_reward
                )
                return
        
        # Respawn générique pour les monstres aléatoires
        self.monsters[monster_id] = Monster(
            id=monster_id,
            x=random.randint(100, 3100),
            y=random.randint(100, 2300),
            hp=random.randint(30, 60),
            max_hp=random.randint(30, 60),
            attack=random.randint(8, 15),
            defense=random.randint(2, 8),
            xp_reward=random.randint(15, 30)
        )
    
    def drop_item(self, monster_x, monster_y):
        """Détermine si un objet doit être lâché et le crée"""
        # 30% de chance de drop d'objet
        if random.random() < 0.3:
            item_id = self.select_random_item()
            drop_id = f"drop_{self.item_counter}"
            self.item_counter += 1
            
            drop = DroppedItem(
                drop_id=drop_id,
                item_id=item_id,
                x=monster_x,
                y=monster_y,
                drop_time=time.time()
            )
            self.dropped_items[drop_id] = drop
            
            # Notifier tous les clients du nouvel objet au sol
            drop_message = {
                'type': 'item_dropped',
                'drop_id': drop_id,
                'item_id': item_id,
                'x': monster_x,
                'y': monster_y
            }
            self.broadcast_message(drop_message)
    
    def select_random_item(self):
        """Sélectionne un objet aléatoire selon la rareté"""
        # Probabilités par rareté
        rarity_weights = {
            'common': 60,
            'uncommon': 25,
            'rare': 12,
            'epic': 2,
            'legendary': 1
        }
        
        # Filtrer les objets par rareté
        items_by_rarity = {}
        for item_id, item in self.items.items():
            rarity = item.rarity
            if rarity not in items_by_rarity:
                items_by_rarity[rarity] = []
            items_by_rarity[rarity].append(item_id)
        
        # Choisir une rareté
        rarity_choices = []
        weights = []
        for rarity, weight in rarity_weights.items():
            if rarity in items_by_rarity:
                rarity_choices.append(rarity)
                weights.append(weight)
        
        chosen_rarity = random.choices(rarity_choices, weights=weights)[0]
        return random.choice(items_by_rarity[chosen_rarity])
    
    def pickup_item(self, player, drop_id):
        """Ramasse un objet au sol"""
        if drop_id not in self.dropped_items:
            return
            
        dropped_item = self.dropped_items[drop_id]
        item = self.items.get(dropped_item.item_id)
        
        if not item:
            return
            
        # Vérifier la distance
        distance = ((player.x - dropped_item.x) ** 2 + (player.y - dropped_item.y) ** 2) ** 0.5
        if distance > 50:  # Portée de ramassage
            return
            
        # Gérer les stacks d'objets
        if item.stackable and item.id in player.inventory:
            # L'objet existe déjà dans l'inventaire et est stackable
            existing_stack = player.inventory[item.id]
            if existing_stack.quantity < item.max_stack:
                # Il y a de la place dans le stack existant
                existing_stack.quantity += 1
                del self.dropped_items[drop_id]
                
                # Notifier le joueur
                self.send_to_client(player.socket, {
                    'type': 'item_picked_up',
                    'item_id': dropped_item.item_id,
                    'item_name': item.name,
                    'quantity': existing_stack.quantity
                })
                
                # Notifier tous les clients que l'objet a été ramassé
                self.broadcast_message({
                    'type': 'item_removed',
                    'drop_id': drop_id
                })
                return
        
        # Vérifier si l'inventaire a de la place pour un nouvel item
        if len(player.inventory) >= 20:  # Limite d'inventaire
            return
            
        # Ajouter à l'inventaire comme nouveau stack
        player.inventory[dropped_item.item_id] = ItemStack(item=item, quantity=1)
        del self.dropped_items[drop_id]
        
        # Notifier le joueur
        self.send_to_client(player.socket, {
            'type': 'item_picked_up',
            'item_id': dropped_item.item_id,
            'item_name': item.name,
            'quantity': 1
        })
        
        # Notifier tous les clients que l'objet a été ramassé
        self.broadcast_message({
            'type': 'item_removed',
            'drop_id': drop_id
        })
    
    def equip_item(self, player, item_id):
        """Équipe un objet"""
        if item_id not in player.inventory:
            return
            
        item_stack = player.inventory[item_id]
        item = item_stack.item
        
        if item.item_type not in ['weapon', 'armor', 'accessory']:
            return
            
        # Déterminer le slot d'équipement
        slot = item.slot
        
        # Si quelque chose est déjà équipé dans ce slot, le déséquiper
        if slot in player.equipped:
            old_item = player.equipped[slot]
            del player.equipped[slot]
            # Créer un nouveau stack pour l'ancien objet équipé
            if old_item.id in player.inventory:
                player.inventory[old_item.id].quantity += 1
            else:
                player.inventory[old_item.id] = ItemStack(item=old_item, quantity=1)
            
        # Équiper le nouvel objet
        player.equipped[slot] = item
        
        # Retirer un exemplaire du stack
        item_stack.quantity -= 1
        if item_stack.quantity <= 0:
            del player.inventory[item_id]
        
        # Recalculer les stats
        self.calculate_player_stats(player)
        
        # Notifier le joueur
        self.send_to_client(player.socket, {
            'type': 'item_equipped',
            'item_id': item_id,
            'item_name': item.name,
            'slot': slot
        })
    
    def unequip_item(self, player, slot):
        """Déséquipe un objet"""
        if slot not in player.equipped:
            return
            
        # Vérifier si l'inventaire a de la place
        if len(player.inventory) >= 20:
            return
            
        # Déséquiper l'objet
        item = player.equipped[slot]
        del player.equipped[slot]
        
        # Ajouter à l'inventaire comme nouveau stack ou ajouter au stack existant
        if item.id in player.inventory:
            player.inventory[item.id].quantity += 1
        else:
            player.inventory[item.id] = ItemStack(item=item, quantity=1)
        
        # Recalculer les stats
        self.calculate_player_stats(player)
        
        # Notifier le joueur
        self.send_to_client(player.socket, {
            'type': 'item_unequipped',
            'item_id': item.id,
            'item_name': item.name,
            'slot': slot
        })
    
    def use_item(self, player, item_id):
        """Utilise un objet consommable"""
        if item_id not in player.inventory:
            return
            
        item_stack = player.inventory[item_id]
        item = item_stack.item
        
        if item.item_type != 'consumable':
            self.send_message(player.socket, {
                'type': 'message',
                'text': "Cet objet ne peut pas être utilisé!"
            })
            return
            
        # Appliquer les effets
        effects_applied = []
        
        for effect, value in item.effects.items():
            if effect == 'heal':
                old_hp = player.hp
                player.hp = min(player.max_hp, player.hp + value)
                if player.hp > old_hp:
                    effects_applied.append(f"Récupère {player.hp - old_hp} HP")
                    
            elif effect == 'mana':
                old_mana = player.mana
                player.mana = min(player.max_mana, player.mana + value)
                if player.mana > old_mana:
                    effects_applied.append(f"Récupère {player.mana - old_mana} mana")
                    
            elif effect == 'strength_boost':
                # Effet temporaire (à implémenter plus tard)
                effects_applied.append(f"Force +{value} temporaire")
                
        # Retirer l'objet de l'inventaire (réduire la quantité)
        item_stack.quantity -= 1
        if item_stack.quantity <= 0:
            del player.inventory[item_id]
        
        # Notifier le joueur
        if effects_applied:
            self.send_to_client(player.socket, {
                'type': 'item_used',
                'item_id': item_id,
                'item_name': item.name,
                'effects': effects_applied
            })
    
    def calculate_player_stats(self, player):
        """Recalcule les stats du joueur en fonction de l'équipement"""
        # Stats de base par classe
        base_stats = {
            'warrior': {'attack': 12, 'defense': 10, 'speed': 6, 'critical_chance': 0.05},
            'mage': {'attack': 8, 'defense': 6, 'speed': 8, 'critical_chance': 0.15},
            'archer': {'attack': 10, 'defense': 7, 'speed': 12, 'critical_chance': 0.20},
            'rogue': {'attack': 9, 'defense': 5, 'speed': 14, 'critical_chance': 0.25}
        }
        
        # Commencer avec les stats de base + niveau
        base = base_stats.get(player.player_class.lower(), base_stats['warrior'])
        
        # Recalculer depuis la base (pas cumulatif)
        player.attack = base['attack'] + (player.level - 1) * 2
        player.defense = base['defense'] + (player.level - 1) * 2
        player.speed = base['speed'] + (player.level - 1) * 1
        player.critical_chance = base['critical_chance'] + (player.level - 1) * 0.01
        
        # Ajouter les bonus d'équipement
        for item in player.equipped.values():
            if hasattr(item, 'stats'):
                for stat, value in item.stats.items():
                    if hasattr(player, stat):
                        current_value = getattr(player, stat)
                        setattr(player, stat, current_value + value)
        
        # Recalculer HP et mana max basés sur attack et defense au lieu de strength/intelligence
        old_max_hp = player.max_hp
        old_max_mana = player.max_mana
        
        # Base HP/Mana par classe + bonus de niveau + bonus de stats
        class_base_hp = {'warrior': 120, 'mage': 80, 'archer': 90, 'rogue': 85}
        class_base_mana = {'warrior': 30, 'mage': 100, 'archer': 50, 'rogue': 40}
        
        base_hp = class_base_hp.get(player.player_class.lower(), 100)
        base_mana = class_base_mana.get(player.player_class.lower(), 50)
        
        player.max_hp = base_hp + (player.level - 1) * 20 + player.attack * 2
        player.max_mana = base_mana + (player.level - 1) * 10 + (player.level * 2)
        
        # Ajuster HP et mana actuels proportionnellement
        if old_max_hp > 0:
            hp_ratio = player.hp / old_max_hp
            player.hp = int(player.max_hp * hp_ratio)
        else:
            player.hp = player.max_hp
            
        if old_max_mana > 0:
            mana_ratio = player.mana / old_max_mana
            player.mana = int(player.max_mana * mana_ratio)
        else:
            player.mana = player.max_mana
            player.mana = player.max_mana
    
    def game_loop(self):
        """Main game loop - sends game state to all clients"""
        last_mana_regen = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Regenerate mana every 2 seconds
                if current_time - last_mana_regen >= 2.0:
                    self.regenerate_mana()
                    last_mana_regen = current_time
                
                with self.lock:
                    game_state = {
                        'type': 'game_state',
                        'players': {pid: self.player_to_dict(p) for pid, p in self.players.items()},
                        'monsters': {mid: self.monster_to_dict(m) for mid, m in self.monsters.items()},
                        'dropped_items': {did: self.dropped_item_to_dict(d) for did, d in self.dropped_items.items()}
                    }
                
                if self.clients:  # Only broadcast if there are clients
                    self.broadcast_message(game_state)
                    
                time.sleep(1/30)  # 30 FPS
            except Exception as e:
                print(f"Erreur game loop: {e}")
                time.sleep(0.1)
    
    def player_to_dict(self, player: Player):
        return {
            'id': player.id,
            'name': player.name,
            'x': player.x,
            'y': player.y,
            'hp': player.hp,
            'max_hp': player.max_hp,
            'level': player.level,
            'xp': player.xp,
            'xp_to_next': player.xp_to_next,
            'attack': player.attack,
            'defense': player.defense,
            'speed': player.speed,
            'skill_points': player.skill_points,
            'alive': player.alive,
            'player_class': player.player_class,
            'mana': player.mana,
            'max_mana': player.max_mana,
            'critical_chance': player.critical_chance,
            'gold': player.gold,
            'inventory': {item_id: {
                'name': item_stack.item.name, 
                'type': item_stack.item.item_type, 
                'rarity': item_stack.item.rarity,
                'quantity': item_stack.quantity,
                'max_stack': item_stack.item.max_stack
            } for item_id, item_stack in player.inventory.items()},
            'equipped': {slot: {'name': item.name, 'type': item.item_type, 'rarity': item.rarity}
                        for slot, item in player.equipped.items()}
        }
    
    def monster_to_dict(self, monster: Monster):
        return {
            'id': monster.id,
            'x': monster.x,
            'y': monster.y,
            'hp': monster.hp,
            'max_hp': monster.max_hp,
            'attack': monster.attack,
            'defense': monster.defense,
            'xp_reward': monster.xp_reward,
            'alive': monster.alive
        }
    
    def dropped_item_to_dict(self, dropped_item: DroppedItem):
        item = self.items.get(dropped_item.item_id)
        return {
            'drop_id': dropped_item.drop_id,
            'item_id': dropped_item.item_id,
            'item_name': item.name if item else 'Unknown Item',
            'item_rarity': item.rarity if item else 'common',
            'x': dropped_item.x,
            'y': dropped_item.y,
            'drop_time': dropped_item.drop_time
        }
    
    def broadcast_message(self, message):
        """Send message to all connected clients"""
        if not self.clients:
            return
            
        message_str = json.dumps(message) + '\n'
        disconnected_clients = []
        
        for client_socket in list(self.clients.keys()):
            try:
                client_socket.send(message_str.encode('utf-8'))
            except (ConnectionResetError, BrokenPipeError, OSError):
                disconnected_clients.append(client_socket)
            except Exception as e:
                print(f"Erreur envoi broadcast: {e}")
                disconnected_clients.append(client_socket)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            self.disconnect_client(client)
    
    def send_to_client(self, client_socket, message):
        """Send message to specific client"""
        try:
            message_str = json.dumps(message) + '\n'
            client_socket.send(message_str.encode('utf-8'))
        except (ConnectionResetError, BrokenPipeError, OSError):
            self.disconnect_client(client_socket)
        except Exception as e:
            print(f"Erreur envoi client: {e}")
            self.disconnect_client(client_socket)
    
    def disconnect_client(self, client_socket):
        try:
            with self.lock:
                if client_socket in self.clients:
                    player = self.clients[client_socket]
                    print(f"Déconnexion de {player.name}")
                    
                    # Remove from players dict
                    if player.id in self.players:
                        del self.players[player.id]
                    
                    # Remove from clients dict
                    del self.clients[client_socket]
        except Exception as e:
            print(f"Erreur déconnexion: {e}")
            
        try:
            client_socket.close()
        except:
            pass
    
    def stop_server(self):
        self.running = False
        self.socket.close()

if __name__ == "__main__":
    server = GameServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
        server.stop_server()
