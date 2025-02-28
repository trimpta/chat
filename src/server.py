import socket
import threading
import logging
import sys
import json
import re

class Networking:
    ADDR = ('', 5906)

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    @classmethod
    def set_addr(self, ip: str, port: int):
        self.ADDR = (ip, port)

    def accept(self):
        self.server.listen()

        while True: #Use events here
            
            try:
                conn, addr = self.server.accept()
                user = User(conn, addr)
            except Exception as e:
                raise
        

class User:

    connected = []
    _valid_nick = re.compile(r"^[A-Za-z0-9\-_\.]{3,20}$")

    def __contains__(self, user: str | User) -> bool:
        
        if isinstance(user, User):
            return user in self.connected
        
        elif isinstance(user, str):
            
            for i in self.connected:
                if i.nick == user:
                    return True
            
            return False


    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

        try:
            self.authenticate()
            User.connected.append(self)
        except Exception as e:
            raise

    def send_text(self, message: str):
        self.conn.send(message.encode())

    def recv_text(self) -> str:
        return self.conn.recv(1024).decode()

    def authenticate(self):
        #Ask conn for nickname
        self.send_text("NICK_PLS")

        


