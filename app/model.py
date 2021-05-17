import numpy as np
import pandas as pd
from app.scaling import Preprocessing
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.metrics import r2_score
import datetime as dt

class Prediction(Preprocessing):
    
    def __init__(self, exchange, interval, asset, action_model, price_model, market = None):
        super().__init__(exchange, interval, asset, market)

        self.start_date = self.df.index[-3]
        self.action_model = action_model
        self.price_model = price_model

        features = ['High', 'Low', 'Open', 'Volume', 'Adj Close', 'P', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3', 
                    'OBV', 'MACD', 'MACDS', 'MACDH', 'SMA', 'LMA', 'RSI', 'SR_K', 'SR_D', 'HL_PCT', 'PCT_CHG']
        self.df_action = self.df.copy()[features + ['Distinct_Action']]
        self.df_price = self.df.copy()[features + ['Future_Adj_Close']]

        self.scaler = StandardScaler()
        self.df_price['Future_Adj_Close_Scaled'] = self.scaler.fit_transform(self.df_price[['Future_Adj_Close']].values).reshape(-1)
        self.action_features, self.action_labels = super(Prediction, self).scaling(self.df_action)
        self.price_features, self.price_labels = super(Prediction, self).scaling(self.df_price[features + ['Future_Adj_Close_Scaled']])
        self.mlb = MultiLabelBinarizer(classes = ['Buy', 'Hold', 'Sell'])
        self.action_labels = self.mlb.fit_transform(self.action_labels)
        
    def get_prediction(self):         
        self.model_prediction_action = self.action_model.predict(self.action_features)
        self.model_prediction_price = self.price_model.predict(self.price_features)
        
        self.model_prediction_action = np.array(self.mlb.inverse_transform(self.model_prediction_action.round()))
        self.model_prediction_price = self.scaler.inverse_transform(self.model_prediction_price).flatten()
        self.requested_prediction_action = str(self.model_prediction_action[-1][-1])
        self.requested_prediction_price = round(float(self.model_prediction_price[-1]), 8)

        price_prediction_length = self.model_prediction_price.shape[0]
        self.df_price = self.df_price.iloc[-price_prediction_length:]

        self.score_action = self.action_model.evaluate(self.action_features, self.action_labels, verbose = 0) 
        self.score_price = r2_score(self.df_price['Future_Adj_Close'].values[:-30], self.model_prediction_price[:-30])
        self.score_action, self.score_price = round((self.score_action[1] * 100), 2), round((self.score_price * 100), 2)
        
    def prediction_postprocessing(self, indication):
        self.indication = indication
        indicators = {'Analysed':'Distinct_Action', 'Predicted':'Action_Predictions'}

        action_prediction_length = self.model_prediction_action.shape[0]
        self.df_visulization = self.df.iloc[-action_prediction_length:]
        self.df_visulization['Action_Predictions'] = self.model_prediction_action
        self.df_visulization = self.df_visulization[['Adj Close', 'Volume', 'Distinct_Action', 
                                                     'Action_Predictions', 'Future_Adj_Close']]
        #self.df_visulization = self.df_visulization.iloc[-366:]
        self.df_visulization['Price_Buy'] = self.df_visulization[self.df_visulization[indicators[self.indication]] == 'Buy']['Adj Close']
        self.df_visulization['Price_Sell'] = self.df_visulization[self.df_visulization[indicators[self.indication]] == 'Sell']['Adj Close']

        interval_value = int(self.selected_interval.split()[0])
        interval_time = str(self.selected_interval.split()[1]).lower()

        future_date = []
        for value in range(1, 34):
            if interval_time == 'minute':
                future_date.append(self.start_date + dt.timedelta(minutes = value * interval_value))
            elif interval_time == 'hour':
                future_date.append(self.start_date + dt.timedelta(hours = value * interval_value))
            elif interval_time == 'day':
                future_date.append(self.start_date + dt.timedelta(days = value * interval_value))
            elif interval_time == 'week':
                future_date.append(self.start_date + dt.timedelta(weeks = value * interval_value))

        self.df_future_price = pd.DataFrame(future_date, columns = ['Date'])
        self.df_future_price['Future Price'] = self.model_prediction_price[-33:].reshape(-1)
        self.df_future_price.set_index('Date', inplace = True)
