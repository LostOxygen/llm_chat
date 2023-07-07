"""library for custom widgets"""
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import VerticalScroll

class ChatMessage(Static):
    """widget class to display chat messages"""
    def __init__(self, message: str):
        """initialize the chat message widget"""
        super().__init__()
        self.message: str = message

    def compose(self) -> ComposeResult:
        """compose the chat message widget and yield the child widgets"""
        yield Label(self.message)


class UserLabel(Static):
    """widget class to display the user labels"""
    def __init__(self, username: str):
        super().__init__()
        self.username: str = username

    def compose(self) -> ComposeResult:
        yield Label(self.username)


class UserColumn(VerticalScroll):
    """widget class to display the user column"""
    def compose(self) -> ComposeResult:
        yield Label("USERS")


class ChatColumn(VerticalScroll):
    """widget class to display the chat column"""
    def compose(self) -> ComposeResult:
        yield Label("CHAT", id="chat_header")
