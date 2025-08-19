import pandas as pd
import argparse
import tensorflow as tf

from os import mkdir

from .dataset_operations import *

def get_args_client():
    parser = argparse.ArgumentParser()

    parser.add_argument("-sip","--server_ip", type=str, default="[::]", help="Server IP address")
    parser.add_argument("-sp","--server_port", type=str, default="8080", help="Server TCP port")
    parser.add_argument("-b","--batch_size", type=int, default=32, help="Batch size to use during the federated learning training")
    parser.add_argument("-ts","--test_size", type=float, default=0.2, help="Test size to use")
    parser.add_argument("-s","--subset_size", type=int, default=100, help="Number of samples to use during the federated learning training")
    parser.add_argument("-nle","--number_of_local_epochs", type=int, default=5, help="How many updates the client does before sending the updated model to the server")
    parser.add_argument("-dp","--data_path", type=str, default="datasets/VeReMi_Extension/mixalldata_clean.csv", help="Path to the data")
    parser.add_argument("-dsp","--dataset_path", type=str, default="datasets/VeReMi_Extension", help="Dataset directory")
    parser.add_argument("-mp","--model_path", type=str, default="models/model", help="Path to the model")
    parser.add_argument("-cid","--client_id", type=int, default=1, help="Client identifier") 
    parser.add_argument("-rp","--result_path", type=str, default="results/", help="Path to store results")
    parser.add_argument("-imf","--image_flag", type=bool, default=False, help="Indicates the type of data")
    parser.add_argument("-md","--model", type=str, default="BIGAN", help="Model name to use in the FL scenario")
    parser.add_argument("-ds","--dataset", type=str, default="VeReMi", help="Dataset name")
    parser.add_argument("-cf","--communication_flag", type=int, default=0, help="Flag to indicate if the clients will simulate the communication delay")
    parser.add_argument("-nc","--num_clients", type=int, default=10, help="How many clients are present during the training")
    parser.add_argument("-ncf","--num_clients_fit", type=int, default=10, help="How many clients fits the model")
    
    return parser.parse_args()

def get_args_server():
    parser = argparse.ArgumentParser()

    parser.add_argument("-sip","--server_ip", type=str, default="[::]", help="Server IP address")
    parser.add_argument("-sp","--server_port", type=str, default="8080", help="Server TCP port")
    parser.add_argument("-nor","--number_of_rounds", type=int, default=3, help="How many global epochs the server executes")
    parser.add_argument("-nc","--num_clients", type=int, default=10, help="How many clients are present during the training")
    parser.add_argument("-ncf","--num_clients_fit", type=int, default=10, help="How many clients fits the model")
    parser.add_argument("-tf","--tofl_flag", type=int, default=1, help="Flag to indicate if the server uses our proposed strategy")
    
    return parser.parse_args()

def generate_pre_processed_dataset(DATA_PATH,DATASET_PATH):
    # Load dataset
    df = load_dataset_to_dataframe(DATA_PATH)


    # Pre-process data by removing highly correlated features
    corr_matrix = df.corr()
    remove_nan_features_corr(df,corr_matrix)

    col = 'class'

    X = df.loc[:,df.columns != col]
    y = df.loc[:,df.columns == col]
    
    # Aplply one-hot ecoding
    Y = pd.get_dummies(y, columns=['class',])

    # Create directory
    mkdir(DATASET_PATH+"/pre_processed")

    # Save dataset
    with open(DATASET_PATH+"/pre_processed/features","wb") as writer:
        dump(X,writer)

    with open(DATASET_PATH+"/pre_processed/labels","wb") as writer:
        dump(Y,writer)

    return 0





if __name__ == "__main__":
    generate_pre_processed_dataset('datasets/VeReMi_Extension/mixalldata_clean.csv','datasets/VeReMi_Extension')
