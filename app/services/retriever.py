import os
import pickle
import faiss

from sentence_transformers import SentenceTransformer


class Retriever:

    _model = None

    def __init__(self):

        base_dir = os.path.dirname(os.path.dirname(__file__))

        index_path = os.path.join(base_dir, "data", "catalog.faiss")
        catalog_path = os.path.join(base_dir, "data", "catalog.pkl")

        self.index = faiss.read_index(index_path)

        with open(catalog_path, "rb") as f:
            self.catalog = pickle.load(f)

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading embedding model...")

            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

            print("Embedding model loaded.")

        return cls._model

    def search(self, query: str, top_k: int = 10):

        model = self.get_model()

        embedding = model.encode(
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

            results.append(
                {
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "duration": item.get("duration"),
                    "job_levels": item.get("job_levels"),
                    "remote": item.get("remote"),
                    "adaptive": item.get("adaptive"),
                    "category": item.get("keys"),
                    "link": item.get("link"),
                    "score": float(score),
                }
            )

        return results