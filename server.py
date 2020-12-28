import socket
from _thread import *
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
print("Waiting for a connection. Server started.")


def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)  # the amount of info we trying to receive
            reply = data.decode("utf-8")  # when sending data need encode, so receive need decode

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))  # send data need encode

        except:
            break

    print("Lost connection.")
    conn.close()


while True:
    conn, addr = s.accept()  # accept incoming connection and store connection and address to conn and addr
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, ))  # to run threaded_client without stopping the while loop (using thread)
