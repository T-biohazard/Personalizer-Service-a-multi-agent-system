import json
import chromadb
from sentence_transformers import SentenceTransformer

_embedder = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _client.get_or_create_collection("catalog")

def index_catalog(path: str = "data/catalog/courses.json"):
    with open(path) as f:
        items = json.load(f)

    ids = [item["id"] for item in items]
    docs = [item["title"] for item in items]
    metadatas = [{"topic": item["topic"], "level": item["level"]} for item in items]
    embeddings = _embedder.encode(docs).tolist()

    _collection.upsert(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings)
    print(f"Indexed {len(items)} catalog items.")

def search(query: str, top_k: int = 3) -> list[dict]:
    query_embedding = _embedder.encode([query]).tolist()
    results = _collection.query(query_embeddings=query_embedding, n_results=top_k)

    return [
        {"title": doc, "topic": meta["topic"], "level": meta["level"]}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]