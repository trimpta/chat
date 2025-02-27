import socket
import threading

class networking:
    ADDR = ('', 5906)

    @classmethod
    def set_addr(self, ip: str, port: int):
        self.ADDR = (ip, port)

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def accept(self):
        self.server.listen()

        while True: #Use events here
            ...
        

class users:

    connected = []

    def __init__(self):
        pass    