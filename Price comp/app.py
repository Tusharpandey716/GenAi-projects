import requests
import chromadb
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

# Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("products")

# Add CORS Middleware to allow frontend requests
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fetch product data from Fake Store API
FAKE_STORE_API = "https://fakestoreapi.com/products"
try:
    response = requests.get(FAKE_STORE_API)
    response.raise_for_status()  # Raise error if the request fails
    products = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    products = []

# Store products in ChromaDB with embeddings (Only if not already added)
existing_ids = set(collection.get()["ids"]) if collection.get() else set()

for product in products:
    product_id = str(product["id"])
    if product_id not in existing_ids:  # Prevent duplicate entries
        embedding = model.encode(product["title"]).tolist()
        collection.add(
            ids=[product_id],
            embeddings=[embedding],
            metadatas=[{
                "title": product["title"],
                "description": product["description"],
                "price": product["price"],
                "category": product["category"],
                "image": product["image"]
            }]
        )

@app.get("/search")
def search_products(query: str = Query(..., title="Search Query")):
    query_embedding = model.encode(query).tolist()
    
    # Retrieve top matching products
    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=5
    )
    
    if "metadatas" not in results or not results["metadatas"][0]:
        return {"query": query, "results": []}  # Return empty results if nothing found

    products_found = [
        {
            "title": res["title"],
            "description": res["description"],
            "price": res["price"],
            "category": res["category"],
            "image": res["image"]
        }
        for res in results["metadatas"][0]
    ]

    return {"query": query, "results": products_found}
