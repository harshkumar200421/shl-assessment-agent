from typing import List, Dict
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., description="Current user query")

    conversation_history: List[Dict] = Field(
        default_factory=list,
        description="Previous conversation between user and assistant"
    )


class Recommendation(BaseModel):
    name: str
    reason: str


class ChatResponse(BaseModel):
    reply: str

    needs_clarification: bool = False

    clarification_question: str = ""

    recommendations: List[Recommendation] = Field(default_factory=list)

    end_of_conversation: bool = False