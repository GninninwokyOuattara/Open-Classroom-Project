# -*- coding: utf-8 -*-
from classes.class_client import Client

player = Client()
player.client_base_setup()
print(player.server_port)
print(player.host)
player.connection()

player.connection_to_server.send(b"Heya!")