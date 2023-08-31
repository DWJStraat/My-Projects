import socket


class RemotePython:
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=5006):
        self.c = None
        self.addr = None
        self.host = host
        self.port = port
        self.socket = socket.socket()

    def start_host(self):
        self.socket.bind((self.host, self.port))
        print(f"Server started on {self.host}:{self.port}!")
        self.socket.listen(100)
        self.c, self.addr = self.socket.accept()
        print(f"Connection from {self.addr} has been established!")

    def connect(self, target_host=None, target_port=5006):
        if target_host is None:
            target_host = self.host
        self.socket.connect((target_host, target_port))
        print(f"Connected to {target_host}:{target_port}!")

    def send(self, data):
        self.socket.send(data.encode('utf-8'))
        print(f"Sent {data} to {self.addr}!")

    def receive(self):
        return self.socket.recv(1024)



