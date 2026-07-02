import faiss
import pickle
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load FAISS index
        self.index = faiss.read_index("app/data/catalog.faiss")

        # Load catalog metadata
        with open("app/data/catalog.pkl", "rb") as f:
            self.catalog = pickle.load(f)

    def search(self, query: str, top_k: int = 10):
        # Create embedding for the user's query
        query_embedding = self.model.encode([query])

        # Search FAISS
        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx, score in zip(indices[0], distances[0]):
            if idx == -1:
                continue

            item = self.catalog[idx]

            results.append({
                "name": item.get("name"),
                "description": item.get("description"),
                "duration": item.get("duration"),
                "job_levels": item.get("job_levels"),
                "remote": item.get("remote"),
                "adaptive": item.get("adaptive"),
                "category": item.get("keys"),
                "link": item.get("link"),
                "score": float(score)
            })

        return results