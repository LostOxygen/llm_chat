"""library module for routes"""
from datetime import datetime
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask("LLM_Chat_API")
sock = SocketIO(app)


def start_api() -> None:
    """start the api"""
    app.run(host="localhost", port="8080", debug=True)


@app.route("/")
@app.route("/index")
def index() -> None:
    """index page"""
    return "<h1>LLM Chat API</h1>"


@sock.on("connect", namespace="/handle_user")
def handle_message(user: str, message: str, timestamp: datetime) -> None:
    """add message to the chat"""
    print(f"User: {user} Message: {message} Timestamp: {timestamp}")
    send(message)
