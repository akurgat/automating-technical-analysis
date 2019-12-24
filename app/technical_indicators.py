import pandas as pd

def Technical_Calculations(df, close, high, low):
    
    #Fibonacci(df, high, low)
    MACD(df, close)
    Moving_Averages(df, close)
    RSI(df, close)
    Slow_Stochastic(df, close, high, low)

def Fibonacci(df, high, low):
    price_low = df['Low'].rolling(30).min()
    price_high = df['High'].rolling(30).max()

    price_change = price_high - price_low

    df['Fibonacci_0'] = price_high
    df['Fibonacci_23.6'] = price_high - (price_change * 0.236)
    df['Fibonacci_38.2'] = price_high - (price_change * 0.382)
    df['Fibonacci_50'] = price_high - (price_change * 0.5)
    df['Fibonacci_61.8'] = price_high - (price_change * 0.618)
    df['Fibonacci_78.6'] = price_high - (price_change * 0.786)
    df['Fibonacci_100'] = price_low
    
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
    
    low_14 = low.rolling(window = n).min()
    high_14 = high.rolling(window = n).max()

    fast_k = 100 * ((close - low_14) / (high_14 - low_14) )
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
