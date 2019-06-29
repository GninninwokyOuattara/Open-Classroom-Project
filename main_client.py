# -*- coding: utf-8 -*-
from classes.class_client import Client
import sys

player = Client()
#player.client_base_setup()
print(player.server_port)
print(player.host)

connect = False
while not connect:
    connect = player.connection()
    if not connect:
        reconnect = input("Rééssayer ? (o/n) : ")
        if reconnect.lower() == "o":
            continue
        else:
            sys.exit()

message = player.connection_to_server.recv(1024)
print(message.decode())
while True:
    message = input("> ")
    #if message.lower() != "fin":
    player.connection_to_server.send(message.encode())
    message = player.connection_to_server.recv(1024)
    print(message.decode())