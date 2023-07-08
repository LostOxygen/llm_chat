"""API class implementation to interact with the ChatVisuzalization class"""
import socket
from datetime import datetime

class ChatAPI:
    """socket API class to interact with ChatVisualization class"""
    def __init__(self, host: str = "127.0.0.1", port: int = 1337):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def send_message(self, user: str, message: str):
        """send data to the socket"""
        timestamp = datetime.now().strftime("%d. %B %Y %I:%M%p")
        final_msg = f"MSG:{user}:{message}:{timestamp}"
        self.sock.sendall(final_msg.encode("utf-8"))


    def close_connection(self):
        """close the socket connection"""
        self.sock.sendall("EXT".encode("utf-8"))
        self.sock.close()
