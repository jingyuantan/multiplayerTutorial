*This is just my personal learning exp on creating a simple multiplayer game (socket and threading)
*full credits to 'Tech with Tim' youtube channel
*learn pygame

The process of a simple game created by the code

Example 1: (2 boxes moving around)
1. run the server.py (s.listen() will continuously look for connection)

2. player 1 and 2 created

3. run client.py for player 1 (main() will be called in client.py)
- client.py will create a network object that will be used to communicate with server

4. in server.py, while loop:
- accept connection from client.py (s.accept())
- start a new thread for the client connected 
- thread will proceed to deal with the connection (continuously, in a while loop) * more continue in point 5
- the main while loop will return to accept incoming connections (if any)
- increment the player number (ready to accept player 2 connection)
5. the thread created will send player data to the client network connection immediately after the connection established.

6. after reveiving player data, network will pass the data back to client (n.getP()).

7. Now we have all the required info for our own player (eg player 1), now we need data of player 2 too to print on the window
- this step will be run in a while loop (to continuously getting other player's data to be printed on the game window)
- so, from client, we send player 1 info to server through network (n.send(p1))
- now in server.py, in the while loop of the thread (this while loop will continuously looking to receive data from client)
  - if data is received (eg p1 data from client.py),  server.py will return player 2 data back to player 1 (client.py).
  - note: send() function will send p1 info to server and return the p2 data back to p1 client.
  - so when we have p1 and p2 data, we can redraw the window. (data as in x,y coordinates, color, etc)
- in this while loop, client will be constantly look for own player movement too, and to be updated in player object. (We have 2 player object in this case, p1 and p2)