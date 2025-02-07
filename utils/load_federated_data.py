#
# Author: Lucas Airam Castro de Souza
# Laboratory: Grupo de Teleinformatica e Automacao (GTA)
# University: Universidade Federal do Rio de Janeiro (UFRJ)
#

import numpy as np
import pandas as pd
import scipy.io as scio

from skimage import transform
from pickle import load
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


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


def load_CAM_data_federated(DATASET="VeReMi",test_size=0.2):
    # Need to implement the VeRemi data transformation
    if DATASET == "VeReMi":
        # Load dataset
        df_dataset = pd.read_csv('../../datasets/VeReMi_Extension/mixalldata_clean.csv')

        # Remove identifiers
        df_dataset = df_dataset.drop(['sender','senderPseudo', 'messageID'], axis=1)
        
        # Remove high correlated features
        features_nan_corr = ["posz",
                     "posz_n",
                     "spdz",
                     "spdz_n",
                     "hedz",
                     "aclz_n",
                     "hedz_n",
                     "type",
                     "posy_n",
                     "aclz"]

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



    elif DATASET == "WiSec":
        # Load dataset
        dataset_1 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack16withlabels.mat')
        dataset_2 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack1withlabels.mat')
        dataset_3 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack2withlabels.mat')
        dataset_4 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack4withlabels.mat')
        dataset_5 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack8withlabels.mat')
    
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
    return x_train, x_test, y_train, y_test
