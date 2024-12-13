import math

class Protocol:
    MAX_DISTANCE = 200  # Distance maximale pour établir une connexion

    def __init__(self):
        self.nodes = []  # Liste des nœuds
        self.links = []  # Liste des liens (arcs) entre les nœuds

    def add_node(self, x, y):
        """Ajoute un nœud au réseau."""
        node_id = len(self.nodes)
        node = {
            "id": node_id,
            "x": x,
            "y": y,
            "color": "gray",  # Couleur initiale (nœud non connecté)
            "info": f"Node {node_id}",
        }
        self.nodes.append(node)
        return node

    def delete_node(self, node_id):
        """Supprime un nœud du réseau et met à jour les connexions."""
        if 0 <= node_id < len(self.nodes):
            self.nodes.pop(node_id)
            # Supprimer les liens associés
            self.links = [
                link
                for link in self.links
                if link["source"] != node_id and link["target"] != node_id
            ]
            # Réassigner les IDs des nœuds restants
            for idx, node in enumerate(self.nodes):
                node["id"] = idx
            # Réassigner les IDs des liens
            for link in self.links:
                link["source"] = self._adjust_id(link["source"], node_id)
                link["target"] = self._adjust_id(link["target"], node_id)

    def _adjust_id(self, link_id, removed_id):
        """Réduit l'ID du lien si un nœud précédent a été supprimé."""
        return link_id - 1 if link_id > removed_id else link_id

    def discover_network(self):
        """Établit les connexions entre les nœuds (découverte du réseau)."""
        self.links = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                # Calculer la distance entre deux nœuds
                distance = math.sqrt(
                    (self.nodes[i]["x"] - self.nodes[j]["x"]) ** 2 +
                    (self.nodes[i]["y"] - self.nodes[j]["y"]) ** 2
                )
                # Ajouter un lien uniquement si la distance est inférieure au maximum
                if distance <= self.MAX_DISTANCE:
                    self.links.append({"source": i, "target": j})
        # Marquer tous les nœuds comme connectés
        for node in self.nodes:
            node["color"] = "white"

    def get_node_info(self, node_id):
        """Retourne les informations d'un nœud spécifique."""
        if 0 <= node_id < len(self.nodes):
            return self.nodes[node_id]
        else:
            return {"error": "Node not found"}
