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
    (close.shift(engulfing_period) > open_.shift(engulfing_period))), 'Engulfing_Indication'] = 1

    df.loc[((close > open_) | (close >= open_.shift(engulfing_period)) & 
    (close.shift(engulfing_period) < open_.shift(engulfing_period))), 'Engulfing_Indication'] = 0

    df['Engulfing_Indication'].fillna(0.5, inplace = True)        

def MACD_Analysis(df):

    macd = -12
    macds = -26
   
    df.loc[((df['MACD'] < df['MACDS']) & (df['MACD'].shift(macd) > df['MACDS'].shift(macds))), 'MADC_Indication'] = 0

    df.loc[((df['MACD'] > df['MACDS']) & (df['MACD'].shift(macd) < df['MACDS'].shift(macds))), 'MADC_Indication'] = 1 

    df['MADC_Indication'].fillna(0.5, inplace = True)

def RSI_Divagence_Convergence(df, close):

    rsi_short = 14
    rsi_long = 30

    df.loc[((df['RSI'].rolling(30).max().shift(rsi_long) >= 70) & 
    (df['RSI'].rolling(14).max().shift(rsi_short) < df['RSI'].rolling(30).max().shift(rsi_long)) & 
    (close.rolling(14).max().shift(rsi_short) > close.rolling(30).max().shift(rsi_long))), 'RSI_Divagence_Convergence'] = 1

    df.loc[((df['RSI'].rolling(30).min().shift(rsi_long) <= 30) & 
    (df['RSI'].rolling(14).min().shift(rsi_short) > df['RSI'].rolling(30).min().shift(rsi_long))& 
    (close.rolling(14).min().shift(rsi_short) < close.rolling(30).min().shift(rsi_long))), 'RSI_Divagence_Convergence'] = 0

    df['RSI_Divagence_Convergence'].fillna(0.5, inplace = True)

def Stochastic_Analysis(df):

    slow_k = -14
    slow_d = -30

    df.loc[((df['SR_K'] < df['SR_D']) & (df['SR_K'].shift(slow_k) > df['SR_D'].shift(slow_d)) & 
    (df['SR_K'].rolling(30).max().shift(slow_d) >= 80)), 'SR_Indication'] = 1

    df.loc[((df['SR_K'] > df['SR_D']) & (df['SR_K'].shift(slow_k) < df['SR_D'].shift(slow_d)) & 
    (df['SR_K'].rolling(30).min().shift(slow_d) <= 20)), 'SR_Indication'] = 0

    df['SR_Indication'].fillna(0.5, inplace = True)

def Moving_Average_Analysis(df):

    sma = -15
    lma = -20

    df.loc[((df['SMA'] < df['LMA']) & (df['SMA'].shift(sma) > df['LMA'].shift(lma))), 'MA_Indication'] = 0

    df.loc[((df['SMA'] > df['LMA']) & (df['SMA'].shift(sma) < df['LMA'].shift(lma))), 'MA_Indication'] = 1

    df['MA_Indication'].fillna(0.5, inplace = True)

def Support_Resistance(df, close):

    sma = -15

    df.loc[((df['SMA'] < close) & (df['SMA'].shift(sma) > close.shift(sma))), 'Support_Resistance_Indication'] = 0

    df.loc[((df['SMA'] > close) & (df['SMA'].shift(sma) < close.shift(sma))), 'Support_Resistance_Indication'] = 1

    df['Support_Resistance_Indication'].fillna(0.5, inplace = True)

def Price_Action(df):

    df['Indication'] =  df.loc[:, 'Engulfing_Indication':].mean(axis = 1).round(3)

    df.loc[((df['Indication'] < 0.5 )), 'Action'] = 'Sell'
    df.loc[((df['Indication'] > 0.55 )), 'Action'] = 'Buy' 
    df['Action'].fillna('Hold', inplace = True)

    df.drop('Indication', inplace = True, axis =1)
 
    df.dropna(inplace = True)

