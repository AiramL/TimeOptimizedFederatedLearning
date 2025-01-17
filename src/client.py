import pandas as pd

''' add logging '''
from math import floor

class Client(object):

    def __init__(self,  
                 model_size=5270, # in kB
                 message_period=0.1, # in seconds
                 client_id=1,
                 server=None,
                 datapath='executions/mean_tp.csv'): 

        ''' Read the 5G dataset to add at 
        client object the communications conditions. '''    
        df  = pd.read_csv(datapath)
        self.dataframe = df[df['Node ID'] == client_id].reset_index()
        self.print_dataframe()
        self.state = 0 # indicates the dataset line used to calculate the delay
        self.model_size = model_size
        self.message_period = message_period
        self.client_id = client_id
        self.server = server
        self.epoch = 0
        self.time_last_chunk = 0.0

    def set_server(self, server):
        self.server = server

    def print_dataframe(self):
        print(self.dataframe)  

    ''' Updates client's positions and 
        communications conditions. '''
    def update_state(self):
        self.state+=1
    
    def set_state(self, state):
        self.state = state
    
    ''' Determines the delay giving the throughput. '''
    def get_delay(self):
        pass
    
    ''' Sends the maximum data as possible during the 100ms. '''
    def send_data_chunk(self, data):
        
        maximum_chunk_size = floor(self.message_period * 1000 * self.dataframe['Throughput UL'].iloc[[self.state]])
                
        if (maximum_chunk_size >= data):
            self.time_last_chunk = data/(1000 * self.dataframe['Throughput UL'].iloc[[self.state]])
            return 0 # no more data to send
        return data - maximum_chunk_size # remain data to send

    ''' Sends the model to the aggregation server. '''
    def send_model(self):

        initial_time = self.state

        remain_data = self.model_size

        print("sending model")
        print(self.server)
        while (remain_data):
            
            print("client ID: ", self.client_id, "state: ", self.state)
            remain_data = self.send_data_chunk(remain_data)
            #print(remain_data)
            
            self.update_state()

        # final time
        print(0.1 * (self.state + self.time_last_chunk - initial_time))
        print(self.state)

        if self.server is not None:
            self.server.update_received_models()
            self.server.set_server_state(self.state)
            print("state: ", self.state)
            print("initial state", initial_time)
            print("last chunck: ", float(self.time_last_chunk))
            self.server.set_highest_delay(float(0.1 * (self.state + self.time_last_chunk - initial_time)))

    def receive_data_chunk(self,data):
        maximum_chunk_size = floor(self.message_period * 1000 * self.dataframe['Throughput DL'].iloc[[self.state]])
                
        if (maximum_chunk_size >= data):
            self.time_last_chunk = data/(1000 * self.dataframe['Throughput DL'].iloc[[self.state]])
            return 0 # no more data to send
        return data - maximum_chunk_size # remain data to send


    def receive_model(self):
        initial_time = self.state

        remain_data = self.model_size

        print("receiving model")
        print(self.server)
        while (remain_data):
            print("client ID: ", self.client_id, "state: ", self.state)
            remain_data = self.receive_data_chunk(remain_data)
            #print(remain_data)
            self.update_state()
            print(self.state)

        # final time
        print(0.1 * (self.state + self.time_last_chunk - initial_time))

        if self.server is not None:
            self.server.set_server_state(self.state)

        ''' local training '''

        ''' send model back to the server '''
        self.send_model()
        
''' Class test '''    

if __name__ == '__main__':
    client = Client()
    client.print_dataframe()
    client.send_model()
    client.receive_model()


