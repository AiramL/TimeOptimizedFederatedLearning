from abc import ABC
from abc import abstractmethod
from train_model import LSTM
import torch

class Estimator(ABC):

    def __init__(self,model):
        self.data = []
        self.model = model

    @abstractmethod
    def predict(self):
        pass

    def set_data(self,data):
        self.data = data

    def set_predictor(self,model):
        self.model = model

class EstimatorLSTM(Estimator):
    def __init__(self,model_path="models/model_10.pt"):
        
        model = LSTM()

        model.load_state_dict(torch.load(model_path, weights_only=True))

        super().__init__(model)

    def predict(self,data):
        return float(self.model(data)[-1])

class EstimatorARIMA(Estimator):
    
    def __init__(self):
        #super().__init__(ARIMA)
        pass

    def predict(self):
        prediction = self.model.predict()
        return prediction
