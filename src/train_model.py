# implement the training for lstm model to predict thorughputs
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
import torch.utils.data as data

def create_dataset(dataset, lookback):
    """Transform a time series into a prediction dataset
    
    Args:
        dataset: A numpy array of time series, first dimension is the time steps
        lookback: Size of window for prediction
    """
    X, y = [], []
    for i in range(len(dataset)-lookback):
        feature = dataset[i:i+lookback]
        target = dataset[i+1:i+lookback+1]
        X.append(feature)
        y.append(target)
    return torch.tensor(X), torch.tensor(y)

class LSTM(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=50, num_layers=1, batch_first=True)
        self.linear = nn.Linear(50, 1)

    def forward(self, x):
        x, _ = self.lstm(x)
        x = self.linear(x)
        return x

def load_tp(client_id=1, data_path="data/processed/", data_file="0.csv"):
    client_id = 1
    df = pd.read_csv(data_path+data_file)
    dt = df[df['Node ID'] == client_id].reset_index()
    tpu = dt[['Throughput DL']].values.astype('float32')
    tpd = dt[['Throughput UL']].values.astype('float32')
    return tpu, tpd


def train():
    # train-test split for time series
    train_size = int(len(tpd) * 0.67)
    test_size = len(tpd) - train_size
    train, test = tpd[:train_size], tpd[train_size:]

    lookback = 5
    X_train, y_train = create_dataset(train, lookback=lookback)
    X_test, y_test = create_dataset(test, lookback=lookback)

    print(X_train.shape, y_train.shape)
    print(X_test.shape, y_test.shape)

    model = LSTM()
    optimizer = optim.Adam(model.parameters())
    loss_fn = nn.MSELoss()
    loader = data.DataLoader(data.TensorDataset(X_train, y_train), shuffle=True, batch_size=8)

    n_epochs = 60
    for epoch in range(n_epochs):
        model.train()
        for X_batch, y_batch in loader:
            y_pred = model(X_batch)
            loss = loss_fn(y_pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        # Validation
        if epoch % 10 != 0:
            continue
        model.eval()

        with torch.no_grad():
            y_pred = model(X_train)
            train_rmse = np.sqrt(loss_fn(y_pred, y_train))
            y_pred = model(X_test)
            test_rmse = np.sqrt(loss_fn(y_pred, y_test))
        print("Epoch %d: train RMSE %.4f, test RMSE %.4f" % (epoch, train_rmse, test_rmse))


        with torch.no_grad():
            # shift train predictions for plotting
            train_plot = np.ones_like(tpd) * np.nan
            y_pred = model(X_train)
            y_pred = y_pred[:, -1, :]
            train_plot[lookback:train_size] = model(X_train)[:, -1, :]
            # shift test predictions for plotting
            test_plot = np.ones_like(tpd) * np.nan
            test_plot[train_size+lookback:len(tpd)] = model(X_test)[:, -1, :]

    # plot
    plt.plot(tpd,c='b',label="real data")
    plt.plot(train_plot, c='r',label="traning")
    plt.plot(test_plot, c='g',label="testing")
    plt.xlabel("Sample (#)")
    plt.ylabel("Throughput (Mb/s)")
    plt.legend()
    plt.show()
    
    torch.save(model.state_dict(),"models/model_10.pt")

if __name__ == "__main__":
    tpu, tpd = load_tp()
    train()
