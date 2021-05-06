from app.technical_indicators import Technical_Calculations

class Indications(Technical_Calculations):

    def __init__(self, exchange, interval, asset, market = None):
        self.engulfing_period = -5
        self.sma = -15
        self.lma = -20
        
        super().__init__(exchange, interval, asset, market)
        super(Indications, self).pivot_point()
        super(Indications, self).on_balance_volume()
        super(Indications, self).moving_average_convergence_divergence()
        super(Indications, self).moving_averages()
        super(Indications, self).relative_strength_index()
        super(Indications, self).slow_stochastic()
        super(Indications, self).price_analysis()

    def engulfing_analysis(self):
        self.df.loc[((self.df['Adj Close'] < self.df['Open']) | (self.df['Adj Close'] <= self.df['Open'].shift(self.engulfing_period)) & 
        (self.df['Adj Close'].shift(self.engulfing_period) > self.df['Open'].shift(self.engulfing_period))), 'Engulfing_Indication'] = 2
        self.df.loc[((self.df['Adj Close'] > self.df['Open']) | (self.df['Adj Close'] >= self.df['Open'].shift(self.engulfing_period)) & 
        (self.df['Adj Close'].shift(self.engulfing_period) < self.df['Open'].shift(self.engulfing_period))), 'Engulfing_Indication'] = 0
        self.df['Engulfing_Indication'].fillna(1, inplace = True)        

    def macd_analysis(self):
        self.df.loc[((self.df['MACD'] < self.df['MACDS'])), 'MADC_Indication'] = 2
        self.df.loc[((self.df['MACD'] > self.df['MACDS'])), 'MADC_Indication'] = 0 
        self.df['MADC_Indication'].fillna(1, inplace = True)

    def rsi_divagence_convergence(self):
        self.df.loc[((self.df['RSI'] >= 70)), 'RSI_Divagence_Convergence'] = 0
        self.df.loc[((self.df['RSI'] <= 30)), 'RSI_Divagence_Convergence'] = 2
        self.df['RSI_Divagence_Convergence'].fillna(1, inplace = True)

    def stochastic_analysis(self):
        self.df.loc[((self.df['SR_K'] > self.df['SR_D']) & (self.df['SR_K'] >= 80) & (self.df['RSI'] >= 70)), 'SR_Indication'] = 0
        self.df.loc[((self.df['SR_K'] < self.df['SR_D']) & (self.df['SR_K'] <= 20) & (self.df['RSI'] <= 30)), 'SR_Indication'] = 2
        self.df['SR_Indication'].fillna(1, inplace = True)

    def moving_average_analysis(self):
        self.df.loc[((self.df['SMA'] < self.df['LMA']) & (self.df['SMA'].shift(self.sma) > self.df['LMA'].shift(self.lma))), 'MA_Indication'] = 0
        self.df.loc[((self.df['SMA'] > self.df['LMA']) & (self.df['SMA'].shift(self.sma) < self.df['LMA'].shift(self.lma))), 'MA_Indication'] = 2
        self.df['MA_Indication'].fillna(1, inplace = True)

    def support_resistance(self):
        self.df.loc[((self.df['SMA'] < self.df['Adj Close']) & (self.df['SMA'].shift(self.sma) > self.df['Adj Close'].shift(self.sma))), 
        'Support_Resistance_Indication'] = 0
        self.df.loc[((self.df['SMA'] > self.df['Adj Close']) & (self.df['SMA'].shift(self.sma) < self.df['Adj Close'].shift(self.sma))), 
        'Support_Resistance_Indication'] = 2
        self.df['Support_Resistance_Indication'].fillna(1, inplace = True)

    def price_action(self):
        self.indication_estimate = 3
        self.df['Indication'] =  self.df.loc[:, 'Engulfing_Indication':].ewm(com = self.indication_estimate - 1, 
                                                                             min_periods = self.indication_estimate, 
                                                                             axis = 1).mean().iloc[:, -1].round(3)
        self.df.loc[((self.df['Indication'] >= 1.25) & (self.df['Adj Close'] <= self.df['P'])), 'Distinct_Action'] = 'Buy'
        self.df.loc[((self.df['Indication'] <= 0.75) & (self.df['Adj Close'] >= self.df['P'])), 'Distinct_Action'] = 'Sell'
        self.df['Distinct_Action'].fillna('Hold', inplace = True)
        self.df.drop(['Indication'], inplace = True, axis = 1)
        self.df.dropna(inplace = True)