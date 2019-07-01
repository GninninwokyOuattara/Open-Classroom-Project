# -*- coding: utf-8 -*-
"""Class server"""

import os
import socket
import select
from threading import Thread

class Server():
    def __init__(self):
        self.main_connection = ''
        #self.server_port = int(server_port)
        self.server_port = 12800
        self.host = ''
        self.server_started = True
        self.client_connected = []
        self.command_received = ''
        self.connection_to_client = []
        self.connection_info = ''
        self.connection_infos = []
        self.player_number = 0

    #Start a server
    def launch_server(self):
        """Method use to start a server"""
        self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_connection.bind((self.host, self.server_port))
        self.main_connection.listen(5)

    #Accept client request for connection
    def accept_connection(self):
        server_started = True #
        """Method use to check and accept client request for connection"""
        while server_started:
            asked_connection, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
            if asked_connection: #If a connection is accepted
                for connection in asked_connection:
                    self.connection_to_client, self.connection_info = connection.accept()
                    #welcome_message(self.connection_to_client)
                    self.player_number += 1
                    message = "Bienvenue Joueur {}".format(self.player_number)
                    self.connection_to_client.send(message.encode())

                    self.client_connected.append(self.connection_to_client) #All clients are are stored in client_connected 'list'
                    self.connection_infos.append(self.connection_info) #All info are stored in connection_info 'list'

                #If a new client is connected, print it's connection information
                if self.connection_info:
                    print(self.connection_info)
                    #server_started = False
            if self.player_number == 2:
                break

    def client_message(self):
        for client in self.client_connected:
            message = client.recv(1024)
            if message.decode() == " ":
                continue
            elif message.decode().lower() == "fin":
                print(message.decode())
                self.server_started = False
                client.send(b"Server closed")
            else:
                print(message.decode())
    
    def welcome_message(self, client):
        message = "Welcome"
        message = message.encode()
        client.send(message)


    
    #End server
    def end_server(self):
        """Method use to close server and all client connected"""
        self.main_connection.close()
        for client in self.client_connected:

            client.close()


class Map():
    def __init__(self, map_folder):
        self.map_folder = map_folder #Where our map are
        self.map_found = {}


    def find_map_in_file(self): 
        number = 1
        for file_name in os.listdir(self.map_folder):
            if file_name.endswith(".txt"):
                link = os.path.join(self.map_folder, file_name)
                #self.map_found[file_name[:-4]] = link
                self.map_found[number] = (file_name[:-4], link)
                number+=1
        return self.map_found


    def map_available(self):
        for key, value in self.map_found.items():
            print("{} - {}".format(key, value[0]))

class Maze():
    def __init__(self, game_map):
        self.game_map = game_map
        self.game_maze = {}


    def create_maze_from_map(self):
        with open(self.game_map[1], "r") as _map:
            number = 1
            for lines in _map:
                if not lines ==  "\n":
                    self.game_maze[number] = lines.rstrip()
                    number += 1


    def show_maze(self):

        for value in self.game_maze.values():
            print(value)
    

