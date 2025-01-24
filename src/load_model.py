# implement the training for lstm model to predict thorughputs
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
import torch.utils.data as data

from train_model import AirModel, load_tp, create_dataset

model = AirModel()

model.load_state_dict(torch.load("model_10.pt", weights_only=True))

tpu, tpd = load_tp()

# train-test split for time series
train_size = int(len(tpd) * 0.67)
test_size = len(tpd) - train_size
train, test = tpd[:train_size], tpd[train_size:]

lookback = 10
X_train, y_train = create_dataset(train, lookback=lookback)
X_test, y_test = create_dataset(test, lookback=lookback)

print("x[0]: ",X_test[0])

y_hat = model(X_test[0])
print("y: ",y_test[0],"y_hat: ",y_hat)
