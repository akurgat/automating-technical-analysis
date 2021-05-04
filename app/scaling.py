from app.indicator_analysis import Indications
from sklearn.preprocessing import scale, StandardScaler
from collections import deque
import numpy as np

class Preprocessing(Indications):
    
    def __init__(self, exchange, interval, asset, market = None):
        super().__init__(exchange, interval, asset, market)
        super(Preprocessing, self).Engulfing_Analysis()
        super(Preprocessing, self).Support_Resistance()
        super(Preprocessing, self).Moving_Average_Analysis()
        super(Preprocessing, self).MACD_Analysis()
        super(Preprocessing, self).Stochastic_Analysis()
        super(Preprocessing, self).RSI_Divagence_Convergence()
        super(Preprocessing, self).Price_Action()

    def scaling(self, df_values):
        self.training_window = 60
        self.df_predictors = df_values
        predictors = self.df_predictors.iloc[:, :-1].columns
        
        scaler = StandardScaler()
        self.df_predictors[predictors] = scale(self.df_predictors[predictors])
        self.df_predictors[predictors] = scaler.fit_transform(self.df_predictors[predictors])

        training_sequence = []
        previous_days = deque(maxlen = self.training_window)
        for i in self.df_predictors.values:
            previous_days.append([x for x in i[:-1]])
            if len(previous_days) == self.training_window:
                training_sequence.append([np.array(previous_days), i[-1:]])
                
        self.X = []
        self.y = []
        for features, action in training_sequence:
            self.X.append(features)
            self.y.append(action)
            
        self.X = np.array(self.X)
        self.y = np.array(self.y)
                                               
        return self.X, self.y