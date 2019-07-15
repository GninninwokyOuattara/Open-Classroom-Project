#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Server part for OpenClassroom final exercise"""

import os
from classes.class_server import *

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
print("Partie commence ")
game_maze.show_maze()

#On met l'execution du thread en pause le temps d'un test
#game_server.thread_dict['thread_r_1'].start()

#A present il faut envoyer les cartes au deux joueurs connectés
game_maze.send_dict_maze(game_server)
#game_maze.send_maze_to_players(game_server)
#Utiliser le threading pour les clients afin de pouvoir envoyer et recevoir
#Les messages en meme temps
