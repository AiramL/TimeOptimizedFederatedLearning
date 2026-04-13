from .m_fastest import ServerMFastestSelection
from .tofl_selection_dl import ServerEstimatorTOFLSelectionDL

class ServerEstimatorTOFLSelectionMFastest(ServerEstimatorTOFLSelectionDL):

    def __init__(self,
                 m_clients=2,
                 **kwargs):

        super().__init__(**kwargs)

        self.server_name = "tofl_mfastest"

        if m_clients > self.number_of_clients_to_select:
            
            # Invalid Number
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



class ServerEstimatorTOFLSelectionMFastestClients(ServerEstimatorTOFLSelectionDL):

    def __init__(self,
                 m_clients=2,
                 **kwargs):

        super().__init__(**kwargs)

        self.server_name = "tofl_mfastest"

        if m_clients > self.number_of_clients_to_select:
            
            # Invalid Number
            raise Exception

        self.m_clients = m_clients
    
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
    

