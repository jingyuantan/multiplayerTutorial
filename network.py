# this network.py is used by client.py to communicate with server.py
import socket
import pickle  # to send data using bits (0,1), can encode decode


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.101"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()  # to let server know which player is it currently communicating

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)  # this is to establish connection
            # when connected, server will send something back and the following will receive the 'something'
            return pickle.loads(self.client.recv(2048))  # for first example, this will receive player's data eg x & y coordinates, color etc
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

