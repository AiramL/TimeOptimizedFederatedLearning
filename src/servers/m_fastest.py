import random

from .server import Server

class ServerMFastestSelection(Server):

    def __init__(self, 
                 m_clients=2, 
                 **kwargs):
        
        super().__init__(**kwargs)

        self.m_clients = m_clients
        
        self.server_name = "m_fastest"

        if m_clients > self.number_of_clients_to_select:
            
            # Invalid Number
            raise Exception

    def select_clients(self):

        self.selected_clients = random.sample(range(len(self.available_clients)),
                                              self.number_of_clients_to_select)

    def set_highest_delay(self,
                          delay):

        self.logger.debug("client delay: %f" % delay)
        self.logger.debug("highest delay: %f" % self.highest_delay) 
        self.logger.debug(f"m_clients_delays list: {self.m_clients_delays}") 
        self.m_clients_delays.append(delay)
        
        if len(self.m_clients_delays) > 1:
            
            self.m_clients_delays.sort() 
        
        if (self.num_received_models == self.number_of_clients_to_select):
        
            self.highest_delay = self.m_clients_delays[self.m_clients-1]
            self.logger.debug("highest delay: %f" % self.highest_delay) 
    
    #def set_server_state(self,
    #                     state, 
    #                     elapsed_time):
    #    
    #    self.m_clients_states.append(int(elapsed_time))
    #    
    #    if len(self.m_clients_states) > 1:
    #        
    #        self.m_clients_states.sort()
    #
    #    if (self.num_received_models == self.number_of_clients_to_select):
    #        
    #        self.highest_delay = self.m_clients_states[self.m_clients-1]
    #        self.state = self.m_clients_states[self.m_clients-1]

