import pandas as pd

def Technical_Calculations(df, close, high, low, volume):
    
    Pivot_Point(df, close, high, low)
    #On_Balance_Volume(df, volume)
    MACD(df, close)
    Moving_Averages(df, close)
    RSI(df, close)
    Slow_Stochastic(df, close, high, low)
 
def MACD(df, close):
    fast_length = 12
    slow_length = 26
    signal_smoothing = 9

    ema1 = close.ewm(span = fast_length, adjust = False).mean()
    ema2 = close.ewm(span = slow_length, adjust = False).mean()
    macd = ema1 - ema2
    df['MACD'] = macd

    ema3 = df['MACD'].ewm(span = signal_smoothing, adjust = False).mean()
    macd_histogram = macd - ema3
    df['MACDS'] = ema3
    df['MACDH'] = macd_histogram

def RSI(df, close):
    rsi_period = 14

    change = close.diff(1)

    gain = change.mask(change < 0, 0)
    loss = change.mask(change > 0, 0)

    average_gain = gain.ewm(com = rsi_period - 1, min_periods = rsi_period).mean()
    average_loss = loss.ewm(com = rsi_period - 1, min_periods = rsi_period).mean()

    rs = abs(average_gain / average_loss)
    rsi = 100 - (100 / (1 + rs))
    df['RSI'] = rsi

def Slow_Stochastic(df, close, high, low):
    n = 14
    
    low_stochastic = low.rolling(window = n).min()
    high_stochastic = high.rolling(window = n).max()

    fast_k = 100 * ((close - low_stochastic) / (high_stochastic - low_stochastic) )
    fast_d = fast_k.rolling(window = 3).mean()
    slow_d = fast_d.rolling(window = 3).mean()
    df['SR_K'] = fast_d
    df['SR_D'] = slow_d

def Moving_Averages(df, close):

    short_run = 20
    long_run = 50
    
    sma = close.rolling(short_run).mean()
    df['SMA'] = sma
    
    lma = close.rolling(long_run).mean()
    df['LMA'] = lma

def Pivot_Point(df, close, high, low): 
    
    P = (close + high + low) / 3
    R1 = (P * 2) - low
    R2 = P + (high - low)
    R3 = high + 2 * (P - low)
    S1 = (P * 2) - high
    S2 = P - (high - low)
    S3 = low - 2 * (high - P)
    
    df['P'] = P
    df['R1'] = R1
    df['R2'] = R2
    df['R3'] = R3
    df['S1'] = S1
    df['S2'] = S2
    df['S3'] = S3

def On_Balance_Volume(df, volume):

    previous_volume = volume.shift(-1)

    df['OBV'] = 0

    df.loc[((df[volume].shift(-1)) < (df[volume])), 'OBV'] = df['OBV'] + df[volume].shift(-1)
    df.loc[((df[volume].shift(-1)) > (df[volume])), 'OBV'] = df['OBV'] - df[volume].shift(-1)
    df.loc[((df[volume].shift(-1)) == (df[volume])), 'OBV'] = df['OBV'] + 0

    df['OBV'].fillna(0, inplace = True)

