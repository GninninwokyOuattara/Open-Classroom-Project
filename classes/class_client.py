# -*- coding: utf-8 -*-
"""Client class"""
import socket
import re
#from classes.class_server import Server
import json

class Client():
    def __init__(self):
        self.server_port = 12800
        self.host = 'localhost'
        self.regex_port = r"128[0-9]{2}"
        self.connection_to_server = ''
        self.player_own_number = '' #Player by order of arrival, first get 1 and so on

#    def get_regex_port():
#        return r"^128[0-9]{2}" #Between 12800 and 12899

    #OBSOLETE
    def client_base_setup(self):
        while True:
            self.server_port = input("Enter the server port > ")
            if not re.search(self.regex_port, self.server_port):
                continue
            else:
                break
        return self.server_port


    #Connection method
    def connection(self):
        """Method use to connect to a server, given the right port"""
        print("On tente de se connecter au server...")
        try:
            self.connection_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection_to_server.connect((self.host, int(self.server_port)))
            print("Connection établie avec le server. Port : {}".format(self.server_port))
            print("connexion etablie avec le serveur.")
            return True
        except:
            print("Connexion avec le server a echouée")

    def send(self):
        """Send message to server if message != '' """
        message = ''
        while True:
            message = input("> ")
            if len(message) != 0:
                message = message.encode
                self.connection_to_server.send(message)

    def receive(self):
        """Receive and print messages from server"""
        while True:
            message = self.connection_to_server.recv(1024)
            if len(message) != 0:
                message = message.decode()
                print(message)
                break
            else:
                #print("On break")
                break
        return message

    def receive_encoded_maze(self):
        
        encoded_maze = self.connection_to_server.recv(4096) #Receive the bytes type dictionnary
        encoded_maze = encoded_maze.decode() #decode it, bytes to str
        decoded_maze = json.loads(encoded_maze) #reconvert it from str to dict
        #print the dictionnary
        if type(decoded_maze) == dict:
            for value in decoded_maze.values(): 
                print(value)
        del encoded_maze
        """        
        elif type(decoded_maze) == str:
            return decoded_maze
        """
