from flask import Flask, jsonify, render_template, request
from protocol import Protocol

app = Flask(__name__)

# Initialisation du protocole
protocol = Protocol()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_node", methods=["POST"])
def add_node():
    data = request.json
    node = protocol.add_node(data["x"], data["y"])
    return jsonify(node)

@app.route("/discover_network", methods=["POST"])
def discover_network():
    protocol.discover_network()
    return jsonify({"nodes": protocol.nodes, "links": protocol.links})

@app.route("/node_info/<int:node_id>")
def node_info(node_id):
    return jsonify(protocol.get_node_info(node_id))

if __name__ == "__main__":
    app.run(debug=True)
