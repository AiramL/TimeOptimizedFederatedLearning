import pandas as pd

from math import floor

class Client(object):

    def __init__(self, 
                 node_id=0, 
                 model_size=527000, 
                 message_period=0.1,
                 client_id=1,
                 server=None,
                 datapath='executions/v2x_simulation_results1.csv'):
        
        df  = pd.read_csv(datapath)
        self.dataframe = df[df['Node ID'] == node_id].reset_index()
        self.state = 0 # indicates the dataset line used to calculate the delay
        self.model_size = model_size
        self.message_period = message_period
        self.client_id = client_id
        self.server = server
        self.epoch = 0

    def set_server(self, server):
        self.server = server
        

    def print_dataframe(self):
        print(self.dataframe)

    ''' Reads the 5G dataset to add at 
        client object the communications conditions. '''
    def read_communication_data(self):
        pass

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
            return 0 # no more data to send
        return data - maximum_chunk_size # remain data to send

    ''' Sends the model to the aggregation server. '''
    def send_model(self):
        initial_time = self.state

        remain_data = self.model_size

        while (remain_data):
            remain_data = self.send_data_chunk(remain_data)
            print(remain_data)
            self.update_state()
        # final time
        print(0.1 * (self.state - initial_time))

        self.server.set_state(self.state)

    def receive_data_chunk(self,data):
        maximum_chunk_size = floor(self.message_period * 1000 * self.dataframe['Throughput UD'].iloc[[self.state]])
                
        if (maximum_chunk_size >= data):
            return 0 # no more data to send
        return data - maximum_chunk_size # remain data to send


    def receive_model(self):
        initial_time = self.state

        remain_data = self.model_size

        while (remain_data):
            remain_data = self.receive_data_chunk(remain_data)
            print(remain_data)
            self.update_state()

        # final time
        print(0.1 * (self.state - initial_time))

        self.server.set_state(self.state)

        ''' local training '''

        ''' send model back to the server '''
        self.send_model()
        
''' Class test '''    

if __name__ == '__main__':
    client = Client()
    client.print_dataframe()
    client.send_model()


