import socket
from _thread import *
from player import Player
from game import Game
import pickle
import sys

# always run server script first, before you can run multiple client script (multiplayer)
# run server script on my machine (the machine the ip below stated), and run client
server = "192.168.0.101"  # ip here
port = 5555  # port here

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)  # number of client connecting to server eg number of players
# s.listen()  # unlimited players, use game id to limit players
print("Waiting for a connection. Server started.")

# initialize players
# store player health and cards here
players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(conn, player):
    # when we connect we want to send something immediately back to the object that connected to us (client.network)
    # this will be sent to network.py, look at def connect()
    # return pickle.loads(self.client.recv(2048)) <------ this will receive the following data, in this case the player's data
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            # receive data from the connection (client.py)
            data = pickle.loads(conn.recv(2048))  # 2048=the amount of info we trying to receive, can increase/decrease
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                # print("Received: ", data)
                # print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))  # send data need encode

        except:
            break

    print("Lost connection.")
    conn.close()


currentPlayer = 0
# s.listen will continuously looking for connection
# if there is incoming connection, this while loop will accept the connection etc and go back to s.listen
while True:
    conn, addr = s.accept()  # accept incoming connection and store connection and address to conn and addr
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))  # to run threaded_client without stopping the while loop (using thread)
    currentPlayer += 1  # a new player connected
