const canvas = document.getElementById("networkCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let nodes = [];
let links = [];

// Add node on click
canvas.addEventListener("click", (event) => {
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

// Discover network button
document.getElementById("discoverNetwork").addEventListener("click", () => {
    fetch("/discover_network", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
            nodes = data.nodes;
            links = data.links;
            drawNetwork();
        });
});

// Show node info on hover
canvas.addEventListener("mousemove", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const hoveredNode = nodes.find(
        (node) => Math.hypot(node.x - x, node.y - y) < 10
    );

    const infoPanel = document.getElementById("infoPanel");
    if (hoveredNode) {
        fetch(`/node_info/${hoveredNode.id}`)
            .then((response) => response.json())
            .then((info) => {
                infoPanel.textContent = `Node ID: ${info.id}, Info: ${info.info}`;
            });
    } else {
        infoPanel.textContent = "Click on a node to see its information";
    }
});

// Draw nodes and links
function drawNetwork() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw links
    links.forEach((link) => {
        const source = nodes[link.source];
        const target = nodes[link.target];
        ctx.beginPath();
        ctx.moveTo(source.x, source.y);
        ctx.lineTo(target.x, target.y);
        ctx.strokeStyle = "gray";
        ctx.stroke();
    });

    // Draw nodes
    nodes.forEach((node) => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.fill();
    });
}
