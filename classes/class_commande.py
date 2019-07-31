#Classe 'Commande'
#Sera hérité par les classes 'class_client' et 'class_server'
#Contient l'ensemble des commandes et methode possibles d'utilisation

import re


class Commande():
    """Class permettant de gerer toutes les commandes possible
    - Executable par le client
    - Traitable par le serveur
    """
    def __init__(self):
        self.move = ['N', 'S', 'O', 'E'] #Direction possible
        self.action = ['M', 'P'] #Action possible
        self.re_move = r"^[NSOE]{1}([0-9]{1})?$"
        self.re_action = r"^[PM]{1}[NSOE]{1}$"
        self.c_partie = r"^[cC]{1}$"
    
    def compile_regex(self):
        """
        Compile tout les regex 
        """
        self.re_move = re.compile(self.re_move)
        self.re_action = re.compile(self.action)

    def command_check(self, commande):
        """Verifie si la commande est valide, si valide, elle l'a traite
        - Retourne 2 elements : first_part, second_part
        du fait du format des commandes, second_part peut etre None
        """
        if re.search(self.re_move, commande):
            action_or_move = "move"
            if not len(commande) == 2:
                first_part = commande[0]
                second_part = "1"
            else:
                first_part = commande[0]
                second_part = commande[1]
            return first_part, second_part, action_or_move 

        elif re.search(self.re_action, commande):
            action_or_move = "action"
            first_part = commande[0]
            second_part = commande[0]
            return first_part, second_part, action_or_move
