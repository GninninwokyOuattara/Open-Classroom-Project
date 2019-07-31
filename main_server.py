#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Server part for OpenClassroom final exercise"""

import os
from classes.class_server import *
from functions.server_functions import encoded_then_sent
import json
import time
from classes.class_commande import Commande

#1st part -- Showing exinsting map in server terminal
map_folder = Map("maps")
map_folder.find_map_in_file()

#Displaying available map
"""
number = 1
for key in map_dictionnary.keys():
    print("{} - {}".format(number, key))
    number+=1
"""
map_folder.map_available()

#Choix de carte
while True:
    chosen_map = int(input("Entrez un numéro de labyrinthe pour commencer à jouer : "))
    if not chosen_map in map_folder.map_found.keys():
        continue
    else:
        #On assigne a game_map le dictionnaire composé de la clé correspondant 
        #au numéro de la carte choisi ainsi que ses attributs
        game_map = map_folder.map_found[chosen_map]
        break

game_maze = Maze(game_map) #Passe en parametre la carte choisi pour le jeu
game_maze.create_maze_from_map() #Genere le dictionnaire de maniere à permettre les
                            #Deplacement

print("On attend les client")


game_server = Server()
game_server.launch_server()
game_server.accept_connection()

#Send player connection infos to other player
all_connection_infos = json.dumps(game_server.connection_infos)
all_connection_infos = all_connection_infos.encode()
#game_server.connection_to_client.sendall(all_connection_infos)
for client in game_server.client_connected:
    client.send(all_connection_infos)

#Il faut assigner une position aléatoire a chaque client dans le labyrinthe.
game_maze.assign_random_position_to_player(game_maze.position_player1)
game_maze.assign_random_position_to_player(game_maze.position_player2)

print("Partie commence ")
command = Commande()
game_maze.show_maze()
game_maze.portals_coor()



#On met l'execution du thread en pause le temps d'un test
#game_server.thread_dict['thread_r_1'].start()

#A present il faut envoyer les cartes au deux joueurs connectés
game_maze.send_dict_re(game_server)

#On attend le signal du joueur 2
verif = game_server.connection_to_client.recv(1024)
#On envoie 'La partie commence !' a nos client connecté apres reception du signal
if verif:
    message = "La partie commence !"
    """
    for client in game_server.client_connected:
        client.send(message.encode())
    """
    game_server.client_connected[0].send(message.encode())
    game_server.client_connected[1].send(message.encode())

time.sleep(5)
#Le serveur doit à présent indiquer aux players a qui est le tour
#Tout en manageant les commandes que ses clients entreront
partie = True
turn = 1

while True:
    if turn ==1:
        player = game_maze.position_player1
        #Tour au premier joueur donc
        encoded_then_sent(game_server.client_connected[0], turn, str)
        #encoded_then_sent(game_server.client_connected[1], turn, str)
        turn = 2
        commande = game_server.client_connected[0].recv(1024)
        if commande:
            commande = commande.decode()
            first_part, second_part, action_or_move = command.command_check(commande)
            if action_or_move == "action":
                game_maze.action(first_part, second_part, player)
            elif action_or_move == "move":
                game_maze.move(first_part, second_part, player)



        #game_server.client_connected[0].send(b"Commande recu")
        #Methode qui va traiter la commande
    if turn == 2:
        player = game_maze.position_player2
        #Tour au second joueur donc
        encoded_then_sent(game_server.client_connected[1], turn, str)
        turn = 1
        commande = game_server.client_connected[1].recv(1024)
        #game_server.client_connected[1].send(b"Commande recu")
        if commande:
            commande = commande.decode()
            first_part, second_part, action_or_move = command.command_check(commande)
            if action_or_move == "action":
                game_maze.action(first_part, second_part, player)
            elif action_or_move == "move":
                game_maze.move(first_part, second_part, player)
    
    #Une fois tout les traitements executer on envoie les dictionnaires aux joueurs.
    
    game_maze.send_dict_re(game_server)
    game_maze.show_maze()

        
        


#game_maze.send_maze_to_players(game_server)
#Utiliser le threading pour les clients afin de pouvoir envoyer et recevoir
#Les messages en meme temps
