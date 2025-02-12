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
from utils import *
from models import build_model 
from load_federated_data import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

DATASET = "VeReMi"    

MODEL = "BIGAN"

x_train, x_test, y_train, y_test = load_CAM_data_federated(DATASET,0.2)
    
model = build_model(x_train.shape[1:][1],y_train.shape[1:][0],MODEL)
    
model.compile(optimizer="rmsprop", loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train,y_train,epochs=40,batch_size=64)
    
model.evaluate(x_test,y_test)
    
model.save("../../models/centralized_"+DATASET+".keras")





