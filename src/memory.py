from typing import List, Dict


class ConversationMemory:
    """Simple conversation memory for the academic assistant."""

    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_user_message(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self):
        return self.messages

    def get_formatted_history(self):
        if not self.messages:
            return "No previous conversation."

        history = []

        for message in self.messages:
            role = message["role"].capitalize()
            content = message["content"]

            history.append(f"{role}: {content}")

        return "\n".join(history)

    def clear(self):
        self.messages = []