"""api test"""
from llm_chat.api import ChatAPI

if __name__ == "__main__":
    api = ChatAPI()
    api.add_message("jonathan", "schönen guten Morgen")
