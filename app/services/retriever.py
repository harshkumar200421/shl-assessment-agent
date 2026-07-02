import pickle
import faiss
from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self):

        self.model = None

        self.index = faiss.read_index("app/data/catalog.faiss")

        with open("app/data/catalog.pkl", "rb") as f:
            self.catalog = pickle.load(f)

    def load_model(self):

        if self.model is None:
            self.model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

    def search(self, query: str, top_k: int = 10):

        self.load_model()

        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        distances, indices = self.index.search(
            embedding,
            top_k
        )

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