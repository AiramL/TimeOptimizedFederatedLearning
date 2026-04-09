

from abc import (
    ABC ,
    abstractmethod
)

from collections import deque

from .server import Server

class ServerTOFLSelection(Server, 
                          ABC):

    def __init__(self, 
                 datapath="data/processed/v2x_mobility_0_mean.csv",
                 **kwargs):

        super().__init__(**kwargs)
        

        self.past_delays = { client_id : (deque(10*[100],10),
                                          deque(10*[100],10))
                                         for client_id in 
                                         self.available_clients.keys() }

        self.clients_estimated_delays = { client_id : 100.0
                                         for client_id in 
                                         self.available_clients.keys() }
    

        self.dataframe = datapath 
        
        self.clients_info = { str(client_id): self.dataframe[
                                self.dataframe['Node ID'] == int(client_id)].reset_index() 
                                for client_id in 
                                self.available_clients.keys() }
        
        
    @abstractmethod
    def receive_data_chunk():
        pass
    
    @abstractmethod
    def send_data_chunk():
        pass
    
    @abstractmethod
    def estimate_delay(self):
        pass

    def select_clients(self):

        selected_clients = []

        total_estimated_delay = []

        self.estimate_delay()

        for client, delay in self.clients_estimated_delays.items():
   
            total_estimated_delay.append((delay,client))
            total_estimated_delay.sort()

        num_selected_clients = 0 
        while num_selected_clients < self.number_of_clients_to_select:
            
            selected_clients.append(int(total_estimated_delay[
                                    num_selected_clients][1]))
            
            num_selected_clients+=1

        self.selected_clients = selected_clients


