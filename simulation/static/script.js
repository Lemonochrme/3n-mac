const canvas = document.getElementById("networkCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let nodes = [];
let links = [];
let selectedNode = null;

// Ajout d'un nœud
canvas.addEventListener("click", (event) => {
    if (event.shiftKey) return; // Empêcher l'ajout si Shift est appuyé

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    fetch("/add_node", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ x, y }),
    })
        .then((response) => response.json())
        .then((node) => {
            nodes.push(node);
            drawNetwork();
        });
});

// Sélection d'un nœud avec Shift + clic
canvas.addEventListener("click", (event) => {
    if (!event.shiftKey) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    selectedNode = nodes.find(
        (node) => Math.hypot(node.x - x, node.y - y) < 10
    );

    drawNetwork();

    if (selectedNode) {
        drawNodeRegion(selectedNode);
        fetch(`/node_info/${selectedNode.id}`)
            .then((response) => response.json())
            .then((info) => {
                const infoPanel = document.getElementById("infoPanel");
                infoPanel.textContent = `Node ID: ${info.id}, Info: ${info.info}`;
            });
    }
});

// Supprimer un nœud sélectionné
document.addEventListener("keydown", (event) => {
    if (event.key === "Delete" && selectedNode) {
        fetch(`/delete_node`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ node_id: selectedNode.id }),
        }).then(() => {
            nodes = nodes.filter((node) => node.id !== selectedNode.id);
            links = links.filter(
                (link) =>
                    link.source !== selectedNode.id &&
                    link.target !== selectedNode.id
            );
            selectedNode = null;
            drawNetwork();
        });
    }
});

// Découverte du réseau
document.getElementById("discoverNetwork").addEventListener("click", () => {
    fetch("/discover_network", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
            nodes = data.nodes;
            links = data.links;
            drawNetwork();
        });
});

// Dessin de la région d'un nœud
function drawNodeRegion(node) {
    ctx.beginPath();
    ctx.arc(node.x, node.y, 200, 0, Math.PI * 2);
    ctx.strokeStyle = "lightgray";
    ctx.setLineDash([5, 5]);
    ctx.stroke();
    ctx.setLineDash([]); // Réinitialiser les lignes pointillées
}

// Dessin du réseau
function drawNetwork() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dessiner les liens
    links.forEach((link) => {
        const source = nodes[link.source];
        const target = nodes[link.target];
        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);
        ctx.strokeStyle = "gray";
        ctx.stroke();
    });

    // Dessiner les nœuds
    nodes.forEach((node) => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.fill();
    });

    // Dessiner la sélection
    if (selectedNode) {
        drawNodeRegion(selectedNode);
    }
}
