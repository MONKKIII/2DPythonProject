# 🏰 Guide du Système de Donjons

## Nouveautés Ajoutées

### 🎮 Fonctionnalités Client
- **Portails de donjons** : Affichage visuel des portails sur la carte du monde
- **Interface de donjons** : Informations sur le donjon actuel en haut à droite
- **Notifications spéciales** : Messages pour les actions de donjons (entrée, sortie, boss)
- **Log des capacités de boss** : Suivi des attaques spéciales des boss en bas à droite
- **Liste des donjons** : Interface pour voir tous les donjons disponibles

### 🎯 Contrôles Ajoutés
- **E** : Entrer dans un donjon (quand vous êtes près d'un portail)
- **R** : Quitter le donjon actuel
- **P** : Afficher/masquer la liste des donjons disponibles

### 🏰 Donjons Disponibles

#### 1. Caverne des Gobelins
- **Niveau requis** : 3+
- **Position** : Centre du monde (1600, 1200)
- **Joueurs max** : 4
- **Boss** : Roi des Gobelins
- **Capacités** : Rage, Invocation de serviteurs

#### 2. Temple des Ombres  
- **Niveau requis** : 7+
- **Position** : Zone forêt (800, 400)
- **Joueurs max** : 3
- **Boss** : Seigneur des Ombres
- **Capacités** : Frappe d'ombre, Invisibilité

#### 3. Antre du Dragon
- **Niveau requis** : 12+
- **Position** : Zone volcan (2400, 1600)
- **Joueurs max** : 5
- **Boss** : Dragon Ancien
- **Capacités** : Souffle de feu, Attaque d'ailes, Guérison

### 🎁 Récompenses

#### Objets Légendaires (Drops de Boss)
- **Épée Tueuse de Dragons** : +15 ATK, +25% Crit
- **Bâton d'Archimage** : +12 ATK, +50 Mana Max
- **Lame d'Ombre** : +10 ATK, +40% Crit, +5 Vitesse
- **Armure de Titan** : +12 DEF, +100 HP Max
- **Couronne des Rois** : +5 ATK/DEF, +50 HP, +30 Mana

#### Bonus de Complétion
- **100 XP bonus** pour tous les participants
- **50 pièces d'or** pour tous les participants

### 🚀 Comment Tester

1. **Démarrer le serveur** :
   ```
   python server.py
   ```

2. **Lancer le client** :
   ```
   python client.py
   ```

3. **Créer un personnage** :
   - Choisissez une classe
   - Entrez un nom
   - Votre personnage spawn au centre du monde

4. **Monter en niveau** :
   - Tuez des monstres pour atteindre niveau 3+
   - Utilisez Q pour les capacités spéciales
   - Équipez des objets pour améliorer vos stats

5. **Explorer les donjons** :
   - Utilisez P pour voir la liste des donjons
   - Dirigez-vous vers un portail (cercles colorés sur la carte)
   - Appuyez sur E quand vous êtes proche pour entrer
   - Le boss apparaît quand 2+ joueurs sont présents

### 🔧 Interface Utilisateur

#### Indicateurs Visuels
- **Portails** : Grands cercles colorés avec niveau requis
- **Couleurs** :
  - Vert : Caverne des Gobelins
  - Violet : Temple des Ombres  
  - Rouge : Antre du Dragon
  - Gris : Niveau insuffisant

#### Informations Affichées
- **Donjon actuel** : Nom, nombre de joueurs (haut droite)
- **Notifications** : Messages d'actions (côté droit)
- **Capacités boss** : Log des attaques spéciales (bas droite)
- **Contrôles étendus** : Incluent les touches de donjons (H pour aide)

### 🎯 Conseils de Jeu

1. **Préparation** :
   - Montez au niveau requis avant d'entrer
   - Équipez-vous correctement
   - Stockez des potions de soin

2. **Stratégie de groupe** :
   - Les boss n'apparaissent qu'avec 2+ joueurs
   - Coordonnez vos attaques
   - Surveillez les capacités spéciales du boss

3. **Récompenses** :
   - Les objets légendaires ont 80% de chance de drop
   - Seuls les boss droppent des légendaires
   - Les bonus XP/or sont automatiques

### 🐛 Debug et Monitoring

- Position actuelle affichée en haut de l'écran
- Logs de combat raccourcis avec emojis
- Messages d'erreur pour les tentatives d'entrée invalides
- Nettoyage automatique des instances après 2 minutes

---

**Le système de donjons est maintenant opérationnel !** 🎉

Testez les différents donjons, combattez les boss, et récupérez des objets légendaires !
