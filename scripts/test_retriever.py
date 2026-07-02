import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.services.retriever import Retriever

retriever = Retriever()

query = "I need an assessment for hiring a Python backend developer with SQL and REST API skills."

results = retriever.search(query)

print("=" * 80)

for i, item in enumerate(results, 1):
    print(f"\n{i}. {item['name']}")
    print(f"Score: {item['score']:.2f}")
    print(f"Duration: {item['duration']}")
    print(f"Job Levels: {item['job_levels']}")
    print(f"Category: {item['category']}")
    print("-" * 80)