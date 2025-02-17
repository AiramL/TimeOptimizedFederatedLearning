from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Precision, Recall#, F1Score


def build_model(features_shape,labels_shape,model_name="MLP",MODEL_PATH=None):
    if model_name == "MLP":
        
        model = Sequential([
                Dense(32,input_shape=(features_shape), activation='relu'),
                Dense(128, activation='relu'),
                Dense(labels_shape,activation='softmax')
            ])
        
        model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

    elif model_name == "BIGAN":
        
        model = Sequential()
        model.add(LSTM(100, activation='tanh',return_sequences=True,input_shape=(None,features_shape)))
        model.add(LSTM(49,activation='tanh'))
        model.add(Dense(labels_shape, activation='softmax'))

        model.compile(optimizer="rmsprop", loss='categorical_crossentropy', metrics=['accuracy'])

    elif model_name == "LSTM_1":
        
        model = Sequential()
        model.add(Bidirectional(LSTM(64, activation='tanh',return_sequences=True,input_shape=(10,20))))
        model.add(Dropout(0.2))
        model.add(Dropout(0.2))
        model.add(Dense(24,activation='relu'))
        model.add(GlobalAveragePooling1D())
        model.add(Dense(20,activation='softmax'))

        model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    return model


