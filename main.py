import socket
from _thread import *
import sys
import heroku3

server = "0.0.0.0"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  s.bind((server, port))
except socket.error as e:
  str(e)

s.listen(2)

print("Awaiting connection, Server Started!")

def make_pos(tup):
  return str(tup[0]), (tup[1])

def read_pos(str):
  str = str.split(",")
  return int(str[0]), int(str[1])

pos = [(0,0),(100, 100)]
def threded_client(conn, plr):
  conn.send(str.encode(make_pos(pos[plr])))
  reply = ""
  while True:
    try:
      data = read_pos(conn.recv(2048).decode())
      pos[plr] = data
      
      if not data:
        print("Disconnected")
        break
      else:
        if plr == 1:
          reply = pos[0]
        else:
          reply = pos[1]
        print("Recvd", data)
        print("sending", reply)
      conn.sendall(str.encode(make_pos(reply)))
    except:
      break
  print("Lost connetion")
  conn.close()
currentPlayer = 0
while True:
  conn, addr = s.accept()
  print("user",addr,"connected!")
  start_new_thread(threded_client, (conn, currentPlayer))
  currentPlayer += 1