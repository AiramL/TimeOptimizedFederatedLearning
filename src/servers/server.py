from abc import (
    ABC,
    abstractmethod)

from pickle import dump

from utils.utils import create_logger

class Server(ABC):

    def __init__(self,
                 n_select_clients=5,
                 n_rounds=10,
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
                 timeout=120,
                 base_station_range=2000,
                 speed=2):
        
        self.available_clients = avalilable_clients
        self.selected_clients = []
        self.epochs_delays = []
        self.m_clients_delays = []
        self.m_clients_states = []
        self.model_size = model_size
        self.number_of_clients_to_select = n_select_clients
        self.number_of_epochs = n_rounds
        self.message_period = 0.1
        self.state = 0
        self.epoch = 0
        self.num_received_models = 0
        self.highest_delay = 0.0
        self.file_name = file_name
        self.SAVE =  False
        self.clients_computation_delay = [ 0 for i in range(n_rounds)] # in seconds
        self.server_name = ""
        self.timeout = timeout
        self.elapsed_time = 0
        self.epoch_begging = 0.0
        self.base_station_range = base_station_range
        self.speed = speed
        self.server_name = "abstract"    
    
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

        if( len(self.selected_clients) - self.num_received_models ):
        
            self.logger.debug("model received")

        else:
            
            self.logger.debug("model not received")
        
    def save(self,
             results):

        with open(self.file_name,"wb") as writer:
        
            dump(results,writer)

    def train(self):
        
        self.logger = create_logger("logs/",
                                    self.server_name)


        if self.number_of_clients_to_select > len(self.available_clients.keys()):
        
            self.logger.error("Invalid configuration. Number of clients to select greater than number of available clients")
            
            raise Exception

        while(self.epoch < self.number_of_epochs+1):
            
            self.set_clients_state()
            self.highest_delay = 0.0
            self.elapsed_time = 0    
            self.m_clients_delays = []
            self.m_clients_states = []
            
            self.logger.debug("starting global epoch at state: %d" % self.state)
            self.logger.debug("global epoch: %d" % self.epoch)

            ''' update delays '''
            self.update_past_delays()

            ''' select clients '''
            self.select_clients()             

            with open(f"results/selected_clients/speed{self.speed}/{self.base_station_range}/{self.server_name}_epoch_{self.epoch}","wb") as writer:

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

    def set_highest_delay(self,
                          delay):

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

    def set_server_state(self, 
                         state,
                         elapsed_time):

        if elapsed_time >= self.elapsed_time:
                
                self.elapsed_time = elapsed_time
                self.state = int(state)
    
    def set_clients_state(self):
        
        for client in self.available_clients.values():
            
            client.set_state(self.state)
