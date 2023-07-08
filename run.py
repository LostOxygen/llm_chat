"""run the chat visualizer"""
import asyncio
from llm_chat.chat_visualizer import ChatVisualizer
from llm_chat.chat_server import start_server

if __name__ == "__main__":
    chat_viz = ChatVisualizer()
    chat_viz.run()
    # asyncio.run(start_server(chat_viz.push_message))
