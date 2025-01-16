from abc import ABC 
from abc import abstractmethod
import random

class Server(ABC):

    def __init__(self,
                 n_select_clients=5,
                 n_epochs=10,
                 avalilable_clients={"1":1,
                                     "2":2,
                                     "3":3,
                                     "4":4,
                                     "5":5,
                                     "6":6,
                                     "7":7,
                                     "8":8,
                                     "9":9,
                                     "10":10,}):
        
        self.avalilable_clients = avalilable_clients
        self.selected_clients = []
        self.number_of_clients_to_select = n_select_clients
        self.number_of_epochs = n_epochs
        self.current_state = 0
        self.epoch = 0

    @abstractmethod
    def select_clients(self):
        pass
    
    ''' need to implement '''
    def train():
        pass

    def update_epoch(self):
        self.epoch+=1

    def set_server_state(self, state):
        self.state = state
    
    def set_clients_state(self):
        for client in self.avalilable_clients.values():
            client.set_state(self.state)

class ServerRandomSelection(Server):

    def select_clients(self):
        self.selected_clients = random.sample(range(1,len(self.avalilable_clients)+1),self.number_of_clients_to_select)


class ServerTOFLSelection(Server):

    def load_estimator():
        pass

    def estimate_delay(self):
        pass


if __name__ == "__main__":
    server = ServerRandomSelection()

    for i in range(10):
        print(server.selected_clients)
        server.select_clients()