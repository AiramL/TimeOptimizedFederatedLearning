import pandas as pd
import logging  
from math import floor

class Client(object):

    def __init__(self,  
                 model_size=527, # in kB
                 message_period=0.1, # in seconds
                 client_id=1,
                 server=None,
                 datapath='executions/mean_tp.csv',
                 n_epochs=100): 

        ''' Read the 5G dataset to add at 
        client object the communications conditions. '''    
        df  = pd.read_csv(datapath)
        self.dataframe = df[df['Node ID'] == client_id].reset_index()
        self.state = 0 # indicates the dataset line used to calculate the delay
        self.model_size = model_size
        self.message_period = message_period
        self.client_id = client_id
        self.server = server
        self.epoch = 0
        self.time_last_chunk = 0.0
        self.computation_delay = [ 0 for i in range(n_epochs)] # in seconds
        self.logger = logging.getLogger("client_"+str(client_id))
        logging.basicConfig(filename="logs/client.log",encoding='utf-8', level=logging.DEBUG)
        

    def set_server(self, server):
        self.server = server  

    ''' Updates client's positions and 
        communications conditions. '''
    def update_state(self):
        self.state+=1

    def set_state(self, state):
        self.state = int(state)
    
    ''' Determines the delay giving the throughput. '''
    def get_delay(self):
        pass
    
    ''' Sends the maximum data as possible during the 100ms. '''
    def send_data_chunk(self, data):
        
        maximum_chunk_size = floor(self.message_period * 1000 * 
                                   self.dataframe['Throughput UL'].iloc[self.state])
                
        if (maximum_chunk_size >= data):
            self.time_last_chunk = data/(1000 * 
                                         self.dataframe['Throughput UL'].iloc[self.state])
                                         
            return 0 # no more data to send
        
        return data - maximum_chunk_size # remain data to send

    # need to implement the trianing part
    def local_training(self):
        self.set_state(self.state + (self.computation_delay[self.epoch]/
                                     self.message_period))

    ''' Sends the model to the aggregation server. '''
    def send_model(self):
        
        initial_time = self.state

        remain_data = self.model_size

        self.logger.debug("sending model to server %s", self.server)
        
        while (remain_data):
            
            self.logger.debug("client ID: %d, state: %d", self.client_id, self.state)
            remain_data = self.send_data_chunk(remain_data)
            
            if remain_data:
                self.update_state()

        self.logger.debug("state: %d" % self.state)
        self.logger.debug("initial state %d" % initial_time)
        self.logger.debug("last chunck: %f" % float(self.time_last_chunk))
        self.logger.debug("time to send the model: %f" % 
                          float(0.1 * (self.state + self.time_last_chunk - initial_time)))

        if self.server is not None:
            self.server.update_received_models()
            self.server.set_highest_delay(float(0.1 * (self.state + 
                                                       self.time_last_chunk - 
                                                       initial_time)))
            self.server.set_server_state(self.state)

    def receive_data_chunk(self,data):
        maximum_chunk_size = floor(self.message_period * 
                                   1000 * 
                                   self.dataframe['Throughput DL'].iloc[self.state])
                
        if (maximum_chunk_size >= data):
            self.time_last_chunk = data/(1000 * 
                                         self.dataframe['Throughput DL'].iloc[self.state])
            return 0 # no more data to send
        return data - maximum_chunk_size # remain data to send


    def receive_model(self):

        initial_time = self.state

        remain_data = self.model_size

        self.logger.debug("receiving model %s" % self.server)
        
        while (remain_data):
            self.logger.debug("client ID: %d state: %d",
                              self.client_id, self.state)
            
            remain_data = self.receive_data_chunk(remain_data)
            
            if remain_data:
                self.update_state()

        # final time
        self.logger.debug("time to receive the model: %f" % 
                          float(0.1 * (self.state + 
                                       self.time_last_chunk - 
                                       initial_time)))
        ''' training '''
        self.local_training()

        ''' send model back to the server '''
        self.send_model()
        


''' Class test '''    

if __name__ == '__main__':
    client = Client()
    client.receive_model()
    client.send_model()
    


