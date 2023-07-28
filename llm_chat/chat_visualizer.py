"""library for chat visualization functions and classes"""
from typing import Final, List, Tuple
import textwrap
import os
from datetime import datetime

from textual.timer import Timer
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Input
from textual.message import Message

from llm_chat.widgets import ChatMessage, UserColumn, ChatColumn, UserLabel
from llm_chat.utils import COLOR_LIST, ASCII_FACES
from llm_chat.api import ChatAPI

PATH: Final[str] = "/tmp/llm_chat/"


class ChatVisualizer(App):
    """class for chat visualization"""
    CSS_PATH: Final[str] = "css/style.css"
    BINDINGS: Final[List[Binding]] = [
        Binding(key="q", action="quit", description="Quit"),
    ]
    data_timer: Timer

    def __init__(self):
        """initialize the chat visualizer class"""
        super().__init__()
        self.chat_msgs: List[ChatMessage] = []
        self.users: dict[str, Tuple(str, str, str)] = {}
        self.curr_chat_len: int = 0
        # check if the paths are valid
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        if os.path.isfile(PATH+"chat_log.txt"):
            os.remove(PATH+"chat_log.txt")
        if os.path.isfile(PATH+"chat_input_log.txt"):
            os.remove(PATH+"chat_input_log.txt")


    def action_toggle_dark(self) -> None:
        """an action to toggle dark mode."""
        self.dark = not self.dark


    def compose(self) -> ComposeResult:
        """compose the chat visualizer and yield the child widgets"""
        yield Header()
        yield UserColumn(id="user_container")
        chat_column = ChatColumn(id="chat_container")
        #chat_column.styles.scrollbar = "black"
        yield chat_column
        yield Input(placeholder="Type message.. (Enter to send)", id="input_field")
        yield Footer()


    def push_message(self, user: str, message: str, timestamp: str) -> None:
        """adds a ChatMessage widget to the chat_msgs list"""
        # check for users and add them to the user dict with a color
        if user not in self.users:
            if len(self.users) < len(COLOR_LIST):
                self.users[user] = (COLOR_LIST[len(self.users)],
                                    COLOR_LIST[len(self.users)].darken(0.1),
                                    ASCII_FACES[len(self.users)])
            else:
                self.users[user] = ("gray", "(⋟﹏⋞)")
            self.push_user(user)

        # sanitize the message and wrap it
        print_message: str = ""
        wrapper = textwrap.TextWrapper(width=70)

        for line in message.split("\n"):
            line = line.lstrip().rstrip()
            print_message += wrapper.fill(text=line)+"\n"

        msg_color = self.users[user][0]
        user_color = self.users[user][1]
        user_face = self.users[user][2]
        new_message = ChatMessage(print_message, user, user_face, user_color, timestamp)

        # add user and timestamp to the border title
        new_message.border_title = f"{user} - ({timestamp}):"
        new_message.styles.background = msg_color

        self.query_one("#chat_container").mount(new_message)


    def push_user(self, user: str) -> None:
        """adds a UserLabel widget to the user list"""
        user_label = UserLabel(user)
        user_label.styles.background = self.users[user][0]

        self.query_one("#user_container").mount(user_label)


    async def on_mount(self) -> None:
        """on button event handler"""
        self.data_timer = self.set_interval(1, self.load_msgs, repeat=0)


    def load_msgs(self) -> None:
        """load messages from"""
        if not os.path.isfile(PATH+"chat_log.txt"):
            return

        with open(PATH+"chat_log.txt", "r", encoding="utf-8") as chat_file:
            try:
                chat = chat_file.read()
                if len(chat) == 0:
                    return

                curr_line_counter: int = 0
                for line in chat.split("@"):
                    curr_line_counter += 1
                    if self.curr_chat_len < curr_line_counter and line != "":
                        self.curr_chat_len += 1
                        msg = line.split("|")
                        self.push_message(msg[1], msg[2], msg[3])
            except EOFError:
                return


    def on_input_submitted(self, submitted: Message) -> None:
        """when the enter key is pressed, this event is triggered"""
        self.add_input_message(str(submitted.value))
        self.query_one(Input).value=""


    def add_input_message(self, message: str) -> None:
        """adds the message from the chat text input to the api text file"""

        if message == "":
            return

        timestamp = datetime.now().strftime("%d. %B %Y %I:%M%p")
        self.push_message("human", message, timestamp)
        ChatAPI.add_input_message(message)
