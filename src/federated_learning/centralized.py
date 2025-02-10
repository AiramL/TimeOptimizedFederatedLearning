import tensorflow as tf
import pandas as pd 
import numpy as np
import seaborn as sns
import scipy.io as scio

from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

from sys import path 
path.append("../../utils")
from dataset_operations import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

dataset_1 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack16withlabels.mat')
dataset_2 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack1withlabels.mat')
dataset_3 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack2withlabels.mat')
dataset_4 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack4withlabels.mat')
dataset_5 = scio.loadmat('../../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset/attack8withlabels.mat')

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

df_dataset = pd.concat([pd.DataFrame(dataset_1['attack16withlabels']),
               pd.DataFrame(dataset_2['attack1withlabels']),
               pd.DataFrame(dataset_3['attack2withlabels']),
               pd.DataFrame(dataset_4['attack4withlabels']),
               pd.DataFrame(dataset_5['attack8withlabels'])])

df_dataset.columns = header

df_dataset = df_dataset.drop(['receiverID','senderID', 'messageID'], axis=1)

df_dataset = df_dataset.dropna()

features_nan_corr = ["receiverZposition",
                     "senderZposition",
                     "type",
                     "senderZvelocity",
                     "timeReceiver"]

df_dataset = df_dataset.drop(columns=features_nan_corr)

X = df_dataset.drop(columns=['class'])

columns_names = X.columns
scaler = MinMaxScaler()
scaler = scaler.fit(X)
X = pd.DataFrame(scaler.transform(X))
X.columns = columns_names

y = df_dataset['class']
y = pd.get_dummies(y,columns=['class'])

x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.8,random_state=42)
x_train = np.resize(x_train,(x_train.shape[0],1,x_train.shape[1]))
x_test = np.resize(x_test,(x_test.shape[0],1,x_test.shape[1]))

model = Sequential()
model.add(LSTM(100, activation='tanh',return_sequences=True,input_shape=(None,X.shape[1])))
model.add(LSTM(49,activation='tanh'))
model.add(Dense(6,activation='softmax'))

model.compile(optimizer="rmsprop", loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train,y_train,epochs=200,batch_size=64)

model.evaluate(x_test,y_test)

model.save("../../models/centralized.keras")




