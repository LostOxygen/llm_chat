"""library for chat visualization functions and classes"""
from typing import Final, List
import textwrap
import os

from textual.timer import Timer
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer

from llm_chat.widgets import ChatMessage, UserColumn, ChatColumn, UserLabel
from llm_chat.utils import COLOR_LIST

PATH: Final[str] = "/tmp/llm_chat/"


class ChatVisualizer(App):
    """class for chat visualization"""
    CSS_PATH: Final[str] = "css/style.css"
    BINDINGS: Final[List[Binding]] = [
        Binding(key="d", action="toggle_dark", description="Toggle Light/Dark Mode"),
        Binding(key="q", action="quit", description="Quit"),
    ]
    data_timer: Timer

    def __init__(self):
        """initialize the chat visualizer class"""
        super().__init__()
        self.chat_msgs: List[ChatMessage] = []
        self.users: dict[str, str] = {}
        self.curr_chat_len: int = 0
        # check if the paths are valid
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        os.remove(PATH+"chat_log.txt")


    def action_toggle_dark(self) -> None:
        """an action to toggle dark mode."""
        self.dark = not self.dark


    def compose(self) -> ComposeResult:
        """compose the chat visualizer and yield the child widgets"""
        yield Header()
        yield UserColumn(id="user_container")
        yield ChatColumn(id="chat_container")
        yield Footer()


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


    async def on_mount(self) -> None:
        """on button event handler"""
        self.data_timer = self.set_interval(1, self.retreive_msgs, repeat=0)


    def retreive_msgs(self) -> None:
        """load messages from"""
        with open(PATH+"chat_log.txt", "r", encoding="utf-8") as chat_file:
            try:
                chat = chat_file.read()
                if len(chat) == 0:
                    return

                curr_line_counter: int = 0
                for line in chat.split("\n"):
                    print(line)
                    curr_line_counter += 1
                    if self.curr_chat_len < curr_line_counter and line != "":
                        self.curr_chat_len += 1
                        msg = line.split(":")
                        self.push_message(msg[1], msg[2], msg[3]+msg[4])
            except EOFError:
                return
