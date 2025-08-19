from timeit import default_timer as timer
import flwr as fl
import tensorflow as tf
from datetime import datetime

from sklearn.model_selection import train_test_split

from os import listdir
from time import sleep
from sys import path

from utils.dataset_operations import *
from utils.models import build_model 
from utils.utils import *
from utils.load_federated_data import *

# Get parameters
args = get_args_client()

# Set Parameters
client_id = args.client_id
n_local_epochs = args.number_of_local_epochs
ss = args.subset_size
bs = args.batch_size
ts = args.test_size
SERVER_IP = args.server_ip
SERVER_PORT = args.server_port
DATA_PATH = args.data_path
DATASET_PATH = args.dataset_path
DATASET = args.dataset
MODEL_PATH = args.model_path
RESULT_PATH = args.result_path
IMAGE_DATA = args.image_flag
MODEL = args.model
COMMUNICATION_FLAG = args.communication_flag
num_clients = args.num_clients
num_selected_clients = args.num_clients_fit

SAVE_COMPUTATIONAL_TIME = False

# Load delays
if COMMUNICATION_FLAG:
    if client_id < 10:
        delays = pd.read_csv("../delays/client0"+str(client_id), header=None)
    else:
        delays = pd.read_csv("../delays/client"+str(client_id), header=None)

# Load data
if IMAGE_DATA:
    print("Training with CIFAR-10")
    trPer=0.8
    x_train, y_train, x_test, y_test = load_data_federated_IID("CIFAR-10", 
                                                               client_id, 
                                                               num_clients, 
                                                               trPer)

    # Defining the deep learning model
    model = tf.keras.applications.MobileNet((32, 32, 3), 
                                             classes=10,
                                             weights=None)
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  loss='sparse_categorical_crossentropy',
                  metrics=['sparse_categorical_accuracy'])

# Intrusion Detection in CAMs
else:
    # define DATASET and test_size
    x_train, x_test, y_train, y_test = load_CAM_data_federated(DATASET,ts)
    
    spe = len(x_train)//bs


    # Defining the deep learning model
    model = build_model(x_train.shape[1:][1],y_train.shape[1:][0],MODEL)

# Federated Learning client
class FLClient(fl.client.NumPyClient):

    def __init__(self, *args, **kwargs):
        super(fl.client.NumPyClient, self).__init__(*args, **kwargs)
        self.global_epoch = 0

    def update_global_epoch(self):
        self.global_epoch += 1

    def get_parameters(self,config):
        return model.get_weights()

    def fit(self, parameters, config):
        
        # Simulate the download delay
        if COMMUNICATION_FLAG:
            sleep(delays[0][self.global_epoch])

        # Start timer to determine the computational time
        fit_start = timer()

        model.set_weights(parameters)
        model.fit(x_train, y_train, epochs=n_local_epochs, batch_size=bs)
        tsp = datetime.now()
        timestamp = tsp.strftime('%Y-%m-%d-%H:%M:%S')
        model.save('../../models/vnc_local_model_client'+str(client_id)+'_n_clients_'+str(num_selected_clients)+'_epoch_'+str(self.global_epoch)+"_"+str(timestamp)+'.keras')
        
        # Determine client's computational time 
        computational_time = timer() - fit_start
        
        if SAVE_COMPUTATIONAL_TIME:
            # Calculating the total local training time
            append_text(RESULT_PATH+"subset_size_"+str(ss)+
                        "/client_"+str(client_id),
                        str(computational_time)+
                        "\n")
        
        # Simulate the upload delay
        if COMMUNICATION_FLAG:
            sleep(delays[2][self.global_epoch])

        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test)

        ''' Since all clients are selected to evaluate, we guaratee
            that each client knows the current global epoch number,
            to correctly read the delays' file input ''' 
        
        self.update_global_epoch()
        
        if client_id == 1:
            model.save('../../models/vnc_model.keras')
            tsp = datetime.now()
            timestamp = tsp.strftime('%Y-%m-%d-%H:%M:%S')
            model.save('../../models/vnc_n_clients_'+str(num_selected_clients)+'_epoch_'+str(self.global_epoch)+"_"+str(timestamp)+'.keras')

        return loss, len(x_test), {"accuracy": float(accuracy)}


fl.client.start_client(server_address=SERVER_IP+":"+SERVER_PORT, client=FLClient().to_client())
