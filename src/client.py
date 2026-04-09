import os

from math import floor

from utils.utils import create_logger

class Client(object):

    def __init__(self,  
                 model_size=527, # in kB
                 message_period=0.1, # in seconds
                 client_id=1,
                 server=None,
                 datapath='executions/mean_tp.csv',
                 n_rounds=100,
                 timeout=120): 

        ''' Read the 5G dataset to add at 
        client object the communications conditions. '''    
        df  = datapath
        self.dataframe = df[df['Node ID'] == client_id].reset_index()
        self.state = 0 # indicates the dataset line used to calculate the delay
        self.model_size = model_size
        self.message_period = message_period
        self.client_id = client_id
        self.server = server
        self.round = 0
        self.time_last_chunk = 0.0
        self.computation_delay = [ 0 for i in range(n_rounds)] # in seconds
        self.timeout = timeout
        self.round_beginning = 0.0
        self.elapsed_time = 0.0

        log_path = "logs/clients/"
        self.logger = create_logger(log_path,
                                    "client_"+str(client_id))
        
    # TODO: to implement the training part
    def local_training(self,
                       elapsed_time):

        self.set_state(self.state + (self.computation_delay[self.round]/
                                     self.message_period))

        return elapsed_time + (self.computation_delay[self.round]/
                                     self.message_period)

    def set_server(self, server):

        self.server = server  
    
    def get_delay(self):

        return float(0.1 * (self.elapsed_time +
                            self.time_last_chunk - 
                            self.round_beginning))
    
    def set_state(self, 
                  state):
        
        if state < self.dataframe.shape[0]:
    
            self.state = int(state)

        else:
            
            self.state = state % self.dataframe.shape[0]

    # Sends the model to the aggregation server
    def send_model(self):

        remain_data = self.model_size

        self.logger.debug(f"sending model to server {self.server}")    
        while (remain_data):
            
            self.logger.debug(f"client ID: {self.client_id}, state: {self.state}")
            remain_data = self.send_data_chunk(remain_data)
            
            if remain_data:
                
                self.elapsed_time += 1
                self.update_state()

        self.logger.debug(f"state: {self.state}")
        self.logger.debug(f"initial state {self.round_beginning}")
        self.logger.debug(f"last chunck: {float(self.time_last_chunk)}")
        self.logger.debug("time to send the model: %f" % 
                          float(0.1 * (self.elapsed_time + 
                                       self.time_last_chunk - 
                                       self.round_beginning)))

        if self.server is not None:
        
            self.server.update_received_models()
            self.server.set_highest_delay(float(0.1 * (self.elapsed_time +
                                                       self.time_last_chunk - 
                                                       self.round_beginning)))

            self.server.set_server_state(self.state, 
                                         self.elapsed_time)
            
    # Sends the maximum data as possible during the message period 
    def send_data_chunk(self, 
                        data):
        
        maximum_chunk_size = floor(self.message_period * 1000 * 
                                   self.dataframe['Throughput UL'].iloc[self.state])
                
        if (maximum_chunk_size >= data):

            self.time_last_chunk = data/(1000 * 
                                         self.dataframe['Throughput UL'].iloc[self.state])
                                         
            return 0 # no more data to send
        
        return data - maximum_chunk_size # remain data to send



    def receive_model(self):

        self.round_beginning = self.state
        self.elapsed_time = self.state
        remain_data = self.model_size

        self.logger.debug(f"receiving model {self.server}")
        while (remain_data):
        
            self.logger.debug(f"client ID: {self.client_id} state: {self.state}")
            remain_data = self.receive_data_chunk(remain_data)
            
            if remain_data:

                self.elapsed_time += 1
                self.update_state()

        # final time
        self.logger.debug("time to receive the model: %f" % 
                          float(0.1 * (self.elapsed_time + 
                                       self.time_last_chunk - 
                                       self.round_beginning)))
        # training 
        self.elapsed_time = self.local_training(self.elapsed_time)

        # send model back to the server 
        self.send_model()
        
    

    def receive_data_chunk(self,
                           data):

        maximum_chunk_size = floor(self.message_period * 
                                   1000 * 
                                   self.dataframe['Throughput DL'].iloc[self.state])
                
        if (maximum_chunk_size >= data):
        
            self.time_last_chunk = data/(1000 * 
                                         self.dataframe['Throughput DL'].iloc[self.state])
            return 0 # no more data to send

        return data - maximum_chunk_size # remain data to send
    
    # Updates client's positions and communications conditions. 
    def update_state(self):
        
        if self.state + 1 < self.dataframe.shape[0]:
    
            self.state += 1

        # reset to the initial point
        else:
            
            self.state = 0


        


''' Class test '''    

if __name__ == '__main__':

    client = Client()
    client.receive_model()
    client.send_model()
    


