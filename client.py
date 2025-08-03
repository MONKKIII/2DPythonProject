import pygame
import socket
import json
import threading
import sys
from typing import Dict, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# World constants
WORLD_WIDTH = 3200
WORLD_HEIGHT = 2400
TILE_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)

# Rarity colors
RARITY_COLORS = {
    'common': GRAY,
    'uncommon': GREEN,
    'rare': BLUE,
    'epic': PURPLE,
    'legendary': ORANGE
}

class GameClient:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG Multijoueur")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Game state
        self.running = True
        self.connected = False
        self.socket = None
        self.my_player_id = None
        self.players = {}
        self.monsters = {}
        self.dropped_items = {}
        self.combat_log = []
        self.show_stats_panel = False
        self.show_class_selection = True
        self.show_inventory = False
        self.show_controls = False
        self.show_combat_log = False  # Logs masqués par défaut
        self.selected_class = "Warrior"
        
        # Input
        self.keys_pressed = set()
        self.player_name = ""
        self.input_active = True
        
        # Camera system
        self.camera_x = 0
        self.camera_y = 0
        self.show_minimap = True
        
    def connect_to_server(self, host='localhost', port=12345):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            
            # Start listening for messages
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
            
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False
    
    def listen_for_messages(self):
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                
                # Process complete messages (separated by newlines)
                while '\n' in buffer:
                    message_str, buffer = buffer.split('\n', 1)
                    if message_str.strip():
                        try:
                            message = json.loads(message_str.strip())
                            self.process_server_message(message)
                        except json.JSONDecodeError as e:
                            print(f"Erreur JSON: {e}")
                            continue
                        except Exception as e:
                            print(f"Erreur traitement message: {e}")
                            continue
                
            except Exception as e:
                print(f"Erreur réception: {e}")
                break
        
        self.connected = False
    
    def process_server_message(self, message):
        msg_type = message.get('type')
        
        if msg_type == 'joined':
            self.my_player_id = message['player_id']
            self.players[self.my_player_id] = message['player']
            
        elif msg_type == 'game_state':
            self.players = message['players']
            self.monsters = message['monsters']
            if 'dropped_items' in message:
                self.dropped_items = message['dropped_items']
            
        elif msg_type == 'combat_result':
            self.combat_log.append(message['log'])
            if len(self.combat_log) > 3:  # Réduire à 3 lignes max
                self.combat_log.pop(0)
            
            # Update player and monster state
            if 'player' in message:
                player_data = message['player']
                self.players[player_data['id']] = player_data
            
            if 'monster' in message:
                monster_data = message['monster']
                self.monsters[monster_data['id']] = monster_data
            
        elif msg_type == 'ability_used':
            self.combat_log.append(message['log'])
            if len(self.combat_log) > 3:  # Réduire à 3 lignes max
                self.combat_log.pop(0)
            
            # Update player state
            if 'player' in message:
                player_data = message['player']
                self.players[player_data['id']] = player_data
                
        elif msg_type == 'item_picked_up':
            item_name = message.get('item_name', 'Objet')
            self.combat_log.append(f"📦 {item_name}")
            if len(self.combat_log) > 3:  # Réduire à 3 lignes max
                self.combat_log.pop(0)
                
        elif msg_type == 'item_used':
            effects = message.get('effects', [])
            if effects:
                effect_text = ", ".join(effects)
                self.combat_log.append(f"💊 {effect_text}")
                if len(self.combat_log) > 3:  # Réduire à 3 lignes max
                    self.combat_log.pop(0)
    
    def send_message(self, message):
        if self.connected:
            try:
                message_str = json.dumps(message) + '\n'
                self.socket.send(message_str.encode('utf-8'))
            except Exception as e:
                print(f"Erreur envoi: {e}")
                self.connected = False
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if self.show_class_selection:
                        if event.key == pygame.K_1:
                            self.selected_class = "Warrior"
                        elif event.key == pygame.K_2:
                            self.selected_class = "Mage"
                        elif event.key == pygame.K_3:
                            self.selected_class = "Archer"
                        elif event.key == pygame.K_4:
                            self.selected_class = "Rogue"
                        elif event.key == pygame.K_RETURN:
                            if self.player_name.strip():
                                self.show_class_selection = False
                                self.join_game()
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            if len(self.player_name) < 15:
                                self.player_name += event.unicode
                    else:
                        if event.key == pygame.K_RETURN:
                            if self.player_name.strip():
                                self.join_game()
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            if len(self.player_name) < 15:
                                self.player_name += event.unicode
                else:
                    if event.key == pygame.K_TAB:
                        self.show_stats_panel = not self.show_stats_panel
                    elif event.key == pygame.K_i:
                        self.show_inventory = not self.show_inventory
                    elif event.key == pygame.K_m:
                        self.show_minimap = not self.show_minimap
                    elif event.key == pygame.K_h:
                        self.show_controls = not self.show_controls
                    elif event.key == pygame.K_l:  # Touche L pour masquer/afficher les logs
                        self.show_combat_log = not self.show_combat_log
                    elif event.key == pygame.K_1 and self.show_stats_panel:
                        self.upgrade_stat('attack')
                    elif event.key == pygame.K_2 and self.show_stats_panel:
                        self.upgrade_stat('defense')
                    elif event.key == pygame.K_3 and self.show_stats_panel:
                        self.upgrade_stat('speed')
                    elif event.key == pygame.K_4 and self.show_stats_panel:
                        self.upgrade_stat('hp')
                    elif event.key == pygame.K_5 and self.show_stats_panel:
                        self.upgrade_stat('mana')
                    elif event.key == pygame.K_6 and self.show_stats_panel:
                        self.upgrade_stat('critical')
                    elif event.key == pygame.K_SPACE:
                        self.attack_nearest_monster()
                    elif event.key == pygame.K_q:  # Capacité spéciale
                        self.use_ability()
                
                self.keys_pressed.add(event.key)
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.input_active:  # Left click
                    mouse_pos = event.pos
                    # Vérifier si on clique dans l'inventaire
                    if self.show_inventory and self.handle_inventory_click(mouse_pos):
                        pass  # Action d'inventaire effectuée
                    # Vérifier si on clique sur un objet au sol
                    elif self.try_pickup_item(mouse_pos):
                        pass  # Objet ramassé
                    else:
                        # Sinon attaquer un monstre
                        self.attack_monster_at_position(mouse_pos)
    
    def join_game(self):
        if self.connected:
            message = {
                'type': 'join',
                'name': self.player_name,
                'class': self.selected_class
            }
            self.send_message(message)
            self.input_active = False
    
    def update_player_movement(self):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        try:
            player = self.players[self.my_player_id]
            if not player['alive']:
                return
            
            speed = player['speed']
            dx, dy = 0, 0
            
            if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
                dx = -speed
            if pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
                dx = speed
            if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
                dy = -speed
            if pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
                dy = speed
            
            if dx != 0 or dy != 0:
                new_x = max(15, min(WORLD_WIDTH - 15, player['x'] + dx))
                new_y = max(15, min(WORLD_HEIGHT - 15, player['y'] + dy))
                
                message = {
                    'type': 'move',
                    'x': new_x,
                    'y': new_y
                }
                self.send_message(message)
        except Exception as e:
            print(f"Erreur mouvement: {e}")
    
    def get_current_zone(self, x, y):
        """Retourne la zone actuelle du joueur"""
        zone_width = WORLD_WIDTH // 3
        zone_height = WORLD_HEIGHT // 3
        
        zones = [
            ("Plaines de Départ", 0, 0, zone_width, zone_height),
            ("Forêt Sombre", zone_width, 0, zone_width, zone_height),
            ("Montagnes", zone_width*2, 0, zone_width, zone_height),
            ("Désert Maudit", 0, zone_height, zone_width, zone_height),
            ("Côte des Pirates", zone_width, zone_height, zone_width, zone_height),
            ("Volcan Actif", zone_width*2, zone_height, zone_width, zone_height),
            ("Terres Gelées", 0, zone_height*2, zone_width, zone_height),
            ("Marais Toxique", zone_width, zone_height*2, zone_width, zone_height),
            ("Cavernes Cristal", zone_width*2, zone_height*2, zone_width, zone_height)
        ]
        
        for zone_name, zx, zy, zw, zh in zones:
            if zx <= x < zx + zw and zy <= y < zy + zh:
                return zone_name
        return "Zone Inconnue"
    
    def update_camera(self):
        """Met à jour la position de la caméra pour suivre le joueur"""
        if not self.my_player_id or self.my_player_id not in self.players:
            return
            
        player = self.players[self.my_player_id]
        
        # Centrer la caméra sur le joueur
        target_camera_x = player['x'] - SCREEN_WIDTH // 2
        target_camera_y = player['y'] - SCREEN_HEIGHT // 2
        
        # Limiter la caméra aux bords du monde
        self.camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, target_camera_x))
        self.camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, target_camera_y))
    
    def world_to_screen(self, world_x, world_y):
        """Convertit les coordonnées monde en coordonnées écran"""
        screen_x = world_x - self.camera_x
        screen_y = world_y - self.camera_y
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x, screen_y):
        """Convertit les coordonnées écran en coordonnées monde"""
        world_x = screen_x + self.camera_x
        world_y = screen_y + self.camera_y
        return world_x, world_y
    
    def draw_world_background(self):
        """Dessine le fond du monde avec les différentes zones"""
        # Définir les zones avec leurs couleurs - arrangement 3x3 simple
        zone_width = WORLD_WIDTH // 3  # 1066.67 ≈ 1067
        zone_height = WORLD_HEIGHT // 3  # 800
        
        zones = [
            # Zone, x, y, width, height, color, name
            ("plains", 0, 0, zone_width, zone_height, (34, 139, 34), "Plaines de Départ"),  # Vert - Zone de spawn
            ("forest", zone_width, 0, zone_width, zone_height, (0, 100, 0), "Forêt Sombre"),  # Vert foncé
            ("mountains", zone_width*2, 0, zone_width, zone_height, (139, 137, 137), "Montagnes"),  # Gris
            ("desert", 0, zone_height, zone_width, zone_height, (238, 203, 173), "Désert Maudit"),  # Beige
            ("coast", zone_width, zone_height, zone_width, zone_height, (65, 105, 225), "Côte des Pirates"),  # Bleu
            ("volcano", zone_width*2, zone_height, zone_width, zone_height, (139, 69, 19), "Volcan Actif"),  # Marron rouge
            ("ice", 0, zone_height*2, zone_width, zone_height, (176, 224, 230), "Terres Gelées"),  # Bleu glacé
            ("swamp", zone_width, zone_height*2, zone_width, zone_height, (85, 107, 47), "Marais Toxique"),  # Vert olive
            ("crystal", zone_width*2, zone_height*2, zone_width, zone_height, (138, 43, 226), "Cavernes Cristal")  # Violet
        ]
        
        for zone_id, zx, zy, zw, zh, color, name in zones:
            # Calculer les coordonnées d'écran pour cette zone
            screen_x, screen_y = self.world_to_screen(zx, zy)
            screen_x2, screen_y2 = self.world_to_screen(zx + zw, zy + zh)
            
            # Calculer les dimensions d'écran
            screen_w = screen_x2 - screen_x
            screen_h = screen_y2 - screen_y
            
            # Ne dessiner que si la zone est visible à l'écran
            if (screen_x < SCREEN_WIDTH and screen_x + screen_w > 0 and 
                screen_y < SCREEN_HEIGHT and screen_y + screen_h > 0):
                
                # Dessiner la zone
                pygame.draw.rect(self.screen, color, (screen_x, screen_y, screen_w, screen_h))
        
        # Dessiner la grille
        self.draw_world_grid()
    
    def draw_world_grid(self):
        """Dessine une grille sur le monde visible"""
        # Calculer les lignes de grille visibles
        start_x = int((self.camera_x // TILE_SIZE) * TILE_SIZE)
        start_y = int((self.camera_y // TILE_SIZE) * TILE_SIZE)
        
        # Lignes verticales
        for x in range(start_x, int(self.camera_x + SCREEN_WIDTH + TILE_SIZE), TILE_SIZE):
            screen_x, _ = self.world_to_screen(x, 0)
            if 0 <= screen_x <= SCREEN_WIDTH:
                pygame.draw.line(self.screen, (40, 150, 40), (screen_x, 0), (screen_x, SCREEN_HEIGHT), 1)
        
        # Lignes horizontales  
        for y in range(start_y, int(self.camera_y + SCREEN_HEIGHT + TILE_SIZE), TILE_SIZE):
            _, screen_y = self.world_to_screen(0, y)
            if 0 <= screen_y <= SCREEN_HEIGHT:
                pygame.draw.line(self.screen, (40, 150, 40), (0, screen_y), (SCREEN_WIDTH, screen_y), 1)
    
    def draw_minimap(self):
        """Dessine la mini-carte"""
        if not self.show_minimap:
            return
            
        # Taille et position de la mini-carte
        minimap_size = 150
        minimap_x = SCREEN_WIDTH - minimap_size - 10
        minimap_y = SCREEN_HEIGHT - minimap_size - 10
        
        # Fond de la mini-carte
        pygame.draw.rect(self.screen, (0, 0, 0, 128), (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(self.screen, WHITE, (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Échelle de la mini-carte
        scale_x = minimap_size / WORLD_WIDTH
        scale_y = minimap_size / WORLD_HEIGHT
        
        # Dessiner les zones sur la mini-carte
        zone_width = WORLD_WIDTH // 3
        zone_height = WORLD_HEIGHT // 3
        zones = [
            (0, 0, zone_width, zone_height, (34, 139, 34)),  # Plaines
            (zone_width, 0, zone_width, zone_height, (0, 100, 0)),  # Forêt
            (zone_width*2, 0, zone_width, zone_height, (139, 137, 137)),  # Montagnes
            (0, zone_height, zone_width, zone_height, (238, 203, 173)),  # Désert
            (zone_width, zone_height, zone_width, zone_height, (65, 105, 225)),  # Côte
            (zone_width*2, zone_height, zone_width, zone_height, (139, 69, 19)),  # Volcan
            (0, zone_height*2, zone_width, zone_height, (176, 224, 230)),  # Glace
            (zone_width, zone_height*2, zone_width, zone_height, (85, 107, 47)),  # Marais
            (zone_width*2, zone_height*2, zone_width, zone_height, (138, 43, 226)),  # Cristal
        ]
        
        for zx, zy, zw, zh, color in zones:
            mini_x = int(minimap_x + zx * scale_x)
            mini_y = int(minimap_y + zy * scale_y)
            mini_w = int(zw * scale_x)
            mini_h = int(zh * scale_y)
            pygame.draw.rect(self.screen, color, (mini_x, mini_y, mini_w, mini_h))
        
        # Dessiner les joueurs
        for player in self.players.values():
            if player['alive']:
                mini_px = int(minimap_x + player['x'] * scale_x)
                mini_py = int(minimap_y + player['y'] * scale_y)
                
                if player['id'] == self.my_player_id:
                    pygame.draw.circle(self.screen, YELLOW, (mini_px, mini_py), 3)
                else:
                    pygame.draw.circle(self.screen, WHITE, (mini_px, mini_py), 2)
        
        # Dessiner la vue actuelle (rectangle de caméra)
        view_x = int(minimap_x + self.camera_x * scale_x)
        view_y = int(minimap_y + self.camera_y * scale_y)
        view_w = int(SCREEN_WIDTH * scale_x)
        view_h = int(SCREEN_HEIGHT * scale_y)
        pygame.draw.rect(self.screen, RED, (view_x, view_y, view_w, view_h), 1)
        
        # Titre de la mini-carte
        minimap_title = pygame.font.Font(None, 16).render("Mini-carte (M)", True, WHITE)
        self.screen.blit(minimap_title, (minimap_x, minimap_y - 20))
    
    def attack_nearest_monster(self):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        player = self.players[self.my_player_id]
        if not player['alive']:
            return
        
        nearest_monster = None
        min_distance = float('inf')
        
        for monster in self.monsters.values():
            if not monster['alive']:
                continue
            
            distance = ((player['x'] - monster['x']) ** 2 + (player['y'] - monster['y']) ** 2) ** 0.5
            if distance < min_distance and distance < 50:  # Attack range
                min_distance = distance
                nearest_monster = monster
        
        if nearest_monster:
            message = {
                'type': 'attack_monster',
                'monster_id': nearest_monster['id']
            }
            self.send_message(message)
    
    def attack_monster_at_position(self, pos):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        player = self.players[self.my_player_id]
        if not player['alive']:
            return
        
        # Convertir la position de l'écran vers le monde
        world_x, world_y = self.screen_to_world(pos[0], pos[1])
        
        # Check if click is on a monster
        for monster in self.monsters.values():
            if not monster['alive']:
                continue
            
            # Créer un rectangle autour du monstre en coordonnées monde
            monster_rect = pygame.Rect(monster['x'] - 10, monster['y'] - 10, 20, 20)
            if monster_rect.collidepoint(world_x, world_y):
                # Check if monster is in range
                distance = ((player['x'] - monster['x']) ** 2 + (player['y'] - monster['y']) ** 2) ** 0.5
                if distance < 50:
                    message = {
                        'type': 'attack_monster',
                        'monster_id': monster['id']
                    }
                    self.send_message(message)
                break
    
    def upgrade_stat(self, stat):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        player = self.players[self.my_player_id]
        if player['skill_points'] > 0:
            message = {
                'type': 'upgrade_stat',
                'stat': stat
            }
            self.send_message(message)
    
    def use_ability(self):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        player = self.players[self.my_player_id]
        if not player['alive']:
            return
        
        player_class = player.get('player_class', 'Warrior')
        ability = None
        target_id = None
        
        if player_class == "Warrior":
            ability = "charge"
        elif player_class == "Mage":
            ability = "fireball"
            # Find nearest monster for fireball
            nearest_monster = self.get_nearest_monster()
            if nearest_monster:
                target_id = nearest_monster['id']
        elif player_class == "Archer":
            ability = "multishot"
        elif player_class == "Rogue":
            ability = "stealth"
        
        if ability:
            message = {
                'type': 'use_ability',
                'ability': ability,
                'target_id': target_id
            }
            self.send_message(message)
    
    def get_nearest_monster(self):
        if not self.my_player_id or self.my_player_id not in self.players:
            return None
        
        player = self.players[self.my_player_id]
        nearest_monster = None
        min_distance = float('inf')
        
        for monster in self.monsters.values():
            if not monster['alive']:
                continue
            
            distance = ((player['x'] - monster['x']) ** 2 + (player['y'] - monster['y']) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_monster = monster
        
        return nearest_monster
    
    def draw_name_input(self):
        # Draw background
        self.screen.fill(BLACK)
        
        if self.show_class_selection:
            self.draw_class_selection()
        else:
            # Title
            title = self.big_font.render("RPG Multijoueur", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(title, title_rect)
            
            # Input prompt
            prompt = self.font.render("Entrez votre nom:", True, WHITE)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 280))
            self.screen.blit(prompt, prompt_rect)
            
            # Input box
            input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 320, 200, 30)
            pygame.draw.rect(self.screen, WHITE, input_box, 2)
            
            # Player name text
            name_text = self.font.render(self.player_name, True, WHITE)
            self.screen.blit(name_text, (input_box.x + 5, input_box.y + 5))
            
            # Instructions
            instruction = self.font.render("Appuyez sur Entrée pour continuer", True, GRAY)
            instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 380))
            self.screen.blit(instruction, instruction_rect)
    
    def draw_class_selection(self):
        # Title
        title = self.big_font.render("Choisissez votre classe", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Name input
        name_prompt = self.font.render(f"Nom: {self.player_name}", True, WHITE)
        name_rect = name_prompt.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(name_prompt, name_rect)
        
        # Class options
        classes = [
            ("1 - Guerrier", "Warrior", "HP élevé, attaque forte, lent"),
            ("2 - Mage", "Mage", "Mana élevé, sorts puissants, fragile"),
            ("3 - Archer", "Archer", "Attaques à distance, critique élevé"),
            ("4 - Voleur", "Rogue", "Très rapide, critique très élevé")
        ]
        
        y_start = 250
        for i, (key, class_name, description) in enumerate(classes):
            y_pos = y_start + i * 60
            
            # Highlight selected class
            color = YELLOW if class_name == self.selected_class else WHITE
            
            # Class name
            class_text = self.font.render(key, True, color)
            class_rect = class_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(class_text, class_rect)
            
            # Description
            desc_text = pygame.font.Font(None, 18).render(description, True, GRAY)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 20))
            self.screen.blit(desc_text, desc_rect)
        
        # Instructions
        instruction = self.font.render("Entrez votre nom puis appuyez sur Entrée", True, GRAY)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game(self):
        # Mettre à jour la caméra
        self.update_camera()
        
        # Dessiner le fond du monde
        self.draw_world_background()
        
        # Draw monsters
        for monster in self.monsters.values():
            if monster['alive']:
                # Convertir les coordonnées monde en coordonnées écran
                screen_x, screen_y = self.world_to_screen(monster['x'], monster['y'])
                
                # Ne dessiner que si visible à l'écran
                if -20 <= screen_x <= SCREEN_WIDTH + 20 and -20 <= screen_y <= SCREEN_HEIGHT + 20:
                    # Monster body with border
                    pygame.draw.circle(self.screen, BLACK, (int(screen_x), int(screen_y)), 12)
                    pygame.draw.circle(self.screen, RED, (int(screen_x), int(screen_y)), 10)
                    
                    # HP bar
                    bar_width = 30
                    bar_height = 4
                    hp_ratio = monster['hp'] / monster['max_hp']
                    hp_bar_width = int(bar_width * hp_ratio)
                    
                    pygame.draw.rect(self.screen, RED, 
                                   (screen_x - bar_width//2, screen_y - 20, bar_width, bar_height))
                    pygame.draw.rect(self.screen, GREEN, 
                                   (screen_x - bar_width//2, screen_y - 20, hp_bar_width, bar_height))
                    
                    # Monster ID
                    monster_text = pygame.font.Font(None, 16).render(monster['id'], True, BLACK)
                    text_rect = monster_text.get_rect(center=(screen_x, screen_y + 20))
                    self.screen.blit(monster_text, text_rect)
        
        # Draw players
        for player in self.players.values():
            # Convertir les coordonnées monde en coordonnées écran
            screen_x, screen_y = self.world_to_screen(player['x'], player['y'])
            
            # Ne dessiner que si visible à l'écran
            if -20 <= screen_x <= SCREEN_WIDTH + 20 and -20 <= screen_y <= SCREEN_HEIGHT + 20:
                if player['alive']:
                    # Different colors for different classes
                    class_colors = {
                        'Warrior': RED,
                        'Mage': BLUE,
                        'Archer': GREEN,
                        'Rogue': PURPLE
                    }
                    
                    if player['id'] == self.my_player_id:
                        color = YELLOW  # Your player is always yellow
                    else:
                        color = class_colors.get(player.get('player_class', 'Warrior'), GRAY)
                    
                    pygame.draw.circle(self.screen, color, (int(screen_x), int(screen_y)), 15)
                    
                    # Player name and class
                    name_text = pygame.font.Font(None, 16).render(f"{player['name']} ({player.get('player_class', 'Warrior')})", True, BLACK)
                    name_rect = name_text.get_rect(center=(screen_x, screen_y - 35))
                    self.screen.blit(name_text, name_rect)
                    
                    # HP bar
                    bar_width = 40
                    bar_height = 6
                    hp_ratio = player['hp'] / player['max_hp']
                    hp_bar_width = int(bar_width * hp_ratio)
                    
                    pygame.draw.rect(self.screen, RED, 
                                   (screen_x - bar_width//2, screen_y + 20, bar_width, bar_height))
                    pygame.draw.rect(self.screen, GREEN, 
                                   (screen_x - bar_width//2, screen_y + 20, hp_bar_width, bar_height))
                    
                    # Mana bar
                    mana_ratio = player.get('mana', 0) / max(1, player.get('max_mana', 1))
                    mana_bar_width = int(bar_width * mana_ratio)
                    
                    pygame.draw.rect(self.screen, PURPLE, 
                                   (screen_x - bar_width//2, screen_y + 28, bar_width, bar_height))
                    pygame.draw.rect(self.screen, BLUE, 
                                   (screen_x - bar_width//2, screen_y + 28, mana_bar_width, bar_height))
                else:
                    # Dead player (gray circle)
                    pygame.draw.circle(self.screen, GRAY, (int(screen_x), int(screen_y)), 15)
        
        # Draw UI
        self.draw_ui()
        
        # Draw dropped items
        self.draw_dropped_items()
        
        # Draw minimap
        self.draw_minimap()
        
        # Debug : afficher position et zone
        if self.my_player_id and self.my_player_id in self.players:
            player = self.players[self.my_player_id]
            zone_name = self.get_current_zone(player['x'], player['y'])
            debug_text = f"Position: ({int(player['x'])}, {int(player['y'])}) - Zone: {zone_name}"
            debug_surface = pygame.font.Font(None, 24).render(debug_text, True, WHITE)
            # Placer le debug en haut au centre pour éviter les conflits
            debug_rect = debug_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
            # Fond noir pour la lisibilité
            pygame.draw.rect(self.screen, BLACK, debug_rect.inflate(20, 10))
            self.screen.blit(debug_surface, debug_rect)
        
        if self.show_inventory:
            self.draw_inventory()
            
        if self.show_stats_panel:
            self.draw_stats_panel()
        
        # Toujours afficher les barres de HP et Mana
        self.draw_health_mana_bars()
    
    def draw_health_mana_bars(self):
        """Dessine les barres de HP et Mana en bas de l'écran"""
        if not self.my_player_id or self.my_player_id not in self.players:
            return
            
        player = self.players[self.my_player_id]
        
        # Dimensions des barres
        bar_width = 200
        bar_height = 20
        bar_spacing = 10
        margin_x = 10
        margin_y = 40  # Distance du bas de l'écran
        
        # Position des barres (en bas à gauche, au-dessus du log de combat)
        hp_bar_x = margin_x
        hp_bar_y = SCREEN_HEIGHT - margin_y - bar_height * 2 - bar_spacing
        mana_bar_x = margin_x
        mana_bar_y = SCREEN_HEIGHT - margin_y - bar_height
        
        # Barre de HP
        hp_current = player.get('hp', 0)
        hp_max = player.get('max_hp', 1)
        hp_ratio = hp_current / hp_max if hp_max > 0 else 0
        
        # Fond de la barre HP (noir)
        pygame.draw.rect(self.screen, BLACK, (hp_bar_x, hp_bar_y, bar_width, bar_height))
        # Barre HP (rouge à vert selon le pourcentage)
        hp_fill_width = int(bar_width * hp_ratio)
        if hp_ratio > 0.6:
            hp_color = GREEN
        elif hp_ratio > 0.3:
            hp_color = YELLOW
        else:
            hp_color = RED
        pygame.draw.rect(self.screen, hp_color, (hp_bar_x, hp_bar_y, hp_fill_width, bar_height))
        # Bordure de la barre HP
        pygame.draw.rect(self.screen, WHITE, (hp_bar_x, hp_bar_y, bar_width, bar_height), 2)
        
        # Texte HP
        hp_text = f"HP: {hp_current}/{hp_max}"
        hp_surface = pygame.font.Font(None, 18).render(hp_text, True, WHITE)
        hp_text_rect = hp_surface.get_rect(center=(hp_bar_x + bar_width // 2, hp_bar_y + bar_height // 2))
        self.screen.blit(hp_surface, hp_text_rect)
        
        # Barre de Mana
        mana_current = player.get('mana', 0)
        mana_max = player.get('max_mana', 1)
        mana_ratio = mana_current / mana_max if mana_max > 0 else 0
        
        # Fond de la barre Mana (noir)
        pygame.draw.rect(self.screen, BLACK, (mana_bar_x, mana_bar_y, bar_width, bar_height))
        # Barre Mana (bleue)
        mana_fill_width = int(bar_width * mana_ratio)
        pygame.draw.rect(self.screen, BLUE, (mana_bar_x, mana_bar_y, mana_fill_width, bar_height))
        # Bordure de la barre Mana
        pygame.draw.rect(self.screen, WHITE, (mana_bar_x, mana_bar_y, bar_width, bar_height), 2)
        
        # Texte Mana
        mana_text = f"Mana: {mana_current}/{mana_max}"
        mana_surface = pygame.font.Font(None, 18).render(mana_text, True, WHITE)
        mana_text_rect = mana_surface.get_rect(center=(mana_bar_x + bar_width // 2, mana_bar_y + bar_height // 2))
        self.screen.blit(mana_surface, mana_text_rect)
    
    def draw_ui(self):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        player = self.players[self.my_player_id]
        
        # Combat log (bottom-left, au-dessus des barres HP/Mana) - seulement si activés
        if self.show_combat_log and self.combat_log:
            y_offset = SCREEN_HEIGHT - 200  # Plus haut pour laisser place aux barres
            log_title = self.font.render("Combat:", True, WHITE)
            self.screen.blit(log_title, (10, y_offset))
            y_offset += 25
            
            for log_entry in self.combat_log:
                text = pygame.font.Font(None, 18).render(log_entry, True, YELLOW)
                self.screen.blit(text, (10, y_offset))
                y_offset += 20
        
        # Controls (top-right) - seulement si activés
        if self.show_controls:
            controls = [
                "CONTRÔLES:",
                "WASD/Flèches: Bouger",
                "Espace: Attaquer le plus proche",
                "Q: Capacité spéciale",
                "Clic: Attaquer monstre/ramasser objet",
                "Tab: Ouvrir panneau stats",
                "I: Ouvrir inventaire",
                "H: Afficher/masquer aide",
                "L: Afficher/masquer logs",
                "",
                f"Classe: {player.get('player_class', 'Warrior')}"
            ]
            
            y_offset = 10
            for control in controls:
                text = pygame.font.Font(None, 18).render(control, True, WHITE)
                text_rect = text.get_rect()
                text_rect.topright = (SCREEN_WIDTH - 10, y_offset)
                self.screen.blit(text, text_rect)
                y_offset += 20
        else:
            # Afficher juste un petit indicateur pour savoir comment afficher les contrôles
            help_hint = pygame.font.Font(None, 16).render("Appuyez sur 'H' pour l'aide", True, GRAY)
            help_rect = help_hint.get_rect()
            help_rect.topright = (SCREEN_WIDTH - 10, 10)
            self.screen.blit(help_hint, help_rect)
    
    def draw_stats_panel(self):
        if not self.my_player_id or self.my_player_id not in self.players:
            return
        
        player = self.players[self.my_player_id]
        
        # Panel background
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 200)
        pygame.draw.rect(self.screen, BLACK, panel_rect)
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
        
        # Title
        title = self.font.render("Améliorer les statistiques", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title, title_rect)
        
        # Available points
        points_text = self.font.render(f"Points disponibles: {player['skill_points']}", True, YELLOW)
        points_rect = points_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(points_text, points_rect)
        
        # Upgrade options
        upgrades = [
            ("1 - Attaque (+2)", "attack"),
            ("2 - Défense (+2)", "defense"),
            ("3 - Vitesse (+1)", "speed"),
            ("4 - HP Max (+15)", "hp"),
            ("5 - Mana Max (+10)", "mana"),
            ("6 - Critique (+5%)", "critical")
        ]
        
        y_offset = SCREEN_HEIGHT // 2 - 50
        for upgrade_text, _ in upgrades:
            color = WHITE if player['skill_points'] > 0 else GRAY
            text = pygame.font.Font(None, 20).render(upgrade_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
        
        # Instructions
        instruction = pygame.font.Font(None, 18).render("Appuyez sur Tab pour fermer", True, GRAY)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(instruction, instruction_rect)
    
    def run(self):
        # Try to connect to server
        if not self.connect_to_server():
            print("Impossible de se connecter au serveur")
            return
        
        while self.running:
            self.handle_input()
            
            if self.input_active:
                self.draw_name_input()
            else:
                self.update_player_movement()
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Cleanup
        if self.socket:
            self.socket.close()
        pygame.quit()
        sys.exit()
    
    def try_pickup_item(self, mouse_pos):
        """Tente de ramasser un objet si on clique dessus"""
        # Convertir la position de l'écran vers le monde
        world_x, world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])
        
        for drop_id, item_data in self.dropped_items.items():
            item_x, item_y = item_data['x'], item_data['y']
            # Vérifier si on clique près de l'objet (tolérance de 20 pixels en coordonnées monde)
            if abs(world_x - item_x) < 20 and abs(world_y - item_y) < 20:
                # Vérifier si notre joueur est assez proche
                if self.my_player_id in self.players:
                    player = self.players[self.my_player_id]
                    distance = ((player['x'] - item_x) ** 2 + (player['y'] - item_y) ** 2) ** 0.5
                    if distance <= 50:  # Portée de ramassage
                        self.send_message({
                            'type': 'pickup_item',
                            'item_drop_id': drop_id
                        })
                        return True
        return False
    
    def handle_inventory_click(self, mouse_pos):
        """Gère les clics dans l'interface d'inventaire"""
        if not self.show_inventory or self.my_player_id not in self.players:
            return False
            
        player = self.players[self.my_player_id]
        mouse_x, mouse_y = mouse_pos
        
        # Nouvelle zone de l'inventaire (agrandie)
        inv_x, inv_y = 50, 50
        inv_width, inv_height = 400, 500
        
        # Vérifier si le clic est dans la zone d'inventaire
        if not (inv_x <= mouse_x <= inv_x + inv_width and inv_y <= mouse_y <= inv_y + inv_height):
            return False
        
        # Calculer les positions correspondant à la nouvelle interface
        stats_y = inv_y + 35
        stats_info_count = 5  # Nombre de lignes de stats
        
        # Zone des objets équipés
        equipped = player.get('equipped', {})
        eq_y = stats_y + 20 + (stats_info_count * 18) + 15  # Position "--- Équipement ---"
        y_offset = eq_y + 20  # Position du premier objet équipé
        
        for slot, item_data in equipped.items():
            if y_offset <= mouse_y <= y_offset + 20:
                # Clic sur un objet équipé - le déséquiper
                self.send_message({
                    'type': 'unequip_item',
                    'slot': slot
                })
                return True
            y_offset += 20
        
        # Zone de l'inventaire
        inventory = player.get('inventory', {})
        inv_start_y = y_offset + 15  # Position "--- Inventaire ---"
        y_offset = inv_start_y + 25  # Position du premier objet d'inventaire
        
        for item_id, item_data in inventory.items():
            if y_offset <= mouse_y <= y_offset + 20:
                # Clic sur un objet de l'inventaire
                item_type = item_data.get('type', '')
                
                if item_type == 'consumable':
                    # Utiliser l'objet consommable
                    self.send_message({
                        'type': 'use_item',
                        'item_id': item_id
                    })
                elif item_type in ['weapon', 'armor', 'accessory']:
                    # Équiper l'objet
                    self.send_message({
                        'type': 'equip_item',
                        'item_id': item_id
                    })
                return True
            y_offset += 20
        
        return False
    
    def draw_inventory(self):
        """Dessine l'interface d'inventaire"""
        if not self.show_inventory or self.my_player_id not in self.players:
            return
            
        player = self.players[self.my_player_id]
        
        # Agrandir l'inventaire pour inclure les stats
        inv_x, inv_y = 50, 50
        inv_width, inv_height = 400, 500
        pygame.draw.rect(self.screen, (50, 50, 50), (inv_x, inv_y, inv_width, inv_height))
        pygame.draw.rect(self.screen, WHITE, (inv_x, inv_y, inv_width, inv_height), 2)
        
        # Titre
        title_text = self.font.render("Inventaire & Stats", True, WHITE)
        self.screen.blit(title_text, (inv_x + 10, inv_y + 10))
        
        # Or
        gold_text = self.font.render(f"Or: {player.get('gold', 0)}", True, YELLOW)
        self.screen.blit(gold_text, (inv_x + 250, inv_y + 10))
        
        # Section Stats du joueur
        stats_y = inv_y + 35
        stats_text = self.font.render("--- Stats ---", True, CYAN)
        self.screen.blit(stats_text, (inv_x + 10, stats_y))
        
        # Afficher les stats principales
        stats_info = [
            f"Niveau: {player.get('level', 1)} | XP: {player.get('xp', 0)}/{player.get('xp_to_next', 100)}",
            f"HP: {player.get('hp', 100)}/{player.get('max_hp', 100)} | Mana: {player.get('mana', 50)}/{player.get('max_mana', 50)}",
            f"Attaque: {player.get('attack', 10)} | Défense: {player.get('defense', 5)}",
            f"Vitesse: {player.get('speed', 5)} | Critique: {int(player.get('critical_chance', 0.1) * 100)}%",
            f"Points de compétence: {player.get('skill_points', 0)}"
        ]
        
        stats_y += 20
        for i, stat_line in enumerate(stats_info):
            stat_text = pygame.font.Font(None, 20).render(stat_line, True, WHITE)
            self.screen.blit(stat_text, (inv_x + 10, stats_y + i * 18))
        
        # Équipement
        eq_y = stats_y + len(stats_info) * 18 + 15
        eq_text = self.font.render("--- Équipement ---", True, CYAN)
        self.screen.blit(eq_text, (inv_x + 10, eq_y))
        
        equipped = player.get('equipped', {})
        y_offset = eq_y + 20
        for slot, item_data in equipped.items():
            color = RARITY_COLORS.get(item_data.get('rarity', 'common'), WHITE)
            item_text = self.font.render(f"{slot}: {item_data['name']} [CLIC: déséquiper]", True, color)
            self.screen.blit(item_text, (inv_x + 10, y_offset))
            y_offset += 20
        
        # Inventaire
        inv_start_y = y_offset + 15
        inv_text = self.font.render("--- Inventaire ---", True, CYAN)
        self.screen.blit(inv_text, (inv_x + 10, inv_start_y))
        
        inventory = player.get('inventory', {})
        y_offset = inv_start_y + 25
        for item_id, item_data in inventory.items():
            color = RARITY_COLORS.get(item_data.get('rarity', 'common'), WHITE)
            item_type = item_data.get('type', '')
            
            # Ajouter une indication de l'action possible
            if item_type == 'consumable':
                action_text = " [CLIC: utiliser]"
            elif item_type in ['weapon', 'armor', 'accessory']:
                action_text = " [CLIC: équiper]"
            else:
                action_text = ""
            
            # Afficher la quantité et la limite de stack
            quantity = item_data.get('quantity', 1)
            max_stack = item_data.get('max_stack', 1)
            
            if max_stack > 1:
                quantity_text = f" ({quantity}/{max_stack})"
            else:
                quantity_text = ""
            
            item_text = self.font.render(f"- {item_data['name']}{quantity_text}{action_text}", True, color)
            self.screen.blit(item_text, (inv_x + 10, y_offset))
            y_offset += 20
        
        # Instructions
        help_y = inv_y + inv_height - 85
        help_texts = [
            "Clic gauche sur objet au sol pour ramasser",
            "Clic gauche sur objet d'inventaire pour équiper/utiliser",
            "Clic gauche sur objet équipé pour déséquiper",
            "I pour ouvrir/fermer l'inventaire",
            "C pour ouvrir/fermer le chat"
        ]
        for i, text in enumerate(help_texts):
            help_text = pygame.font.Font(None, 16).render(text, True, GRAY)
            self.screen.blit(help_text, (inv_x + 10, help_y + i * 16))
    
    def draw_dropped_items(self):
        """Dessine les objets au sol"""
        for drop_id, item_data in self.dropped_items.items():
            world_x, world_y = item_data['x'], item_data['y']
            screen_x, screen_y = self.world_to_screen(world_x, world_y)
            
            # Ne dessiner que si visible à l'écran
            if -10 <= screen_x <= SCREEN_WIDTH + 10 and -10 <= screen_y <= SCREEN_HEIGHT + 10:
                rarity = item_data.get('item_rarity', 'common')
                color = RARITY_COLORS.get(rarity, WHITE)
                
                # Dessiner un petit carré pour l'objet
                pygame.draw.rect(self.screen, color, (screen_x-5, screen_y-5, 10, 10))
                pygame.draw.rect(self.screen, BLACK, (screen_x-5, screen_y-5, 10, 10), 1)
                
                # Nom de l'objet au survol (approximatif)
                mouse_pos = pygame.mouse.get_pos()
                if abs(mouse_pos[0] - screen_x) < 20 and abs(mouse_pos[1] - screen_y) < 20:
                    name_text = pygame.font.Font(None, 18).render(item_data.get('item_name', 'Item'), True, color)
                    self.screen.blit(name_text, (screen_x + 10, screen_y - 10))

if __name__ == "__main__":
    # Get server IP from command line argument or use localhost
    server_ip = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    
    client = GameClient()
    client.run()
