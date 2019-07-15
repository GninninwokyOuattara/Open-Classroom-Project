# -*- coding: utf-8 -*-
from classes.class_client import Client
import sys
import threading

player = Client()
#player.client_base_setup()
print(player.server_port)
print(player.host)

connect = False
while not connect:
    connect = player.connection()
    if not connect:
        reconnect = input("Réessayer ? (o/n) : ")
        if reconnect.lower() == "o":
            continue
        else:
            sys.exit()

message = player.connection_to_server.recv(1024)
print(message.decode())

#thread_receive = threading.Thread(target = player.receive, args = ())

player.receive_encoded_maze() #Receive maze from server

while True:
    message = input("> ")
    #if message.lower() != "fin":
    player.connection_to_server.send(message.encode())
    #message = player.connection_to_server.recv(1024)
    #print(message.decode())


