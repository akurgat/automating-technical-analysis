from sklearn.preprocessing import scale, StandardScaler, LabelEncoder
from collections import deque
import numpy as np
import pandas as pd
import random

def Scaling(df, training_window):
           
    training_sequence = []
    previous_days = deque(maxlen = training_window)

    for i in df.values:
        previous_days.append([x for x in i[:-1]])

        if len(previous_days) == training_window:
            training_sequence.append([np.array(previous_days), i[-1]])

    random.shuffle(training_sequence)

    X = []
    y = []

    for feature, action in training_sequence:
        X.append(feature)
        y.append(action)
    
    X = np.array(X)
    y = np.array(y)
    
    scaler = StandardScaler()

    X = X.reshape(X.shape[0], -1)
    X = scale(X)
    X = scaler.fit_transform(X)
    X = X.reshape(X.shape[0], training_window, int(X.shape[1]/training_window))

    return X, y
