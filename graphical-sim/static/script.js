const canvas = document.getElementById("networkCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let nodes = [];
let links = [];
let selectedNode = null;

function logToConsole(message) {
    const consoleLog = document.getElementById("consoleLog");
    const logEntry = document.createElement("div");
    logEntry.textContent = message;
    consoleLog.appendChild(logEntry);
    consoleLog.scrollTop = consoleLog.scrollHeight;
}

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
            logToConsole(`Node added: ${JSON.stringify(node)}`);
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
                logToConsole(`Node selected: ${JSON.stringify(info)}`);
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
            logToConsole("Network discovered");
        });
});

document.getElementById("cleanWorkspace").addEventListener("click", () => {
    fetch("/clean_workspace", { method: "POST" })
        .then((response) => response.json())
        .then(() => {
            nodes = [];
            links = [];
            drawNetwork();
            logToConsole("Workspace cleaned");
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
        ctx.strokeStyle = link.type === "interregion" ? "red" : "gray"; // Lien interrégion en rouge
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