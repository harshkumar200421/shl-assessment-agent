import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Opening catalog...")

with open("app/data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")

documents = []

for item in catalog:
    text = f"""
Assessment Name: {item.get('name', '')}

Description:
{item.get('description', '')}

Job Levels:
{', '.join(item.get('job_levels', []))}

Categories:
{', '.join(item.get('keys', []))}

Languages:
{', '.join(item.get('languages', []))}

Duration:
{item.get('duration', '')}

Remote Testing:
{item.get('remote', '')}

Adaptive:
{item.get('adaptive', '')}
"""
    
    documents.append(text)

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("Building FAISS index...")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "app/data/catalog.faiss")

with open("app/data/catalog.pkl", "wb") as f:
    pickle.dump(catalog, f)

print("✅ Done!")