import numpy as np
import pandas as pd
from app.scaling import Scaling
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer, OrdinalEncoder
from sklearn.metrics import r2_score

present_model = load_model("models/present_prediction_model.h5")
future_model = load_model("models/future_prediction_model.h5")
future_price_model = load_model("models/future_price_prediction_model.h5")

def ML(df, present_model = present_model, future_model = future_model, future_price_model = future_price_model):

    df_now = df[['Volume', 'P', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3', 'OBV', 'MACD', 'MACDS', 'MACDH', 
                'RSI', 'SR_K', 'SR_D', 'SMA', 'LMA', 'Distinct_Action']]

    df_future = df[['Volume', 'OBV', 'MACD', 'MACDS', 'MACDH', 'RSI', 'SR_K', 'SR_D', 'SMA', 'LMA', 
                    'Action_Buy', 'Action_Sell', 'Action_Hold', 'Distinct_Action', 'Future_Action']]

    df_future_price = df[['High', 'Low', 'Open', 'Volume', 'Adj Close', 'P', 'R1', 'R2', 'R3', 'S1', 
                            'S2', 'S3', 'OBV', 'HL_PCT', 'PCT_CHG', 'MACD', 'MACDS', 'MACDH', 'SMA', 
                            'LMA', 'RSI', 'SR_K', 'SR_D', 'Future_Adj_Close']]

    ole = OrdinalEncoder(categories = [['Buy', 'Hold', 'Sell']])
    df_future[['Distinct_Action']] = ole.fit_transform(df_future[['Distinct_Action']].values)

    features_now, labels_now = Scaling(df_now, 60)
    features_future, labels_future = Scaling(df_future, 60)
    features_future_price, labels_future_price, scaler_future_price = Scaling(df_future_price, 60, price = True)
    

    mlb = MultiLabelBinarizer(classes = ['Buy', 'Hold', 'Sell'])
    labels_now = mlb.fit_transform(labels_now)
    labels_future = mlb.fit_transform(labels_future)

    model_prediction_now = present_model.predict(features_now)
    model_prediction_future = future_model.predict(features_future)
    model_prediction_future_price = future_price_model.predict(features_future_price)

    model_prediction_now = np.array(mlb.inverse_transform(model_prediction_now.round()))
    model_prediction_future = np.array(mlb.inverse_transform(model_prediction_future.round()))
    model_prediction_future_price = np.array(scaler_future_price.inverse_transform(model_prediction_future_price))

    requested_prediction_now = str(model_prediction_now[-1][-1])
    requested_prediction_future = str(model_prediction_future[-1][-1])
    requested_prediction_future_price = round(float(model_prediction_future_price[-1][-1]), 8)

    score_now = present_model.evaluate(features_now, labels_now, verbose = 0) 
    score_future = future_model.evaluate(features_future[:-10], labels_future[:-10], verbose = 0)
    score_future_price = r2_score(np.array(scaler_future_price.inverse_transform(labels_future_price)[:-30]), model_prediction_future_price[:-30])

    score_now, score_future, score_future_price = score_now[1] * 100, score_future[1] * 100, score_future_price * 100
    score_now, score_future, score_future_price = round(score_now, 2), round(score_future, 2), round(score_future_price, 2)

    return str(requested_prediction_now), str(requested_prediction_future), str(requested_prediction_future_price), model_prediction_now, model_prediction_future_price, str(score_now), str(score_future), str(score_future_price)