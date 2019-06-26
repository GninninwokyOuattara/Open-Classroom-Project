#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Server part for OpenClassroom final exercise"""

import os
from classes.class_server import *

#1st part -- Showing exinsting map in server terminal
map_folder = Map("maps")
map_folder.find_map_in_file()
map_folder.map_available()

chosen_map = input("Entrez un numéro de labyrinthe pour commencer à jouer : ")


port = input("Server port > ") #Gerer le regex plus tard
main = Server(int(port))
main.launch_server()
main.accept_connection()
