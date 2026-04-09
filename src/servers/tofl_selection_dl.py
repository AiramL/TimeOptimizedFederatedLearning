import torch

from collections import deque
from math import floor

from utils.estimator.architecture import EstimatorLSTM
from .tofl import ServerTOFLSelection

class ServerEstimatorTOFLSelectionDL(ServerTOFLSelection):

    def __init__(self, 
                 **kwargs):
        
        super().__init__(**kwargs)

        self.estimator = EstimatorLSTM(base_station_range=self.base_station_range)

        self.server_name = "tofl"

        self.past_delays = { client_id : (deque(10*[100],10),
                                          deque(10*[100],10))
                             for client_id in 
                             self.available_clients.keys() }

    def update_past_delays(self):

        if self.state < 10:
        
            begin = 0

        else:
            begin = self.state-10

        for client_id in self.available_clients.keys():
            
            info = self.clients_info[client_id].iloc[begin:self.state]

            # we need to rethink about the logic to replace the values
            for value in info['Throughput DL']:
                self.past_delays[client_id][0].appendleft(value)
                #self.clients_estimated_delays[client_id][0].appendleft(value)

            for value in info['Throughput UL']:
                self.past_delays[client_id][1].appendleft(value)
                #self.clients_estimated_delays[client_id][1].appendleft(value)

    def receive_data_chunk(self, 
                           data, 
                           client_id):
        
        time_last_chunk = 0.0


        window = torch.tensor(list(self.past_delays[client_id][0]),
                              dtype=torch.float32).view(-1,1)

        estimated_delay = self.estimator.predict(window)

        self.past_delays[client_id][0].appendleft(
            estimated_delay)


        maximum_chunk_size = floor(self.message_period * 
                                   1000 * 
                                   estimated_delay)

        if (maximum_chunk_size >= data):

            time_last_chunk = data/(1000 * 
                                    estimated_delay)
            
            return 0, time_last_chunk

        return data - maximum_chunk_size, time_last_chunk
    
    ''' disconsider the upload delay '''
    def send_data_chunk(self, 
                        data,  
                        client_id,
                        state=0):
        return 0.0
    
    def get_delay(self, 
                  client_id):

        remaining_data = self.model_size
        time = 0

        while (remaining_data):
            
            self.logger.debug("remaining data: %d state: %d", remaining_data, self.state)
        
            remaining_data, time_last_chunk = self.receive_data_chunk(remaining_data, 
                                                                      client_id)
            if remaining_data:

                time+=1
                
        return float(0.1 * (time + time_last_chunk))

    def estimate_delay(self):

        for client in self.available_clients.keys():
            
            self.logger.debug("estimating delay client %s" % client)
            self.logger.debug("estimating download delay")    
            self.clients_estimated_delays[client] = self.get_delay(client)

