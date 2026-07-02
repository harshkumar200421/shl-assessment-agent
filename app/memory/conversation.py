from typing import List, Dict


class ConversationMemory:
    """
    Stores conversation history for a single chat request.
    Later this can be replaced with Redis or a database.
    """

    def __init__(self):
        self.messages: List[Dict] = []

    def load(self, history: List[Dict]):
        self.messages = history or []

    def add_user(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def get_context(self):

        conversation = ""

        for msg in self.messages:
            conversation += f"{msg['role'].upper()}: {msg['content']}\n"

        return conversation

    def latest_user_message(self):
        for msg in reversed(self.messages):
            if msg["role"] == "user":
                return msg["content"]
        return ""