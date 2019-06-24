#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Server part for OpenClassroom final exercise"""

import os
import socket
import select

"""
from classes import *
from functions import *

#Loading maps
while True:
    recheck = False
    maps = {}
    maps_dictionnary = {}
    counter = 1
    for map_name in os.listdir("maps/"):
        if map_name.endswith(".txt"):
            link_to_file = os.path.join("maps", map_name)
            maps_dictionnary[counter] = map_name
            counter+=1
    break
"""
host = ''
port = 12800
main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_connection.bind((host, port))
main_connection.listen(5)
print("Server set on port {}".format(port))
server_started = True
command_received =""
client_connected = []
while server_started:
    #Check if clients trying to connect every x ms
    asked_connection, wlist, xlist = select.select([main_connection], [], [], 0.05)
    for connection in asked_connection:
        connection_to_client, connection_infos = connection.accept()
        client_connected.append(connection_to_client)
        if connection_infos:    
            print(connection_infos)

    try:
        for client in client_connected:
            command_received = connection_to_client.recv(1024)
            print(command_received.decode())
            if command_received.decode() == "fin":
                server_started = False
                for client in client_connected:
                    client.send("Fermetre de la connection".encode())
                    client.close()
                main_connection.close()
            if command_received.decode() =="a":
                connection_to_client.send("Bien recu".encode())
    except:
        pass

""""            
    client_to_read = []
    try:
        client_to_read, wlist, xlist = select.select(client_connected, [], [], 0.05)
    except select.error:
        pass
    else:
        for client in client_connected:
            client.send(b"Welcome")
            #server_started = False
"""