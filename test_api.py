"""api test"""
from time import sleep
from llm_chat.api import ChatAPI

if __name__ == "__main__":
    api = ChatAPI()
    sleep(1)
    api.send_message("jonathan", "schönen guten Morgen")
    sleep(1)
    api.close_connection()
