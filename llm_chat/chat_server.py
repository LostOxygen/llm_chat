"""library for server functions"""
import asyncio
from typing import List, Callable

chat_function: Callable


async def start_server(chat: Callable) -> None:
    """handle the socket connection"""
    global chat_function
    chat_function = chat
    server = await asyncio.start_server(handle_connection, "localhost", 1337)
    async with server:
        await server.serve_forever()


async def handle_connection(reader, writer) -> None:
    """handle the socket connection via asyncio sockets as a background task"""
    data_list: List = []
    data = (await reader.read(255)).decode("utf8")
    data_list = data.split(":")
    print(data_list)
    if data_list[0] == "MSG":
        chat_function(data_list[1], data_list[2], data_list[3])
    elif data_list[0] == "EXT":
        writer.close()
    writer.close()
    await writer.wait_closed()
