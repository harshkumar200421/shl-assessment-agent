from fastapi import APIRouter
from app.models.schema import ChatRequest
from app.services.retriever import Retriever
from app.services.recommender import Recommender

router = APIRouter(tags=["Chat"])

retriever = None
recommender = None


def get_retriever():
    global retriever

    if retriever is None:
        retriever = Retriever()

    return retriever


def get_recommender():
    global recommender

    if recommender is None:
        recommender = Recommender()

    return recommender


def build_search_query(query: str, history: list):

    context = ""

    if history:
        for message in history[-6:]:
            if message.get("role") == "user":
                context += message.get("content", "") + " "

    context += query

    return context.strip()


@router.post("/chat")
def chat(request: ChatRequest):

    retriever = get_retriever()
    recommender = get_recommender()

    search_query = build_search_query(
        request.query,
        request.conversation_history
    )

    retrieved = retriever.search(
        search_query,
        top_k=10
    )

    response = recommender.recommend(
        query=request.query,
        retrieved=retrieved,
        conversation_history=request.conversation_history
    )

    enriched = []

    if isinstance(response, dict):

        recommendations = response.get("recommendations", [])

        catalog_lookup = {
            item["name"]: item
            for item in retrieved
        }

        for rec in recommendations:

            if isinstance(rec, dict):

                assessment = catalog_lookup.get(rec.get("name"))

                if assessment:

                    enriched.append({
                        "name": assessment.get("name"),
                        "reason": rec.get("reason", ""),
                        "description": assessment.get("description"),
                        "duration": assessment.get("duration"),
                        "job_levels": assessment.get("job_levels"),
                        "category": assessment.get("category"),
                        "remote": assessment.get("remote"),
                        "adaptive": assessment.get("adaptive"),
                        "link": assessment.get("link")
                    })

        response["recommendations"] = enriched

        return response

    return {
        "reply": str(response),
        "needs_clarification": False,
        "clarification_question": "",
        "recommendations": [],
        "end_of_conversation": False
    }