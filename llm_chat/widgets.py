"""library for custom widgets"""
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import VerticalScroll

class ChatMessage(Static):
    """widget class to display chat messages"""
    def __init__(self, message: str, user: str, user_face: str,
                 user_color: str, timestamp: str):
        """initialize the chat message widget"""
        super().__init__()
        self.message: str = message
        self.user: str = user
        self.user_face: str = user_face
        self.user_color: str = user_color
        self.time: str = timestamp

    def compose(self) -> ComposeResult:
        """compose the chat message widget and yield the child widgets"""
        # create the widgets
        user_chat_label = Label(self.user_face + " | " + \
                                self.user.upper()+" - (" + self.time + "):",
                                id="user_chat_label")

        # stylize
        user_chat_label.styles.background = self.user_color
        user_chat_label.styles.color = "#eceff4"

        yield user_chat_label
        yield Label("\n"+self.message)


class UserLabel(Static):
    """widget class to display the user labels"""
    def __init__(self, username: str):
        super().__init__()
        self.username: str = username

    def compose(self) -> ComposeResult:
        yield Label("\n" + "    " + self.username+"\n", id="user_label_text")


class UserColumn(VerticalScroll):
    """widget class to display the user column"""
    def compose(self) -> ComposeResult:
        yield Label("USERS")


class ChatColumn(VerticalScroll):
    """widget class to display the chat column"""
    def compose(self) -> ComposeResult:
        yield Label("CHAT", id="chat_header")
