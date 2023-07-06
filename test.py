"""test file for backend"""
from backend import llm_chat_api

llm_chat_api.start_api()
llm_chat_api.handle_message(user="jonny", message="hello", timestamp="2021-01-01 00:00:00")
