from app.services.retriever import Retriever
from app.services.recommender import Recommender

retriever = Retriever()
recommender = Recommender()

query = "Hiring a backend Python developer with SQL and REST API knowledge."

results = retriever.search(query)

response = recommender.recommend(query, results)

print(response)