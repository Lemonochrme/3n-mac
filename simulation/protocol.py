class Protocol:
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

    def discover_network(self):
        """Établit les connexions entre les nœuds (découverte du réseau)."""
        self.links = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                # Simuler une connexion entre chaque paire de nœuds
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
