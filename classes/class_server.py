# -*- coding: utf-8 -*-
"""Class server"""
import socket
import select

class Server():
    def __init__(self, server_port):
        self.main_connection = ''
        self.server_port = server_port
        self.host = ''
        self.server_started = True
        self.client_connected = []
        self.command_received = ''
        self.connection_to_client = []
        self.connection_info = ''
        self.connection_infos = []

    #Start a server
    def launch_server(self):
        """Method use to start a server"""
        self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_connection.bind((self.host, self.server_port))
        self.main_connection.listen(5)

    #Accept client request for connection
    def accept_connection(self):
        """Method use to check and accept client request for connection"""
        while self.server_started:
            asked_connection, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
            if asked_connection: #If a connection is accepted
                for connection in asked_connection:
                    self.connection_to_client, self.connection_info = connection.accept()
                    self.client_connected.append(self.connection_to_client) #All clients are are stored in client_connected 'list'
                    self.connection_infos.append(self.connection_info) #All info are stored in connection_info 'list'
                #If a new client is connected, print it's connection information
                if self.connection_info:
                    print(self.connection_info)
    
    #End server
    def end_server(self):
        """Method use to close server and all client connected"""
        self.main_connection.close()
        for client in self.client_connected:
            client.close()


x = Server(12800)
x.launch_server()
x.accept_connection()
x.end_server()

    