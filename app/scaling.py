from app.indicator_analysis import Indications
from sklearn.preprocessing import scale, StandardScaler
from collections import deque
import numpy as np

class Preprocessing(Indications):
    
    def __init__(self, exchange, interval, asset, market = None):
        super().__init__(exchange, interval, asset, market)
        super(Preprocessing, self).engulfing_analysis()
        super(Preprocessing, self).support_resistance()
        super(Preprocessing, self).moving_average_analysis()
        super(Preprocessing, self).macd_analysis()
        super(Preprocessing, self).stochastic_analysis()
        super(Preprocessing, self).rsi_divagence_convergence()
        super(Preprocessing, self).price_action()

    def scaling(self, df_values):
        self.training_window = 60
        self.df_predictors = df_values
        predictors = self.df_predictors.iloc[:, :-1].columns
        self.df_predictors = self.df_predictors.replace([np.inf, -np.inf], 0)
        
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