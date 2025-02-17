#
# Author: Lucas Airam Castro de Souza
# Laboratory: Grupo de Teleinformatica e Automacao (GTA)
# University: Universidade Federal do Rio de Janeiro (UFRJ)
#

import numpy as np
import pandas as pd
import scipy.io as scio

from skimage import transform
from pickle import load, dump
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import StratifiedKFold

def load_data_federated_IID(dataset_name,clientID,numClients,trPer):

    X = np.array([],dtype=np.float32)
    Y = np.array([],dtype=np.float32)

    for i in range(0,10):
        X_train_current = np.array([],dtype=np.float32)
        Y_train_current = np.array([],dtype=np.float32)
        X_test_current = np.array([],dtype=np.float32)
        Y_test_current = np.array([],dtype=np.float32)

        X_train_current = np.asarray(load(open('../../datasets/'+
            dataset_name+'/class'+str(i)+'Train','rb')), dtype=np.float32)
        
        X_test_current = np.asarray(load(open('../../datasets/'+
            dataset_name+'/class'+str(i)+'Test','rb')), dtype=np.float32)

        Y_train_current = np.asarray(load(open('../../datasets/'+
            dataset_name+'/class'+str(i)+'TrainLabel','rb')), dtype=np.float32)


        Y_test_current = np.asarray(load(open('../../datasets/'+
            dataset_name+'/class'+str(i)+'TestLabel','rb')),dtype=np.float32)

        begin_slice_train = int(len(Y_train_current)/numClients*(clientID-1))
        end_slice_train = int(len(Y_train_current)/numClients*clientID)
        begin_slice_test = int(len(Y_test_current)/numClients*(clientID-1))
        end_slice_test = int(len(Y_test_current)/numClients*clientID)

        X_train_current = X_train_current[begin_slice_train:end_slice_train]
        Y_train_current = Y_train_current[begin_slice_train:end_slice_train]
        X_test_current = X_test_current[begin_slice_test:end_slice_test]
        Y_test_current = Y_test_current[begin_slice_test:end_slice_test]
   
        if len(X) == 0:
            X = np.concatenate((X_train_current,X_test_current))
            Y = np.concatenate((Y_train_current,Y_test_current))
        else:
            X = np.concatenate((X,X_train_current,X_test_current))
            Y = np.concatenate((Y,Y_train_current,Y_test_current))
   
    # normalize the data
    X /= 255 

    # reshape MNIST and FMNIST
    if dataset_name == "MNIST" or dataset_name == "FMNIST":
        X = transform.resize(X, (len(X), 32, 32, 1))

    X, Y = shuffle(X, Y, random_state=47527)
    
    trSize = int(len(X)*trPer)
    
    return X[:trSize], Y[:trSize], X[trSize:], Y[trSize:]

def create_time_series(group, features, label_col,sequence_length):
    X, y = [], []
    group = group[features + [label_col]].values  # Convert to NumPy array

    if len(group) < sequence_length:
        return None  # Skip senders with insufficient data

    # Create sliding window sequences
    for i in range(len(group) - sequence_length):
        X.append(group[i:i+sequence_length, :-1])  # Features
        y.append(group[i+sequence_length, -1])  # Label

    X, y = np.array(X), np.array(y)

    # Ensure correct dimensions: X should be 3D, y should be 1D
    if X.ndim != 3 or y.ndim != 1:
        return None  # Skip malformed sequences

    return X, y

def load_CAM_data_federated(DATASET="VeReMi",test_size=0.2):
    
    # Need to implement the VeRemi data transformation
    if DATASET == "VeReMi":
        # Load dataset
        df = pd.read_csv('../../datasets/VeReMi_Extension/mixalldata_clean.csv')

        # Sort by sender and timestamp
        df.sort_values(["sender", "messageID"], inplace=True)

        # Define features
        features = ['posx', 
                    'posy', 
                    'posx_n', 
                    'spdx', 
                    'spdy', 
                    'spdx_n',
                    'spdy_n', 
                    'aclx', 
                    'acly', 
                    'aclx_n', 
                    'acly_n', 
                    'hedx', 
                    'hedy', 
                    'hedx_n',
                    'hedy_n'] 


        label_col = "class"

        # Normalize features
        scaler = StandardScaler()
        df[features] = scaler.fit_transform(df[features])

        # Encode labels
        df[label_col] = df[label_col].astype("category").cat.codes

        # Group by sender_id
        grouped = df.groupby("sender")

        sequence_length = 10

        # Apply function to all sender groups
        X_y_pairs = [create_time_series(group, features, label_col, sequence_length) for _, group in grouped]

        # Remove None values (senders with insufficient data)
        X_y_pairs = [pair for pair in X_y_pairs if pair is not None]

        # Ensure valid unpacking
        if len(X_y_pairs) > 0:
            X_list, y_list = zip(*X_y_pairs)  # Unpack
            X = np.concatenate(X_list, axis=0)  # Convert to final shape
            y = np.concatenate(y_list, axis=0)
        else:
            raise ValueError("No valid sequences found! Reduce `sequence_length`.")

        y = to_categorical(y, num_classes=len(np.unique(y)))

        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.98, random_state=42, stratify=y)
        
        return x_train, x_test[:4096], y_train, y_test[:4096]

    elif DATASET == "WiSec":
        # Load dataset
        dataset_1 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack16withlabels.mat')
        dataset_2 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack1withlabels.mat')
        dataset_3 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack2withlabels.mat')
        dataset_4 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack4withlabels.mat')
        dataset_5 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack8withlabels.mat')
    
        # Pre-process
        header = ["type",
         "timeReceiver",
         "receiverID",
         "receiverXposition",
         "receiverYposition",
         "receiverZposition",
         "timeTransmitted",
         "senderID",
         "messageID",
         "senderXposition",
         "senderYposition",
         "senderZposition",
         "senderXvelocity",
         "senderYvelocity",
         "senderZvelocity",
         "rssi",
         "class"]

        # Join datasets
        df_dataset = pd.concat([pd.DataFrame(dataset_1['attack16withlabels']),
                                pd.DataFrame(dataset_2['attack1withlabels']),
                                pd.DataFrame(dataset_3['attack2withlabels']),
                                pd.DataFrame(dataset_4['attack4withlabels']),
                                pd.DataFrame(dataset_5['attack8withlabels'])])

        # Set column names
        df_dataset.columns = header

        # Drop idetifiers
        df_dataset = df_dataset.drop(['receiverID','senderID', 'messageID'], axis=1)
        
        # Drop missing values
        df_dataset = df_dataset.dropna()
        
        # Remove high correlated features
        features_nan_corr = ["receiverZposition",
                     "senderZposition",
                     "type",
                     "senderZvelocity",
                     "timeReceiver"]

        df_dataset = df_dataset.drop(columns=features_nan_corr)

        # Feature set
        X = df_dataset.drop(columns=['class'])
        columns_names = X.columns
        scaler = MinMaxScaler()
        scaler = scaler.fit(X)
        X = pd.DataFrame(scaler.transform(X))
        X.columns = columns_names
    
        # Label set
        y = df_dataset['class']
        y = pd.get_dummies(y,columns=['class'])

    x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.8,random_state=42)
    x_train = np.resize(x_train,(x_train.shape[0],1,x_train.shape[1]))
    x_test = np.resize(x_test,(x_test.shape[0],1,x_test.shape[1]))

    # Split dataset
    return x_train[:8192*4], x_test[:2048*4], y_train[:8192*4], y_test[:2048*4]


def load_CAM_data(client_id,datapath='../../datasets/processed/'):
    
    client_id -= 1

    dataset = "WiSec"
    
    with open(datapath+dataset+"_x_train"+str(client_id),"rb") as reader:
        x_train = load(reader)
    
    with open(datapath+dataset+"_x_test"+str(client_id),"rb") as reader:
        x_test = load(reader)

    with open(datapath+dataset+"_y_train"+str(client_id),"rb") as reader:
        y_train = load(reader)

    with open(datapath+dataset+"_y_test"+str(client_id),"rb") as reader:
        y_test = load(reader)
    
    return x_train, x_test, y_train, y_test


def generate_distribution_CAM(n_clients=20, dataset="WiSec"):
    
    datapath = '../datasets/processed/'

    sub_X_train = []
    sub_y_train = []
    
    sub_X_test = []
    sub_y_test = []
    
    if dataset == "WiSec":

        # Load dataset
        dataset_1 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack16withlabels.mat')
        dataset_2 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack1withlabels.mat')
        dataset_3 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack2withlabels.mat')
        dataset_4 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack4withlabels.mat')
        dataset_5 = scio.loadmat('../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack8withlabels.mat')

        # Pre-process
        header = ["type",
         "timeReceiver",
         "receiverID",
         "receiverXposition",
         "receiverYposition",
         "receiverZposition",
         "timeTransmitted",
         "senderID",
         "messageID",
         "senderXposition",
         "senderYposition",
         "senderZposition",
         "senderXvelocity",
         "senderYvelocity",
         "senderZvelocity",
         "rssi",
         "class"]

        # Join datasets
        df_dataset = pd.concat([pd.DataFrame(dataset_1['attack16withlabels']),
                                pd.DataFrame(dataset_2['attack1withlabels']),
                                pd.DataFrame(dataset_3['attack2withlabels']),
                                pd.DataFrame(dataset_4['attack4withlabels']),
                                pd.DataFrame(dataset_5['attack8withlabels'])])

        # Set column names
        df_dataset.columns = header

        # Drop idetifiers
        df_dataset = df_dataset.drop(['receiverID','senderID', 'messageID'], axis=1)
        
        # Drop missing values
        df_dataset = df_dataset.dropna()
        
        # Remove high correlated features
        features_nan_corr = ["receiverZposition",
                     "senderZposition",
                     "type",
                     "senderZvelocity",
                     "timeReceiver"]

        df_dataset = df_dataset.drop(columns=features_nan_corr)

        # Feature set
        X = df_dataset.drop(columns=['class'])
        columns_names = X.columns
        scaler = MinMaxScaler()
        scaler = scaler.fit(X)
        X = pd.DataFrame(scaler.transform(X))
        X.columns = columns_names

        # Label set
        y = df_dataset['class']
        y = pd.get_dummies(y,columns=['class'])
            
        X_train, x_test, Y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
        X_train = np.resize(X_train,(X_train.shape[0],1,X_train.shape[1]))
        x_test = np.resize(x_test,(x_test.shape[0],1,x_test.shape[1]))
    
    elif dataset == "VeReMi":

        # Load dataset
        df = pd.read_csv('../datasets/VeReMi_Extension/mixalldata_clean.csv')

        # Sort by sender and timestamp
        df.sort_values(["sender", "messageID"], inplace=True)

        # Define features
        features = ['posx', 
                    'posy', 
                    'posx_n', 
                    'spdx', 
                    'spdy', 
                    'spdx_n',
                    'spdy_n', 
                    'aclx', 
                    'acly', 
                    'aclx_n', 
                    'acly_n', 
                    'hedx', 
                    'hedy', 
                    'hedx_n',
                    'hedy_n'] 


        label_col = "class"

        # Normalize features
        scaler = StandardScaler()
        df[features] = scaler.fit_transform(df[features])

        # Encode labels
        df[label_col] = df[label_col].astype("category").cat.codes

        # Group by sender_id
        grouped = df.groupby("sender")

        sequence_length = 10

        # Apply function to all sender groups
        X_y_pairs = [create_time_series(group, features, label_col, sequence_length) for _, group in grouped]

        # Remove None values (senders with insufficient data)
        X_y_pairs = [pair for pair in X_y_pairs if pair is not None]

        # Ensure valid unpacking
        if len(X_y_pairs) > 0:
            X_list, y_list = zip(*X_y_pairs)  # Unpack
            X = np.concatenate(X_list, axis=0)  # Convert to final shape
            y = np.concatenate(y_list, axis=0)
        else:
            raise ValueError("No valid sequences found! Reduce `sequence_length`.")

        y = to_categorical(y, num_classes=len(np.unique(y)))

        X_train, x_test, Y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    
    for index in range(n_clients):
    
        x_train, _, y_train, _ = train_test_split(X_train, Y_train, test_size=0.90, random_state=index, stratify=Y_train)         
        
        with open(datapath+dataset+"_x_train"+str(index),'wb') as writer:
            dump(x_train[:8192*4],writer)
        
        with open(datapath+dataset+"_y_train"+str(index),'wb') as writer:
            dump(y_train[:8192*4],writer)
        
        with open(datapath+dataset+"_x_test"+str(index),'wb') as writer:
            dump(x_test[:2048],writer)
        
        with open(datapath+dataset+"_y_test"+str(index),'wb') as writer:
            dump(y_test[:2048],writer)

if __name__ == "__main__":
    generate_distribution_CAM(dataset="WiSec")
    generate_distribution_CAM(dataset="VeReMi")
