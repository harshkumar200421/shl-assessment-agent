from fastapi import APIRouter
from app.models.schema import ChatRequest
from app.services.retriever import Retriever
from app.services.recommender import Recommender

router = APIRouter(tags=["Chat"])

retriever = Retriever()
recommender = Recommender()


def build_search_query(query: str, history: list) -> str:
    """
    Build a richer search query using the conversation history.
    This helps follow-up questions such as:
    'Also include personality'
    """

    context = ""

    if history:
        for message in history[-6:]:
            role = message.get("role", "")
            content = message.get("content", "")

            if role == "user":
                context += content + " "

    context += query

    return context.strip()


@router.post("/chat")
def chat(request: ChatRequest):

    # ---------------------------------------------
    # Build search query
    # ---------------------------------------------

    search_query = build_search_query(
        request.query,
        request.conversation_history
    )

    # ---------------------------------------------
    # Semantic Search
    # ---------------------------------------------

    retrieved = retriever.search(
        search_query,
        top_k=10
    )

    # ---------------------------------------------
    # Recommendation Engine
    # ---------------------------------------------

    response = recommender.recommend(
        query=request.query,
        retrieved=retrieved,
        conversation_history=request.conversation_history
    )

    # ---------------------------------------------
    # If Gemini returned recommendation names only,
    # enrich them with catalog details.
    # ---------------------------------------------

    enriched = []

    if isinstance(response, dict):

        recommendations = response.get("recommendations", [])

        if recommendations:

            catalog_lookup = {
                item["name"]: item
                for item in retrieved
            }

            for rec in recommendations:

                if isinstance(rec, dict):

                    name = rec.get("name")

                    if name in catalog_lookup:

                        assessment = catalog_lookup[name]

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

    # ---------------------------------------------
    # Fallback
    # ---------------------------------------------

    return {
        "reply": str(response),
        "needs_clarification": False,
        "clarification_question": "",
        "recommendations": [],
        "end_of_conversation": False
    }