# Guide de Dépannage Multijoueur

## Problèmes Courants et Solutions

### 🔧 Le jeu se bloque avec plusieurs joueurs

**Problème résolu !** Les versions antérieures avaient des problèmes de concurrence.

✅ **Solution appliquée :**
- Meilleure gestion des buffers réseau
- Synchronisation avec des locks
- Gestion d'erreurs améliorée
- Messages délimités par des newlines

### 🌐 Problèmes de Connexion

#### Erreur "Connection refused"
```
❌ Impossible de se connecter au serveur
```

**Solutions :**
1. Vérifiez que le serveur est démarré :
   ```bash
   python server.py
   ```
2. Vérifiez l'adresse IP et le port
3. Testez avec le script de test :
   ```bash
   python test_server.py
   ```

#### Erreur "Connection reset"
```
❌ [WinError 10053] Une connexion établie a été abandonnée
```

**Normal !** Cela arrive quand un client se déconnecte. Le serveur gère automatiquement cette situation.

### 🐌 Lag ou Saccades

#### Trop de monstres
Réduisez le nombre dans `server.py` :
```python
# Dans spawn_monsters()
for i in range(3):  # Au lieu de 5
```

#### Fréquence d'envoi trop élevée
Modifiez dans `server.py` :
```python
time.sleep(1/20)  # 20 FPS au lieu de 30
```

#### Trop de logs de combat
Réduisez dans `client.py` :
```python
if len(self.combat_log) > 3:  # Au lieu de 5
```

### 💾 Problèmes de Mémoire

#### Le serveur consomme trop de RAM
- Redémarrez le serveur périodiquement
- Limitez le nombre de clients simultanés
- Réduisez la fréquence des mises à jour

### 🔐 Problèmes de Pare-feu

#### Connexion bloquée
**Windows :**
1. Ouvrir "Pare-feu Windows Defender"
2. Cliquer "Autoriser une application"
3. Ajouter Python.exe
4. Cocher "Public" et "Privé"

**Routeur (pour jouer via Internet) :**
1. Port forwarding du port 12345
2. Diriger vers l'IP de l'ordinateur serveur

### 🧪 Tests de Diagnostic

#### Test de connexion simple
```bash
python test_server.py
```

#### Test multijoueur
```bash
python test_multiplayer.py
```

#### Test de performance
Surveillez les logs du serveur pour détecter les erreurs.

### 📊 Monitoring et Débogage

#### Logs du serveur
Le serveur affiche :
- Nouvelles connexions
- Déconnexions de joueurs
- Erreurs de traitement

#### Logs du client
Le client affiche :
- Erreurs de connexion
- Erreurs d'envoi/réception
- Problèmes de traitement des messages

### ⚙️ Configuration Avancée

#### Modifier le port du serveur
Dans `server.py` :
```python
server = GameServer(host='0.0.0.0', port=8080)
```

Dans `client.py` :
```bash
python client.py <IP_SERVEUR> 8080
```

#### Autoriser les connexions externes
Dans `server.py` :
```python
server = GameServer(host='0.0.0.0', port=12345)  # Au lieu de 'localhost'
```

#### Augmenter les timeouts
Dans `server.py` :
```python
client_socket.settimeout(60.0)  # 60 secondes au lieu de 30
```

### 🆘 Problèmes Persistants

Si vous rencontrez toujours des problèmes :

1. **Redémarrez complètement** :
   ```bash
   # Arrêter tous les processus Python
   taskkill /f /im python.exe  # Windows
   killall python  # Linux/Mac
   
   # Redémarrer le serveur
   python server.py
   ```

2. **Vérifiez la version Python** :
   ```bash
   python --version  # Doit être 3.7+
   ```

3. **Réinstallez Pygame** :
   ```bash
   pip uninstall pygame
   pip install pygame
   ```

4. **Testez sur localhost d'abord** avant d'essayer en réseau

### 📈 Optimisations Recommandées

Pour de meilleures performances :

1. **Réduisez la fréquence d'envoi** (20 FPS au lieu de 30)
2. **Limitez les joueurs simultanés** (4-6 maximum recommandé)
3. **Utilisez un SSD** pour de meilleures performances I/O
4. **Fermez les applications inutiles** sur la machine serveur

### 🎯 Conseils pour Jouer en LAN

1. **Un seul serveur** : Une personne lance le serveur
2. **Partagez l'IP** : Utilisez `ipconfig` (Windows) ou `ifconfig` (Linux/Mac)
3. **Même réseau** : Assurez-vous que tous sont sur le même Wi-Fi/réseau
4. **Test de ping** : `ping <IP_SERVEUR>` pour vérifier la connectivité

Le jeu est maintenant stable pour le multijoueur ! 🎮
