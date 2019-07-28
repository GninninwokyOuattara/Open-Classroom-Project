# -*- coding: utf-8 -*-
from classes.class_client import Client
from classes.class_commande import Commande
import sys
import threading
import re
import json

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


            

#On receptionne le message de bienvenue
message = player.connection_to_server.recv(1024)
#On recupere le numero du joueur.
player.player_own_number = int(message.decode()[-1]) 
print(message.decode())

#Recoit les infos des connections
data = player.connection_to_server.recv(1024)
if data:
    data = data.decode()
    data = json.loads(data)
    #Data contient toutes les données, celle du joueur incluse
    own = player.connection_to_server.getsockname()
    for element in data:
        if element == own:
            #On supprime cette donnée
            data.remove(own)

print(data)

#Commande class
commande = Commande()

#Regex commande pour demarrer partie
commande_start_partie = re.compile(r"^C$")
#Regex tour des joueurs
turn = re.compile(r"[1-2]")

#thread_receive = threading.Thread(target = player.receive, args = ())

player.receive_encoded_maze() #Receive maze from server

#Les utilisateurs doivent attendre que le joueur 2, demarre la partie 
#Joueur 2 demarre la partie en entrant C
if not player.player_own_number == 2:
    #message = player.connection_to_server.recv(1024)
    #player.receive()
    message = player.connection_to_server.recv(1024)
    if message:
        print(message)

else:
    
    while True:   
        action = str(input("Entrer C pour commencer à jouer : \n"))
        #if not commande_start_partie.search(commande):
        if not re.search(commande.c_partie, action):
            continue
        else:
            #Si C, on fait signe au serveur afin d'entammer le prochain stade
            player.connection_to_server.send(action.encode())
            #player.connection_to_server.recv(1024)
            break
    #message = player.connection_to_server.recv(1024)
    message = player.connection_to_server.recv(1024)
    if message:
        print(message)



#Les clients/Players doivent attendre leur tour pour lancer une action
while True:
    player_turn = player.receive()
        #Le serveur indique a qui est le tour
        #player_turn doit etre un entier entre 1 et 2       
    if str(player.player_own_number) == player_turn:
        while True:
            action = input("Votre tour \n")
            if re.search(commande.re_moove, action) \
                or re.search(commande.re_action, action):
                break           
            else:
                print("Action invalide")
                continue
        player.connection_to_server.send(action.encode())       
    else:
        continue


while True:
    message = input("> ")
    #if message.lower() != "fin":
    player.connection_to_server.send(message.encode())
    #message = player.connection_to_server.recv(1024)
    #print(message.decode())


