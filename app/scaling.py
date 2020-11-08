from sklearn.preprocessing import scale, StandardScaler, LabelEncoder
from collections import deque
import numpy as np
import pandas as pd
import random

def Scaling(df, training_window, price = False):

    predictors = df.iloc[:, :-1].columns
    scaler = StandardScaler()

    df[predictors] = scale(df[predictors])
    df[predictors] = scaler.fit_transform(df[predictors])
    if price:
        df.iloc[:-30, -1:] = scaler.fit_transform(df.iloc[:-30, -1:])
                 
    training_sequence = []
    previous_days = deque(maxlen = training_window)

    for i in df.values:
        previous_days.append([x for x in i[:-1]])
        if len(previous_days) == training_window:
            training_sequence.append([np.array(previous_days), i[-1:]])

    X = []
    y = []

    for features, action in training_sequence:
        X.append(features)
        y.append(action)
    
    X = np.array(X)
    y = np.array(y)

    if price:
        return X, y, scaler
    else:
        return X, y
