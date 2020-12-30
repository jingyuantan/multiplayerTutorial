import socket
import pickle  # to send data using bits (0,1), can encode decode


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.101"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))  # for first example
            # return self.client.recv(2048).decode()  # for second example
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))  # for first example
            # self.client.send(str.encode(data))  # send a string to server, for second example
            return pickle.loads(self.client.recv(2048))  # receive an object from server
        except socket.error as e:
            print(e)

