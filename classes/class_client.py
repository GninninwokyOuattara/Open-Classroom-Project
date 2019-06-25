# -*- coding: utf-8 -*-
"""Client class"""
import socket
import re

class Client():
    def __init__(self):
        self.server_port = ''
        self.host = 'localhost'
        self.regex_port = r"128[0-9]{2}"
        self.connection_to_server = ''

#    def get_regex_port():
#        return r"^128[0-9]{2}" #Between 12800 and 12899

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
        self.connection_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_to_server.connect((self.host, int(self.server_port)))
        print("Connection établie avec le server. Port : {}".format(self.server_port))
        

    
