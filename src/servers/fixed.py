from pickle import load

from .server import Server

class ServerFixedSelection(Server):
    
    def __init__(self, 
                 *args,
                 **kwargs):

        super().__init__(*args,
                         **kwargs)
 
        self.server_name = "fixed"
    
    def set_selected_clients(self,clients_ids):
        self.selected_clients = clients_ids

    def select_clients(self):
        pass


class ServerFixedTestSelection(Server):

    def select_clients(self):
        with open("test/epoch"+str(self.epoch),"rb") as loader:
            self.selected_clients = load(loader)