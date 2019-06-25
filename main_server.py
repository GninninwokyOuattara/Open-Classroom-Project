#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Server part for OpenClassroom final exercise"""

import os
from classes.class_server import *

port = input("Server port > ") #Gerer le regex plus tard
main = Server(int(port))
main.launch_server()
main.accept_connection()
