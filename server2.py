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

s.listen()  # unlimited players, use game id to limit players
print("Waiting for a connection. Server started.")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount  # to keep track number of games running
    conn.send(str.encode(str(p)))  # so we know if it's player 1 or 2

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]  # to check if the game still exists
                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost Connection")
    try:
        del games[gameId]
        print("Closing game: ", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()  # accept incoming connection and store connection and address to conn and addr
    print("Connected to:", addr)

    idCount += 1
    p = 0  # number of players
    gameId = (idCount - 1)//2  # every 2 players connected to the server, game id increment by 1 (rock paper scissors, 2 players for 1 game)
    if idCount % 2 == 1:
        # if number of players is not even, we need to create a new game and wait for a new player to join
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))  # to run threaded_client without stopping the while loop (using thread)
