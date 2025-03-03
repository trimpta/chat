from __future__ import annotations
import socket
import threading
import logging
import sys
import re
from enum import Enum

class MsgType(Enum):
    MSG = "MSG"
    CMD = "CMD"
    ERR = "ERR"

class commands:
    list = {}

    @classmethod 
    def register(cls, func, command, desc):
        cls.list[command] = [func, desc]

    @classmethod
    def use(cls, command, *args, **kwags):

        if command not in cls.list:
            raise ValueError(f"Invalid command: {command}")
        
        return cls.list[command][0](*args, **kwags)


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

    done = False
    connected = []
    commands = {}
    _valid_nick = re.compile(r"^[A-Za-z0-9\-_\.]{3,20}$")
    seperator = " :"

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
        self.nick = ""

        #get_nick returns True on success
        if self.get_nick():
            User.connected.append(self)

    def broadcast_msg(self, content: str):

        for user in User.connected:
            if user != self:
                user.send(
                    f"{self.nick}{User.seperator}{content}".encode()
                )

    def close(self):
        self.conn.close()
        
        try:
            self.connected.remove(self)
        except ValueError:
            pass

    def send(self, type: Enum, content: str) -> None:
        self.conn.send(
            (type.value + content).encode()
        )

    def whisper(self, message: str, sender: User | None = None) -> None:

        prefix = sender.nick + User.seperator if sender is not None else ''
        self.send(MsgType.MSG, prefix + message)

    def recv(self) -> tuple:
        msg = self.conn.recv(1024).decode()
        command_value, content = msg[:3], msg[3:]

        try:
            command = MsgType(command_value)
        except ValueError:
            self.close()
            raise ValueError(f"Invalid command recieved from {self.nick}: {command_value}")


        return command, content


    def get_nick(self):
        #Ask conn for nickname

        self.send(MsgType.CMD, "NICK_PLS")
        type, nick = self.recv()

        if type is not MsgType.CMD:
            self.conn.close()
            return False

        if re.fullmatch(self._valid_nick, nick) is None:
            self.send(MsgType.ERR, "NICK_INVALID")
            return False
            
        if nick in self.connected:
            self.send(MsgType.ERR, "NICK_TAKEN")
            return False

        self.send(MsgType.CMD, "NICK_OK")
        self.nick = nick

        return True

    def handle_cmd(self, val: str):
        
        command, *content = val.split()
        content = ' '.join(content)


        
        

    def run(self):
        
        while not self.done:

            type, msg = self.recv()

            if type is MsgType.CMD:
                self.handle_cmd(msg)

            if type is MsgType.MSG:
                self.broadcast_msg(msg)