import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer


class Recommender:

    def __init__(self):

        print("Retriever initializing...")

        self.model = None

        base = os.path.join("app", "data")

        index_path = os.path.join(base, "catalog.faiss")
        pkl_path = os.path.join(base, "catalog.pkl")

        print(f"Loading FAISS index from {index_path}")

        self.index = faiss.read_index(index_path)

        print("FAISS loaded")

        print(f"Loading catalog from {pkl_path}")

        with open(pkl_path, "rb") as f:
            self.catalog = pickle.load(f)

        print(f"Catalog loaded: {len(self.catalog)} records")

    def load_model(self):

        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )
            print("Embedding model loaded.")

    def search(self, query: str, top_k: int = 10):

        self.load_model()

        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        distances, indices = self.index.search(embedding, top_k)

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