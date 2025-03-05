from flask import Flask, request, jsonify
import ollama
import faiss
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create FAISS index for shipment search
dimension = 512
index = faiss.IndexFlatL2(dimension)

# Sample shipment database (with vectors)
shipments = {
    "12345": "Order 12345: Delivered on 25th Feb",
    "67890": "Order 67890: Out for delivery",
    "11223": "Order 11223: Dispatched, expected in 3 days",
}

# Convert text into random vectors (Replace this with real embeddings)
vectors = np.random.rand(len(shipments), dimension).astype("float32")
index.add(vectors)

shipment_ids = list(shipments.keys())

# 🔹 Function to search shipment details
def search_shipment(query_vector):
    _, indices = index.search(query_vector, k=1)
    return shipment_ids[indices[0][0]] if indices[0][0] < len(shipment_ids) else None

# 🔹 AI Response Generator using Ollama
def generate_response(user_query):
    prompt = f"""
    You are an AI assistant for shipment tracking and customer support.
    Answer the user's query based on shipment details.

    User Query: {user_query}
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# 🔹 API Endpoint: Get Shipment Details
@app.route("/track", methods=["POST"])
def track_shipment():
    data = request.json
    order_id = data.get("order_id")

    if order_id in shipments:
        return jsonify({"status": "success", "details": shipments[order_id]})
    else:
        return jsonify({"status": "error", "message": "Order not found"}), 404

# 🔹 API Endpoint: Ask AI for Help
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    response = generate_response(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
