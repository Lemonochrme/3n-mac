import math
import heapq


class Protocol:
    MAX_DISTANCE = 200  # Distance maximale pour établir une connexion

    def __init__(self):
        self.nodes = []  # Liste des nœuds
        self.links = []  # Liste des liens entre les nœuds

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
            self.links = [
                link
                for link in self.links
                if link["source"] != node_id and link["target"] != node_id
            ]
            for idx, node in enumerate(self.nodes):
                node["id"] = idx
            for link in self.links:
                link["source"] = self._adjust_id(link["source"], node_id)
                link["target"] = self._adjust_id(link["target"], node_id)

    def _adjust_id(self, link_id, removed_id):
        return link_id - 1 if link_id > removed_id else link_id

    def distance(self, node1, node2):
        """Calcule la distance entre deux nœuds."""
        return math.sqrt((node1["x"] - node2["x"]) ** 2 + (node1["y"] - node2["y"]) ** 2)

    def discover_network(self):
        """Établit les connexions entre les nœuds (découverte du réseau)."""
        self.links = []
        node_count = len(self.nodes)

        # Connexions intra-région
        for i in range(node_count):
            for j in range(i + 1, node_count):
                distance = self.distance(self.nodes[i], self.nodes[j])
                if distance <= self.MAX_DISTANCE:
                    self.links.append({"source": i, "target": j})

        # Détection et ajout des passerelles interrégion
        self.add_interregion_links()

        for node in self.nodes:
            node["color"] = "white"

    def add_interregion_links(self):
        """Ajoute les connexions entre les régions via des nœuds passerelles."""
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                distance = self.distance(self.nodes[i], self.nodes[j])
                if distance > self.MAX_DISTANCE:
                    # Identifier des passerelles proches pour connecter les régions
                    self.find_shortest_bridge(i, j)

    def find_shortest_bridge(self, node_a_id, node_b_id):
        """Trouve le chemin le plus court entre deux nœuds de régions différentes."""
        # Construire un graphe pondéré (distances entre les nœuds intra-région)
        graph = {node["id"]: [] for node in self.nodes}
        for link in self.links:
            source, target = link["source"], link["target"]
            distance = self.distance(self.nodes[source], self.nodes[target])
            graph[source].append((distance, target))
            graph[target].append((distance, source))

        # Trouver le chemin le plus court avec Dijkstra
        path, cost = self.dijkstra(graph, node_a_id, node_b_id)
        if path:
            # Ajouter des liens pour ce chemin
            for i in range(len(path) - 1):
                self.links.append({"source": path[i], "target": path[i + 1]})

    def dijkstra(self, graph, start, goal):
        """Implémente Dijkstra pour trouver le chemin le plus court."""
        queue = [(0, start, [])]  # (coût actuel, nœud actuel, chemin)
        visited = set()

        while queue:
            cost, node, path = heapq.heappop(queue)
            if node in visited:
                continue
            visited.add(node)

            path = path + [node]
            if node == goal:
                return path, cost

            for distance, neighbor in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + distance, neighbor, path))

        return None, float("inf")
