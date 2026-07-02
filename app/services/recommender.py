import json
import re

from app.core.prompts import SYSTEM_PROMPT
from app.services.llm import generate


class Recommender:

    def __init__(self):
        pass

    def _needs_clarification(self, query: str) -> bool:
        """
        Ask for more details when the query is too vague.
        """
        query = query.lower()

        vague_queries = [
            "assessment",
            "test",
            "recommend",
            "hire",
            "hiring",
            "job",
            "candidate"
        ]

        # Very short queries should trigger clarification
        if len(query.split()) <= 3:
            return True

        # Doesn't mention any role or technology
        keywords = [
            "python",
            "java",
            "developer",
            "engineer",
            "manager",
            "sales",
            "analyst",
            "sql",
            "aws",
            "react",
            "backend",
            "frontend",
            "data"
        ]

        if not any(k in query for k in keywords):
            return True

        return False

    def recommend(
        self,
        query: str,
        retrieved: list,
        conversation_history=None
    ):

        if conversation_history is None:
            conversation_history = []

        # ---------------------------------------
        # Ask clarification instead of guessing
        # ---------------------------------------
        if self._needs_clarification(query):

            return {
                "reply": (
                    "I'd be happy to help. "
                    "Could you please tell me:\n\n"
                    "• Which role are you hiring for?\n"
                    "• Experience level?\n"
                    "• Any important technical or behavioural skills?"
                ),
                "needs_clarification": True,
                "clarification_question": (
                    "Which role, experience level and skills should be assessed?"
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # ---------------------------------------
        # Build conversation
        # ---------------------------------------

        history = ""

        for item in conversation_history:
            role = item.get("role", "")
            content = item.get("content", "")
            history += f"{role}: {content}\n"

        # ---------------------------------------
        # Retrieved catalog
        # ---------------------------------------

        catalog = json.dumps(retrieved, indent=2)

        # ---------------------------------------
        # Final prompt
        # ---------------------------------------

        prompt = f"""
{SYSTEM_PROMPT}

Conversation History:

{history}

Current User Query:

{query}

Retrieved Assessments:

{catalog}
"""

        # ---------------------------------------
        # Gemini Response
        # ---------------------------------------

        response = generate(prompt)

        # ---------------------------------------
        # Parse JSON
        # ---------------------------------------

        try:
            return json.loads(response)

        except Exception:

            # Gemini sometimes returns JSON inside markdown

            match = re.search(r"\{.*\}", response, re.DOTALL)

            if match:

                try:
                    return json.loads(match.group())
                except Exception:
                    pass

            # Final fallback

            return {
                "reply": response,
                "needs_clarification": False,
                "clarification_question": "",
                "recommendations": [],
                "end_of_conversation": False
            }