import socket
from _thread import *
import pickle
from game import Game
from threading import Lock

server = "192.168.43.208"  # тут вставь свой ipv4 адрес

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0
lock = Lock()


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(2048*8).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetBoard(p)
                    elif data != "get":
                        game.setValue(data, p)

                    conn.sendall(pickle.dumps(game))


            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
        print("Game was created")

    start_new_thread(threaded_client, (conn, p, gameId))