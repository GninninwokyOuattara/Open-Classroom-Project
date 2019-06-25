# -*- coding: utf-8 -*-
from classes.class_client import Client

player = Client()
player.client_base_setup()
print(player.server_port)
print(player.host)
player.connection()
message = player.connection_to_server.recv(1024)
print(message.decode())
while True:
    message = input("> ")
    #if message.lower() != "fin":
    player.connection_to_server.send(message.encode())
    message = player.connection_to_server.recv(1024)
    print(message.decode())