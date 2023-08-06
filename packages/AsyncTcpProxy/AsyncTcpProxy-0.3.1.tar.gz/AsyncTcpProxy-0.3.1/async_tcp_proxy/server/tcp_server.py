#! /usr/bin/env python3

import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MSG_SIZE = 1024     # 1KB for socket data transmition

class TcpServer:
    def __init__(self, host: str = HOST,
                 port: int = PORT,
                 msg_size: int = MSG_SIZE):
        self._host = host
        self._port = port
        self._msg_size = msg_size

    def start(self):
        """ Start listening to incoming requests. """
        # socket.AF_INET => ipv4; socket.SOCK_STREAM => TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._host, self._port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('connected by', addr)
                while True:
                    try:
                        data = conn.recv(MSG_SIZE)
                        print('received', repr(data))
                        if not data: break
                        conn.sendall(data)
                    except KeyboardInterrupt:
                        print('Stoping server.')
                        break


if __name__ == "__main__":
    print('Server starts.')
    server = TcpServer()
    server.start()

