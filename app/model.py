import numpy as np
import pandas as pd
from app.scaling import Scaling
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer, OrdinalEncoder

present_model = load_model("models/present_prediction_model.h5")
future_model = load_model("models/future_prediction_model.h5")

def ML(df, present_model = present_model, future_model = future_model):

    df_now = df[['MACD', 'MACDS', 'MACDH', 'RSI', 'SR_K', 'SR_D', 'SMA', 'LMA', 'Distinct_Action']]
    df_future = df[['Action_Buy', 'Action_Sell', 'Action_Hold', 'Distinct_Action', 'Future_Action']]

    ole = OrdinalEncoder(categories = [['Buy', 'Hold', 'Sell']])
    df_future['Distinct_Action'] = ole.fit_transform(df_future[['Distinct_Action']].values)

    features_now, labels_now = Scaling(df_now, 60)
    features_future, labels_future = Scaling(df_future, 60)

    mlb = MultiLabelBinarizer(classes = ['Buy', 'Hold', 'Sell'])
    labels_now = mlb.fit_transform(labels_now)
    labels_future = mlb.fit_transform(labels_future)

    model_prediction_now = present_model.predict(features_now)
    model_prediction_future = future_model.predict(features_future)

    model_prediction_now = np.array(mlb.inverse_transform(model_prediction_now.round()))
    model_prediction_future = np.array(mlb.inverse_transform(model_prediction_future.round()))

    requested_prediction_now = str(model_prediction_now[-1][-1])
    requested_prediction_future = str(model_prediction_future[-1][-1])

    score_now = present_model.evaluate(features_now, labels_now, verbose = 0) 
    score_future = future_model.evaluate(features_future, labels_future, verbose = 0)

    score_now, score_future = score_now[1] * 100, score_future[1] * 100
    score_now, score_future = round(score_now, 2), round(score_future, 2)

    return str(requested_prediction_now), str(requested_prediction_future), model_prediction_now, str(score_now), str(score_future)