import pandas as pd

def Indications(df, close, open_):

    Engulfing_Analysis(df, close, open_)
    MACD_Analysis(df)
    Moving_Average_Analysis(df)
    Support_Resistance(df, close)
    RSI_Divagence_Convergence(df, close)
    Stochastic_Analysis(df)
    df.dropna(inplace = True)

def Engulfing_Analysis(df, close, open_):
    
    engulfing_period = -5

    df.loc[((close < open_) | (close <= open_.shift(engulfing_period)) & 
    (close.shift(engulfing_period) > open_.shift(engulfing_period))), 'Engulfing_Indication'] = 2
    df.loc[((close > open_) | (close >= open_.shift(engulfing_period)) & 
    (close.shift(engulfing_period) < open_.shift(engulfing_period))), 'Engulfing_Indication'] = 0
    df['Engulfing_Indication'].fillna(1, inplace = True)        

def MACD_Analysis(df):
   
    df.loc[((df['MACD'] < df['MACDS'])), 'MADC_Indication'] = 2
    df.loc[((df['MACD'] > df['MACDS'])), 'MADC_Indication'] = 0 
    df['MADC_Indication'].fillna(1, inplace = True)


def RSI_Divagence_Convergence(df, close):

    df.loc[((df['RSI'] >= 70)), 'RSI_Divagence_Convergence'] = 0
    df.loc[((df['RSI'] <= 30)), 'RSI_Divagence_Convergence'] = 2
    df['RSI_Divagence_Convergence'].fillna(1, inplace = True)

def Stochastic_Analysis(df):

    df.loc[((df['SR_K'] > df['SR_D']) & (df['SR_K'] >= 80) & (df['RSI'] >= 70) & (df['MACDH'] < 0)), 'SR_Indication'] = 0
    df.loc[((df['SR_K'] < df['SR_D']) & (df['SR_K']) <= 20) & (df['RSI'] <= 30) & (df['MACDH'] > 0), 'SR_Indication'] = 2
    df['SR_Indication'].fillna(1, inplace = True)

def Moving_Average_Analysis(df):

    sma = -15
    lma = -20

    df.loc[((df['SMA'] < df['LMA']) & (df['SMA'].shift(sma) > df['LMA'].shift(lma))), 'MA_Indication'] = 0
    df.loc[((df['SMA'] > df['LMA']) & (df['SMA'].shift(sma) < df['LMA'].shift(lma))), 'MA_Indication'] = 2
    df['MA_Indication'].fillna(1, inplace = True)

def Support_Resistance(df, close):

    sma = -15

    df.loc[((df['SMA'] < close) & (df['SMA'].shift(sma) > close.shift(sma))), 'Support_Resistance_Indication'] = 0
    df.loc[((df['SMA'] > close) & (df['SMA'].shift(sma) < close.shift(sma))), 'Support_Resistance_Indication'] = 2
    df['Support_Resistance_Indication'].fillna(1, inplace = True)

def Price_Action(df):

    df['Indication'] =  df.loc[:, 'Engulfing_Indication':].mean(axis = 1).round(3)

    df.loc[((df['Indication'] < 1 )), 'General_Action'] = 'Sell'
    df.loc[((df['Indication'] > 1 )), 'General_Action'] = 'Buy' 
    df.loc[((df['Indication'] == 1 )), 'General_Action'] = 'Hold' 

    df.loc[((df['General_Action'] == 'Buy') & (df['Adj Close'] == df['Adj Close'].rolling(5).min())), 'Action_Buy'] = 1
    df.loc[((df['General_Action'] == 'Sell') & (df['Adj Close'] == df['Adj Close'].rolling(5).max())), 'Action_Sell'] = 1
    df.loc[((df['General_Action'] == 'Hold')), 'Action_Hold'] = 1
    df['Action_Buy'].fillna(0, inplace = True)
    df['Action_Sell'].fillna(0, inplace = True)
    df['Action_Hold'].fillna(0, inplace = True)

    df.loc[((df['Action_Buy'] == 0 ) & (df['Action_Sell'] == 1 )), 'Distinct_Action'] = 'Sell'
    df.loc[((df['Action_Buy'] == 1 ) & (df['Action_Sell'] == 0 )), 'Distinct_Action'] = 'Buy'
    df.loc[((df['Action_Buy'] == 0 ) & (df['Action_Sell'] == 0 )), 'Distinct_Action'] = 'Hold'

    df['Future_Action'] = df['Distinct_Action'].shift(-10)
    df['Future_Action'].fillna(0, inplace = True)
    df.drop(['Indication'], inplace = True, axis = 1)
    df.dropna(inplace = True)


