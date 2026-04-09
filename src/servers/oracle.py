from math import floor

from .tofl import ServerTOFLSelection

class ServerOracleTOFLSelection(ServerTOFLSelection):

    def __init__(self, 
                 **kwargs):
        
        super().__init__(**kwargs)


        self.computational_delays = []
        self.estimated_state = 0

        self.server_name = "tofl_oracle"
                                
        if self.number_of_clients_to_select > len(self.dataframe['Node ID'].unique()):

            # Invalid Number
            raise Exception


    def local_training(self):

        pass

    def client_receive_model(self, 
                             client_id, 
                             time):

        state = time
        elapsed_time = time
        remain_data = self.model_size
        
        if state >= self.clients_info[client_id]['Throughput UL'].shape[0]:
                    
            state = state % self.clients_info[client_id]['Throughput UL'].shape[0]
        
        while (remain_data):

            remain_data, _ = self.receive_data_chunk(remain_data, 
                                                     client_id, 
                                                     state)
            
            if remain_data:

                if state + 1 < self.clients_info[client_id]['Throughput DL'].shape[0]:
                    
                    state += 1
                    elapsed_time += 1

                else:

                    state = 0 
                    elapsed_time += 1


        ''' training '''
        self.local_training()

        return elapsed_time 
    

    def client_send_model(self, 
                          client_id, 
                          time):

        initial_time = time
        state = time
        elapsed_time = time 

        remain_data = self.model_size
                
        if state >= self.clients_info[client_id]['Throughput UL'].shape[0]:
                    
            state = state % self.clients_info[client_id]['Throughput UL'].shape[0]
        
        while (remain_data):
        
            remain_data, time_last_chunk = self.send_data_chunk(remain_data, 
                                                                client_id, 
                                                                state)
            
            if remain_data:

                if state + 1 < self.clients_info[client_id]['Throughput UL'].shape[0]:
                    
                    elapsed_time += 1
                    state += 1

                else:
                    
                    elapsed_time += 1
                    state = 0
                
        return float(0.1 * (elapsed_time + 
                            time_last_chunk - 
                            initial_time))



    def send_data_chunk(self, 
                        data, 
                        client_id, 
                        state=0):
        
        time_last_chunk = 0.0

        maximum_chunk_size = floor(self.message_period * 1000 * 
                                   self.clients_info[client_id]['Throughput UL'].iloc[state])
                
        if (maximum_chunk_size >= data):

            time_last_chunk = data/(1000 * 
                                    self.clients_info[client_id]['Throughput UL'].iloc[state])
            
            return 0, time_last_chunk

        return data - maximum_chunk_size, time_last_chunk

    
    def receive_data_chunk(self, 
                           data, 
                           client_id, 
                           state=0):

        time_last_chunk = 0.0

        maximum_chunk_size = floor(self.message_period * 1000 * 
                                   self.clients_info[client_id]['Throughput DL'].iloc[state])

        if (maximum_chunk_size >= data):

            time_last_chunk = data/(1000 * 
                                    self.clients_info[client_id]['Throughput DL'].iloc[state])
            
            return 0, time_last_chunk

        return data - maximum_chunk_size, time_last_chunk
    
    def estimate_delay(self):

        for client in self.available_clients.keys():
            
            self.logger.debug("estimating delay client %s" % client) 
            
            # server -> client
            self.logger.debug("estimating download delay")
            time = self.client_receive_model(client, self.state)

            # server <- client
            self.logger.debug("estimating upload delay")
            time  = self.client_send_model(client, time)
            
            self.clients_estimated_delays[client] = time


