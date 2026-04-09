import random

from .server import Server

class ServerRandomSelection(Server):

    def __init__(self, 
                 *args,
                 **kwargs):

        super().__init__(*args,
                         **kwargs)
 
        self.server_name = "random"

    def select_clients(self):

        self.selected_clients = random.sample(range(len(self.available_clients)),
                                              self.number_of_clients_to_select)

