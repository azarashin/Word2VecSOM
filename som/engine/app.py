import os
import socket

from gensim.models import KeyedVectors

class WordSimWebApp:
    def __init__(self, port):
        self._port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), self._port))  # IPとポート番号を指定します
        s.listen(5)

        while True:
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established!")
            clientsocket.send(bytes("Welcome to the server!", 'utf-8'))
            clientsocket.close()

if __name__ == '__main__':
    app = WordSimWebApp(8080)
    app.run()