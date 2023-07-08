"""library for chat visualization functions and classes"""
import socket
from time import sleep
import asyncio
from typing import Final, List
import textwrap

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer

from llm_chat.widgets import ChatMessage, UserColumn, ChatColumn, UserLabel
from llm_chat.utils import COLOR_LIST


class ChatVisualizer(App):
    """class for chat visualization"""
    CSS_PATH: Final[str] = "css/style.css"
    BINDINGS: Final[List[Binding]] = [
        Binding(key="d", action="toggle_dark", description="Toggle Light/Dark Mode"),
        Binding(key="q", action="quit", description="Quit"),
    ]

    def __init__(self, host: str = "127.0.0.1", port: int = 1337):
        """initialize the chat visualizer class"""
        super().__init__()
        self.chat_msgs: List[ChatMessage] = []
        self.users: dict[str, str] = {}
        # socket stuff
        self.host = host
        self.port = port
        self.running = False
        #asyncio.get_event_loop().run_until_complete(self.start_server())


    def start_server(self) -> None:
        """start the socket server with textual worker"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.push_message("system", "server started", "now")
        asyncio.create_task(self.get_messages())


    async def get_messages(self) -> None:
        """get messages from the socket"""
        sleep(1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        conn, _ = self.sock.accept()

        with conn:
            while True:
                sleep(0.1)
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode("utf-8")
                data = data.split(":")
                self.push_message(data[1], data[2], data[3])


    def action_toggle_dark(self) -> None:
        """an action to toggle dark mode."""
        self.dark = not self.dark


    def compose(self) -> ComposeResult:
        """compose the chat visualizer and yield the child widgets"""
        yield Header()
        yield UserColumn(id="user_container")
        yield ChatColumn(id="chat_container")
        yield Footer()
        if not self.running:
            self.start_server()


    def push_message(self, user: str, message: str, timestamp: str) -> None:
        """adds a ChatMessage widget to the chat_msgs list"""
        # check for users and add them to the user dict with a color
        if user not in self.users:
            if len(self.users) < len(COLOR_LIST):
                self.users[user] = COLOR_LIST[len(self.users)]
            else:
                self.users[user] = "gray"
            self.push_user(user)

        # sanitize the message and wrap it
        print_message: str = ""
        wrapper = textwrap.TextWrapper(width=70)

        for line in message.split("\n"):
            line = line.lstrip().rstrip()
            print_message += wrapper.fill(text=line)+"\n"

        new_message = ChatMessage(print_message)

        # add user and timestamp to the border title
        new_message.border_title = f"{user} - ({timestamp}):"
        new_message.styles.background = self.users[user]
        self.query_one("#chat_container").mount(new_message)


    def push_user(self, user: str) -> None:
        """adds a UserLabel widget to the user list"""
        user_label = UserLabel(user)
        user_label.styles.background = self.users[user]

        self.query_one("#user_container").mount(user_label)
