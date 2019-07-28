# -*- coding: utf-8 -*-
"""Class server"""

import os
import socket
import select
import threading
import json
import random
import copy

                #SERVER

class Server(threading.Thread):
    def __init__(self):
        super().__init__()
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
        self.thread_dict = {}

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

                    #On creer un thread personnel pour le client connecté
                    self.thread_dict['thread_r_'+'{}'.format(self.player_number)] =\
                         threading.Thread(target = self.receive, args = (self.connection_to_client,) )

                    self.client_connected.append(self.connection_to_client) #All clients are are stored in client_connected 'list'
                    self.connection_infos.append(self.connection_info) #All info are stored in connection_info 'list'

                #If a new client is connected, print it's connection information
                if self.connection_info:
                    print(self.connection_info)
                    #server_started = False
            if self.player_number == 2: #Max player allowed
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
    
    def send(self, client_connected = [], labyrinthe = {}):
        """Method to send things to client(s)"""
        
        for client in client_connected:
            for values in labyrinthe.values():
                maze_line = values.encode()
                client.connected.send(maze_line)


    #ON HOLD
    def receive(self, connection_to_client):
        reception = True
        while reception:
            message = connection_to_client.recv(1024)
            message = message.decode()
            if message.lower() == "fin":
                reception == False
            else:
                print(message)



    
    #End server
    def end_server(self):
        """Method use to close server and connection w/ all client connected"""
        self.main_connection.close()
        for client in self.client_connected:

            client.close()

                    #MAP


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


                        #MAZE   

class Maze():
    def __init__(self, game_map):
        self.game_map = game_map
        self.game_maze = {}
        self.game_maze_dimension = ()
        self.wall = "O"
        self.portal = "."
        self.exit = "U"
        #self.player_robot_list = ['1', '2']
        self.position_player1 = ['1',()]
        self.position_player2 = ['2', ()]

 
    def update_position(self, player):
        """Method that can be run anytime to automaticaly 
        catch player (given as parameter) position in the maze"""
        for key, value in self.game_maze.items():
            if player[0] in self.game_maze[key]:
                player[1] = (key, self.game_maze[key].index(player[0]))

    def create_maze_from_map(self):
        with open(self.game_map[1], "r") as _map:
            number = 1
            for lines in _map:
                if not lines ==  "\n" or lines == '':
                    self.game_maze[number] = lines.rstrip()
                    number += 1


    def show_maze(self):

        for value in self.game_maze.values():
            if not value == '':
                print(value)

    def send_maze_to_players(self, game_server):
        #game_server = object, pour avoir accès a toutes les variables de l'objet
        for player in game_server.client_connected:
            number = 1
            for i in range(len(self.game_maze)):
                game_server.connection_to_client.send(self.game_maze[number].encode())
                number+=1
            """    
            for value in self.game_maze.values():
                value = value.encode()
                game_server.connection_to_client.send(value)
            """   

    def send_dict_maze(self, game_server):
        """Method used to send maze to connectd client"""
        encoded_maze = json.dumps(self.game_maze) #Convert the dict to str with json
        encoded_maze = encoded_maze.encode() #Encode the str to bytes
        for player in game_server.client_connected:
            player.send(encoded_maze)

    def maze_dimension(self):
        """Method used to get a proper dimension of the maze
        in the tuple form (line, column)"""
        x = len(self.game_maze.keys()) #Max lines number
        y = len(self.game_maze[1]) #Max columns number
        self.game_maze_dimension = (x, y)
    
    def maze_dim(self):
        return (len(self.game_maze.keys()), len(self.game_maze[1]))



    def assign_random_position_to_player(self, player):
        """Method used to assign a random position to the player
        - player parameter = player_robot_list[0] or [1]

        Not an issue but can probably be confusing, coordonate are tuple (x, y)
        x for lines and y for columns.
        Since keys represent lines  1 is indeed 1 in (1, y).
        but for element in x that are string, (1, 2) represent not the second element
        but the third one.
        
        """
        #self.maze_dimension()
        self.game_maze_dimension = self.maze_dim()

        #We generate a list of x lines and y columns in the maze scope
        #x_list = [x for x in range (self.game_maze_dimension[0] + 1) if x != 0]
        #y_list = [y for y in range (self.game_maze_dimension[1] + 1) if y != 0]
        x_list = []
        y_list = []
        for x in range(self.game_maze_dimension[0]):
            #if not x == 0:
            x_list.append(x + 1)
        for y in range(self.game_maze_dimension[1]):
            #if not y == 0:
            y_list.append(y)

        #We loop until we find a good spot
        while True:
            #We generate a random coordinate (x,y) in the scope the maze
            #x = random.choice(x_list)
            #y = random.choice(y_list)
            coordinate = (random.choice(x_list), random.choice(y_list))
            print(coordinate)

            #We verify that this generated coordinate isn't a wall, a portal, an exit
            #or litteraly another player
            #Wall = O, Portal = ., Exit = U
            print(self.game_maze[coordinate[0]][coordinate[1]])
            if self.game_maze[coordinate[0]][coordinate[1]] in \
                [self.wall, self.exit, self.portal, self.position_player1[0],\
                     self.position_player2[0]]:
                #We disregard that positon
                continue
            
            else:
                player[1] = coordinate 
                #We assign this position to player
                #player = (coordinate[0], coordinate[1])
                #We generate a list of all element in the line associated with the x coordinate
                liste = []
                for element in self.game_maze[coordinate[0]]:
                    liste.append(element)
                #Set the player robot in the right place
                print(liste[coordinate[1]])
                liste[coordinate[1]] = player[0]
                #Convert the list of element into a string and update in the maze
                liste = "".join(liste)
                self.game_maze[coordinate[0]] = liste
                break

    def send_dict_re(self, game_server):
        """
        Edit and send maze to the players.
        Own player see himself in 'X' while opponenent is 'x'
        """
        
        self.update_position(self.position_player1)
        self.update_position(self.position_player2)

        #Copie du dictionnaire
        fake_maze = copy.deepcopy(self.game_maze)

        #Premier player self.position_player1
        for key, value in fake_maze.items():
            #Si on trouve la position du premier joueur
            if self.position_player1[0] in fake_maze[key]:
                val = []
                for value in fake_maze[key]:
                    val.append(value)
                val[self.position_player1[1][1]] = 'X'
                val = "".join(val)
                fake_maze[key] = val
                """
                for element in val:
                    if element == self.position_player1[0]:
                        element = 'X'
                        val = "".join(val)
                        fake_maze[key] = val
                """
            #Si on trouve la position du second joueur
            if self.position_player2[0] in fake_maze[key]:
                val = []
                
                for value in fake_maze[key]:
                    val.append(value)
                """
                for element in val:
                    if element == self.position_player2[0]:
                        element = 'x'
                        val = "".join(val)
                        fake_maze[key] = val
                """
                val[self.position_player2[1][1]] = 'x'
                val = "".join(val)
                fake_maze[key] = val

        encoded_maze = json.dumps(fake_maze) #Convert the dict to str with json
        encoded_maze = encoded_maze.encode() #Encode the str to bytes  
        game_server.client_connected[0].send(encoded_maze)         

        #Second player#
        fake_maze = copy.deepcopy(self.game_maze)

        #Deuxieme player self.position_player2
        for key, value in fake_maze.items():
            #Si on trouve la position du premier joueur
            if self.position_player2[0] in fake_maze[key]:
                val = []
                for value in fake_maze[key]:
                    val.append(value)
                """
                for element in val:
                    if element == self.position_player1[0]:
                        element = 'x'
                        val = "".join(val)
                        fake_maze[key] = val
                """
                val[self.position_player2[1][1]] = 'X'
                val = "".join(val)
                fake_maze[key] = val
            #Si on trouve la position du second joueur
            if self.position_player1[0] in fake_maze[key]:
                val = []
                for value in fake_maze[key]:
                    val.append(value)
                """
                for element in val:
                    if element == self.position_player2[0]:
                        element = 'X'
                        val = "".join(val)
                        fake_maze[key] = val
                """
                val[self.position_player1[1][1]] = 'x'
                val = "".join(val)
                fake_maze[key] = val
        encoded_maze = json.dumps(fake_maze) #Convert the dict to str with json
        encoded_maze = encoded_maze.encode() #Encode the str to bytes  
        game_server.client_connected[1].send(encoded_maze) 