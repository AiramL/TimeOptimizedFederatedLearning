from abc import ABC 
from abc import abstractmethod
from pickle import dump
from pickle import load
import random
from time import sleep
import pandas as pd
from math import floor
from utils.estimator.architecture import *
import logging
from collections import deque

class Server(ABC):

    def __init__(self,
                 n_select_clients=5,
                 n_epochs=10,
                 file_name="result",
                 model_size=527,
                 avalilable_clients={"1":1,
                                     "2":2,
                                     "3":3,
                                     "4":4,
                                     "5":5,
                                     "6":6,
                                     "7":7,
                                     "8":8,
                                     "9":9,
                                     "0":0,},
                 timeout=120):
        
        self.available_clients = avalilable_clients
        self.selected_clients = []
        self.epochs_delays = []
        self.m_clients_delays = []
        self.m_clients_states = []
        self.model_size = model_size
        self.number_of_clients_to_select = n_select_clients
        self.number_of_epochs = n_epochs
        self.message_period = 0.1
        self.state = 0
        self.epoch = 0
        self.num_received_models = 0
        self.highest_delay = 0.0
        self.file_name = file_name
        self.SAVE =  False
        self.clients_computation_delay = [ 0 for i in range(n_epochs)] # in secondsi
        self.server_name = ""
        self.timeout = timeout
        self.epoch_begging = 0.0
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename="logs/server.log",encoding='utf-8', level=logging.CRITICAL)
        
        
        if n_select_clients > len(avalilable_clients.keys()):
            self.logger.error("Invalid configuration. Number of clients to select greater than number of available clients")
            raise Exception

    
    @abstractmethod
    def select_clients(self):
        pass
    
    ''' used only in TOFL estimator '''
    def update_past_delays(self):
        pass

    def send_model(self):
        for client_id in self.selected_clients:
            self.available_clients[str(client_id)].receive_model()

    def receive_models(self):
        if(len(self.selected_clients)-self.num_received_models):
            self.logger.debug("model received")
        else:
            self.logger.debug("model not received")
        
    def save(self,results):
        with open(self.file_name,"wb") as writer:
            dump(results,writer)

    def train(self):
        
        while(self.epoch < self.number_of_epochs+1):
            
            self.set_clients_state()
            self.highest_delay = 0.0
            
            self.m_clients_delays = []
            self.m_clients_states = []
            
            self.logger.debug("starting global epoch at state: %d" % self.state)
            self.logger.debug("global epoch: %d" % self.epoch)

            ''' update delays '''
            self.update_past_delays()

            ''' select clients '''
            self.select_clients()             

            with open("results/selected_clients/"+self.server_name+"epoch"+str(self.epoch),"wb") as writer:
                dump(self.selected_clients , writer)

            ''' send model to the clients '''
            self.send_model()

            ''' receive models from clients '''
            self.num_received_models = 0
            self.receive_models()

            self.epochs_delays.append(self.highest_delay)            

            self.logger.debug("server state: %d", self.state)
                
            ''' update epoch '''
            self.update_epoch()
        
        ''' total delay '''
        self.logger.info(self.calculate_total_delay())

        ''' save result '''
        self.save(self.epochs_delays)

        ''' return the total delay '''
        return self.calculate_total_delay()

    def set_highest_delay(self,delay):
        self.logger.debug("client delay: %f" % delay)
        self.logger.debug("highest delay: %f" % self.highest_delay)
        if delay > self.highest_delay:
            self.highest_delay = delay
    
    def calculate_total_delay(self):
        
        return sum(self.epochs_delays)

    def update_epoch(self):
        
        self.epoch+=1

    def update_received_models(self):
        
        self.num_received_models+=1
        self.logger.debug("number of received models updated: %d" % self.num_received_models)
        models_to_receive = len(self.selected_clients) - self.num_received_models
        self.logger.debug("number of models to be received: %d" % models_to_receive)

    def set_server_state(self, state):

        if state > self.state:
           
            self.state = int(state)
    
    def set_clients_state(self):
        
        for client in self.available_clients.values():
            
            client.set_state(self.state)

class ServerRandomSelection(Server):

    def __init__(self, 
                 *args,
                 **kwargs):

        super().__init__(*args,
                         **kwargs)
 
        self.server_name = "random"

    def select_clients(self):

        self.selected_clients = random.sample(range(len(self.available_clients)),
                                              self.number_of_clients_to_select)

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

class ServerMFastestSelection(Server):
    def __init__(self, 
                 n_select_clients=5, 
                 n_epochs=10, 
                 file_name="result", 
                 model_size=527,
                 m_clients=2, 
                 avalilable_clients={ "1": 1,
                                      "2": 2,
                                      "3": 3,
                                      "4": 4,
                                      "5": 5,
                                      "6": 6,
                                      "7": 7,
                                      "8": 8,
                                      "9": 9,
                                      "0": 0 }):
        
        super().__init__(n_select_clients, 
                         n_epochs, 
                         file_name, 
                         model_size, 
                         avalilable_clients)

        self.m_clients = m_clients

        
        self.server_name = "m_fastest"

        if m_clients > n_select_clients:
            self.logger.error("Invalid configuration. Number of m_clients \
                               greater than number of clients to select")
            raise Exception

    def select_clients(self):
        self.selected_clients = random.sample(range(len(self.available_clients)),
                                              self.number_of_clients_to_select)

    def set_highest_delay(self,delay):
        self.logger.debug("client delay: %f" % delay)
        self.logger.debug("highest delay: %f" % self.highest_delay)
        
        self.m_clients_delays.append(delay)
        
        if len(self.m_clients_delays) > 1:
            self.m_clients_delays.sort() 
        
        if (self.num_received_models == self.number_of_clients_to_select):
            self.highest_delay = self.m_clients_delays[self.m_clients-1]
    
    def set_server_state(self, state):
        
        self.m_clients_states.append(int(state))
        
        if len(self.m_clients_states) > 1:
            
            self.m_clients_states.sort()

        if (self.num_received_models == self.number_of_clients_to_select):
            
            self.state = self.m_clients_states[self.m_clients-1]


class ServerTOFLSelection(Server, ABC):

    def __init__(self, 
                 n_select_clients=5, 
                 n_epochs=10, 
                 file_name="result", 
                 model_size=527, 
                 avalilable_clients={ "1": 1,
                                      "2": 2,
                                      "3": 3,
                                      "4": 4,
                                      "5": 5,
                                      "6": 6,
                                      "7": 7,
                                      "8": 8,
                                      "9": 9,
                                      "0": 0 },
                datapath="data/processed/v2x_mobility_0_mean.csv"):

        super().__init__(n_select_clients, 
                         n_epochs, 
                         file_name, 
                         model_size, 
                         avalilable_clients)

        self.past_delays = { client_id : (deque(10*[100],10),
                                          deque(10*[100],10))
                                         for client_id in 
                                         self.available_clients.keys() }

        self.clients_estimated_delays = { client_id : 100.0
                                         for client_id in 
                                         self.available_clients.keys() }
    

        self.dataframe = datapath 
        self.logger.debug("loading data")
        
        self.clients_info = { str(client_id): self.dataframe[
                                self.dataframe['Node ID'] == int(client_id)].reset_index() 
                                for client_id in 
                                avalilable_clients.keys() }
        
        
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
    
class ServerOracleTOFLSelection(ServerTOFLSelection):

    def __init__(self, 
                 n_select_clients=5, 
                 n_epochs=10, 
                 file_name="result", 
                 model_size=527, 
                 avalilable_clients={ "1": 1,
                                      "2": 2,
                                      "3": 3,
                                      "4": 4,
                                      "5": 5,
                                      "6": 6,
                                      "7": 7,
                                      "8": 8,
                                      "9": 9,
                                      "0": 0 },
                 datapath="data/processed/0.csv"):
        
        super().__init__(n_select_clients, 
                         n_epochs, 
                         file_name, 
                         model_size, 
                         avalilable_clients,
                         datapath)


        self.computational_delays = []
        self.estimated_state = 0

        self.server_name = "tofl_oracle"
                                
        self.logger.debug("finished loading data")
        if n_select_clients > len(self.dataframe['Node ID'].unique()):
            self.logger.error("Invalid number of clients to be selected, \
                               higher than the total available number of clients.")
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
                    
            state = 0 
        
        while (remain_data):

            remain_data, _ = self.receive_data_chunk(remain_data, client_id, state)
            
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
                    
            state = 0 
        
        while (remain_data):
        
            remain_data, time_last_chunk = self.send_data_chunk(remain_data, client_id, state)
            
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



class ServerEstimatorTOFLSelectionDL(ServerTOFLSelection):

    def __init__(self, 
                 n_select_clients=5, 
                 n_epochs=10, 
                 file_name="result", 
                 model_size=527, 
                 avalilable_clients={"1": 1,
                                     "2": 2,
                                     "3": 3,
                                     "4": 4,
                                     "5": 5,
                                     "6": 6,
                                     "7": 7,
                                     "8": 8,
                                     "9": 9,
                                     "0": 0 },
                 datapath="data/processed/v2x_mobility_0_mean.csv"):
        
        super().__init__(n_select_clients, 
                         n_epochs, 
                         file_name, 
                         model_size, 
                         avalilable_clients,
                         datapath)

        self.estimator = EstimatorLSTM()
        
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
            self.logger.debug("remaining %d state:data:  %d", remaining_data, self.state)
        
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


class ServerEstimatorTOFLSelectionMFastest(ServerEstimatorTOFLSelectionDL):

    def __init__(self,
                 n_select_clients=5,
                 m_clients=2,
                 n_epochs=10,
                 file_name="result",
                 model_size=527,
                 avalilable_clients={"1": 1,
                                     "2": 2,
                                     "3": 3,
                                     "4": 4,
                                     "5": 5,
                                     "6": 6,
                                     "7": 7,
                                     "8": 8,
                                     "9": 9,
                                     "0": 0 },
                 datapath="data/processed/v2x_mobility_0_mean.csv"):

        super().__init__(n_select_clients,
                         n_epochs,
                         file_name,
                         model_size,
                         avalilable_clients,
                         datapath)
        
        self.server_name = "tofl_mfastest"

        if m_clients > n_select_clients:
            self.logger.error("Invalid configuration. Number of m_clients \
                               greater than number of clients to select")
            raise Exception

        self.m_clients = m_clients

    def select_clients(self):

        selected_clients = []

        total_estimated_delay = []

        self.estimate_delay()

        for client, delay in self.clients_estimated_delays.items():
            total_estimated_delay.append((delay,client))
            total_estimated_delay.sort()

        num_selected_clients = 0
        while num_selected_clients < self.m_clients:
            selected_clients.append(int(total_estimated_delay[
                                    num_selected_clients][1]))

            num_selected_clients+=1

        self.selected_clients = selected_clients
    

if __name__ == "__main__":

    # testing random selection
    #server = ServerRandomSelection()

    for i in range(2,11):
        #server = ServerOracleTOFLSelection(n_select_clients=i)
        server = ServerEstimatorTOFLSelectionDL(n_select_clients=i)
        server.select_clients()
        print(server.selected_clients)
