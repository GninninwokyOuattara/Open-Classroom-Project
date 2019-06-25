# -*- coding: utf-8 -*-
"""Class server"""
import socket
import select
from threading import Thread

class Server():
    def __init__(self, server_port):
        self.main_connection = ''
        self.server_port = int(server_port)
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
        server_started = True #
        """Method use to check and accept client request for connection"""
        while server_started:
            asked_connection, wlist, xlist = select.select([self.main_connection], [], [], 0.05)
            if asked_connection: #If a connection is accepted
                for connection in asked_connection:
                    self.connection_to_client, self.connection_info = connection.accept()
                    #welcome_message(self.connection_to_client)
                    self.connection_to_client.send(b"Welcome")
                    self.client_connected.append(self.connection_to_client) #All clients are are stored in client_connected 'list'
                    self.connection_infos.append(self.connection_info) #All info are stored in connection_info 'list'

                #If a new client is connected, print it's connection information
                if self.connection_info:
                    print(self.connection_info)
                    #server_started = False

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


#x = Server(12800)
#x.launch_server()
#x.accept_connection()

#while x.server_started:
#    x.client_message()

#x.end_server()

    