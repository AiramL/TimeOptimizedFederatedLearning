from abc import ABC 
from abc import abstractmethod
from pickle import dump
import random

class Server(ABC):

    def __init__(self,
                 n_select_clients=5,
                 n_epochs=10,
                 file_name="result",
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
        
        self.available_clients = avalilable_clients
        self.selected_clients = []
        self.epochs_delays = []
        self.number_of_clients_to_select = n_select_clients
        self.number_of_epochs = n_epochs
        self.state = 0
        self.epoch = 0
        self.num_received_models = 0
        self.highest_delay = 0.0
        self.file_name = file_name

    @abstractmethod
    def select_clients(self):
        pass
    
    def send_model(self):
        for client_id in self.selected_clients:
            self.available_clients[str(client_id)].receive_model()

    def receive_models(self):
        if(len(self.selected_clients)-self.num_received_models):
            print("ok")
        else:
            print("not ok")
        
    def save(self,results):
        with open(self.file_name,"wb") as writer:
            dump(results,writer)


    def train(self):
        
        while(self.epoch < self.number_of_epochs+1):
            self.set_clients_state()
            self.highest_delay = 0.0
            #initial_time = self.state
            print("starting global epoch at state: ",self.state)
            

            print("global epoch: ", self.epoch)

            ''' select clients '''
            self.select_clients()

            ''' send model to the clients '''
            self.send_model()

            ''' receive models from clients '''
            self.num_received_models = 0
            self.receive_models()

            self.epochs_delays.append(self.highest_delay)
            
            print("server state: ", self.state)
            
            ''' update epoch '''
            self.update_epoch()
        
        ''' save result '''
        self.save(self.epochs_delays)

    def set_highest_delay(self,delay):
        print("client delay:", delay)
        print("highest delay: ",self.highest_delay)
        if delay > self.highest_delay:
            self.highest_delay = delay
    
    def update_epoch(self):
        self.epoch+=1

    def update_received_models(self):
        self.num_received_models+=1
        print("number of received models updated: ",self.num_received_models)
        print("number of models to be received: ", len(self.selected_clients)-self.num_received_models)

    def set_server_state(self, state):
        if state > self.state:
            self.state = state
    
    def set_clients_state(self):
        for client in self.available_clients.values():
            client.set_state(self.state)

class ServerRandomSelection(Server):

    def select_clients(self):
        self.selected_clients = random.sample(range(1,len(self.available_clients)+1),self.number_of_clients_to_select)

class ServerFixedSelection(Server):
    
    def set_selected_clients(self,clients_ids):
        self.selected_clients = clients_ids

    def select_clients(self):
        pass


class ServerTOFLSelection(Server):

    def load_estimator(self):
        pass

    def estimate_delay(self):
        pass


if __name__ == "__main__":
    server = ServerRandomSelection()

    for i in range(10):
        print(server.selected_clients)
        server.select_clients()