# 3n-mac
Near Network MAC Protocol for Wireless Sensor Network

## Installation
1. Clone the repository
2. Create a new python env called *3n-mac*: `python -m venv ~/.virtualenvs/3n-mac`
3. Use the new python env : `source ~/.virtualenvs/3n-mac/bin/activate` if you use fish `source ~/.virtualenvs/3n-mac/bin/activate.fish`
4. Install the dependencies : `pip install -r requirements.txt`





### **1. Quand on ajoute un nouveau nœud :**

1. **Activation** :
   - Le nouveau nœud s’allume et commence en mode **FD (Fast Discovery)**.
   - Il envoie des *beacons* toutes les 1 seconde pour signaler sa présence.

2. **Recherche de voisins** :
   - Les nœuds voisins déjà dans le réseau répondent avec un *beacon de bienvenue* contenant :
     - Leur adresse.
     - La force du signal (RSSI).
     - Les informations réseau nécessaires pour rejoindre le maillage (ex. clé de sécurité ou ID réseau).

3. **Sélection du meilleur voisin** :
   - Le nouveau nœud choisit le voisin avec le **meilleur RSSI** pour établir une connexion initiale.
   - Il envoie un message de **connexion** au voisin choisi.

4. **Validation de la connexion** :
   - Le voisin vérifie que le nouveau nœud est autorisé (authentification avec une clé partagée).
   - Si tout est correct, le voisin ajoute le nouveau nœud à sa table de routage et transmet l’information au reste du réseau.

5. **Passage en mode SD** :
   - Une fois connecté et stabilisé, le nouveau nœud passe en mode **SD (Slow Discovery)** pour économiser de l’énergie.

---

### **2. Organisation du réseau après ajout d’un nœud :**

1. **Mise à jour des routes** :
   - Tous les nœuds voisins mettent à jour leurs tables de routage pour inclure le nouveau nœud.
   - Les routes sont recalculées dynamiquement en fonction du **RSSI** et de la charge énergétique des nœuds.

2. **Propagation de l’information** :
   - Le réseau entier est informé qu’un nouveau nœud a été ajouté grâce à un mécanisme de diffusion contrôlée (éviter la surcharge).

3. **Stabilisation** :
   - Une fois les routes recalculées, le réseau fonctionne normalement, avec le nouveau nœud pleinement intégré.

---

### **3. Envoyer un message d’un nœud A à un nœud B :**

1. **Détermination de la route** :
   - Le nœud A consulte sa **table de routage** pour trouver le meilleur chemin vers B.
   - Si B est un voisin direct, le message est envoyé directement.
   - Sinon, le message est envoyé au **prochain nœud sur le chemin** (déterminé par le RSSI et les priorités).

2. **Transmission du message** :
   - Le message est transmis de nœud en nœud jusqu’à atteindre le nœud B.
   - Chaque nœud intermédiaire :
     - Consulte sa propre table de routage.
     - Transmet le message au prochain nœud avec le **meilleur RSSI** vers la destination.

3. **Accusé de réception** :
   - Une fois que le message atteint B, un **accusé de réception** est envoyé à A en suivant le chemin inverse.
   - Si l’accusé de réception n’est pas reçu après un certain délai, A retransmet le message en essayant un autre chemin.

---

### **4. Que se passe-t-il si un nœud disparaît ou échoue ?**

1. **Détection de la panne** :
   - Les nœuds voisins du nœud défaillant détectent l’absence de ses *beacons SD* après 3 cycles consécutifs.

2. **Mise à jour du réseau** :
   - Les voisins suppriment le nœud défaillant de leur table de routage.
   - Une **reconfiguration dynamique** des routes est effectuée.

3. **Redondance** :
   - Les messages en transit sont automatiquement redirigés via d’autres chemins si disponibles.

---

### **5. Optimisation énergétique et communication efficace :**

1. **Mode veille** :
   - Les nœuds qui n’envoient ni ne reçoivent de messages passent en **mode veille** pour économiser leur batterie.
   - Ils se réveillent uniquement pour écouter les *beacons SD* ou envoyer/recevoir des données.

2. **Réduction des collisions** :
   - Le protocole utilise **CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)** :
     - Chaque nœud vérifie si le canal est libre avant d’envoyer un message.
     - Si une collision est détectée, l’envoi est réessayé après un délai aléatoire.

---

### **Résumé des étapes principales :**

- **Ajouter un nœud** : Le nouveau nœud découvre ses voisins, se connecte au meilleur voisin, et est intégré au réseau.
- **Envoyer un message** : Les messages passent par le chemin avec le meilleur RSSI, chaque nœud jouant le rôle de relais si nécessaire.
- **Gérer les pannes** : Si un nœud disparaît, les routes sont recalculées automatiquement pour maintenir la connectivité.
- **Optimiser l’énergie** : Les nœuds utilisent des modes veille et des cycles de transmission optimisés pour réduire leur consommation.

Avec cette organisation, le réseau est **flexible, robuste, et efficace énergétiquement**, tout en restant simple à comprendre et à mettre en œuvre.