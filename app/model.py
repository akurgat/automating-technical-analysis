import numpy as np
import pandas as pd
from app.scaling import Scaling
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

model = load_model("models/prediction_model.h5")

def ML(df, model = model):

    df = df[['Engulfing_Indication', 'MADC_Indication', 'SR_Indication', 'MA_Indication', 
            'Support_Resistance_Indication', 'RSI_Divagence_Convergence', 'Action']]

    features, labels = Scaling(df, 60)

    le = LabelEncoder()
    le = le.fit(['Buy', 'Hold', 'Sell']) 
    labels = le.transform(labels)
    labels = to_categorical(labels)

    model_prediction = model.predict(features)
    model_prediction = le.inverse_transform(np.argmax(model_prediction.round(1), axis = 1))
    requested_prediction = model_prediction[-1]

    score = model.evaluate(features, labels, verbose = 0)
    score = score[1] * 100
    score = score.round(2)

    return str(requested_prediction), model_prediction, str(score)