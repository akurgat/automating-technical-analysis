from app.technical_indicators import Technical_Calculations
from app.indicator_analysis import Indications, Price_Action
from app.exchange_api import *
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
from _plotly_future_ import v4_subplots
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from pandas.plotting import register_matplotlib_converters
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf

register_matplotlib_converters()
init_notebook_mode(connected = True)
cf.go_offline()


def yahoo_preprocess(Stock, Interval):

    if Interval == '1 Minute':
        period = '7d'
    elif Interval == '5 Minute' or Interval == '15 Minute' or Interval == '30 Minute':
        period = '1mo'
    elif Interval == '1 Hour':
        period = '2y'
    else:
        period = 'max'

    stocks = {'Apple': 'AAPL', 'Airbus': 'AIR.BE', 'AMD': 'AMD', 'Boeing': 'BA', 'BMW': 'BMW.BE', 'Facebook': 'FB', 
                'Google': 'GOOG', 'IBM': 'IBM', 'Intel': 'INTC', 'Jumia': 'JMIA', 'Microsoft': 'MSFT', 'Nvidia': 'NVDA', 
                'Samsung': '005930.KS', 'Tesla': 'TSLA', 'Twitter': 'TWTR', 'Uber': 'UBER','Volkswagen': 'VOW.DE'}

    intervals = {'1 Minute':'1m', '5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', 
                '1 Hour':'60m', '1 Day':'1d', '1 Week':'1wk', '1 Month':'1mo'}

    for stock, ticker in stocks.items():
        if Stock == stock:
            stock_ticker = ticker

    for interval, inter in intervals.items():
        if Interval == interval:
            stock_interval = inter

    return stock_ticker, period, stock_interval

def crypto_preprocess(Stock, Market, Interval):

    cryptocurrency = {'Bitcoin': 'BTC', 'Bitcoin Cash': 'BCH', 'Cardano': 'ADA', 'Ethereum': 'ETH', 
    'EOS': 'EOS', 'Groestlcoin': 'GRS', 'Litecoin': 'LTC', 'Stellar': 'XLM', 'Ripple': 'XRP'}

    markets = {'Bitcoin': 'BTC', 'Ethereum': 'ETH', 'Tether' : 'USDT', 'US Dollar' : 'USD'}

    intervals = {'1 Minute':'1m', '5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', 
    '1 Hour':'1h', '1 Day':'1d', '1 Week':'1w', '1 Month':'1M'}

    bittrex_intervals = {'1 Minute':'oneMin', '5 Minute':'fiveMin', '30 Minute':'thirtyMin', 
    '1 Hour':'hour', '1 Day':'day'}

    for crypto, tick in cryptocurrency.items():
        if Stock == crypto:
            crypto_ticker = tick

    for market, markt in markets.items():
        if Market == market:
            crypto_market = markt

    for interval, inter in intervals.items():
        if Interval == interval:
            crypto_interval = inter

    for bit_interval, bit_inter in bittrex_intervals.items():
        if Interval == bit_interval:
            bittrex_interval = bit_inter

    return crypto_ticker,  crypto_market, crypto_interval, bittrex_interval

def prediction_action(prediction):

    action = ''
    if (prediction == 0.5):
        action = 'Hold'
    elif (prediction >= 0) and (prediction < 0.5):
        action = 'Sell' 
    elif (prediction <= 1) and (prediction > 0.5):
        action = 'Buy' 

    return action

def load_data(stock, market, interval, exchange):

    if exchange == 'Yahoo Finance':
        stock_ticker, period, stock_interval = yahoo_preprocess(stock, interval) 
    else:
        cypto_ticker, market, interval, bittrex_interval = crypto_preprocess(stock, market, interval)

    if exchange == 'Binance':
        df = binance_market_data(cypto_ticker, market, interval)
    elif exchange == 'Bitfinex':
        df = bitfinex_market_data(cypto_ticker, market, interval)
    elif exchange == 'Bittrex':
        df = bittrex_market_data(cypto_ticker, market, bittrex_interval)
    else:
        df = yahoo_market_data(stock_ticker, period, stock_interval)

    df = df.iloc[-500:]
    requested_date = df.index[-1]
    current_price = df.iloc[-1,-1].round(2)

    return df, str(requested_date), str(current_price)

def analyse(df):

    Technical_Calculations(df, df['Adj Close'], df['High'], df['Low'])
    df.dropna(inplace = True)
    analysis = analysis = df.loc[:, 'MACD':]

    return analysis, df

def indications(df):

    Indications(df, df['Adj Close'], df['Open'])
    Price_Action(df)
    df.dropna(inplace = True)
    indicators = df.loc[:, 'Engulfing_Indication':'SR_Indication']

    return indicators

def graph(Stock, ticker, df):

    fig = make_subplots(specs = [[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = df.index, y = df['Action'], name = "Price Action"), secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, y = df['Adj Close'], name = "Close Price"), secondary_y = True)
    
    fig.layout.update(title_text = Stock + " to " + ticker)
    fig.update_xaxes(title_text = "Date")
    fig.update_yaxes(title_text = "Close Price", secondary_y = True)
    fig.update_yaxes(title_text = "Price Action", secondary_y = False)

    return fig

def main():
    
    st.sidebar.subheader('Exchange:')
    exchange = st.sidebar.selectbox('', ('Binance', 'Bitfinex', 'Bittrex', 'Yahoo Finance'))

    if exchange == 'Yahoo Finance':
        st.sidebar.subheader('Stock:')
        stock = st.sidebar.selectbox('', ('Apple', 'Airbus', 'AMD', 'Boeing', 'BMW', 'Facebook', 'Google', 'IBM', 
                                        'Intel', 'Jumia', 'Microsoft', 'Nvidia', 'Samsung', 'Tesla', 'Twitter', 'Uber', 'Volkswagen'))

        if stock == 'Airbus' or stock == 'BMW' or stock == 'Volkswagen':
            market = 'Euros'
        elif stock == 'Samsung':
            market = 'Korean Won'
        else:
            market = 'US Dollar'

        interval = st.sidebar.selectbox('', ('1 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day', '1 Week', '1 Month'))        
        label = 'Stock'

    else:
        st.sidebar.subheader('Crypto:')
        stock = st.sidebar.selectbox('', ('Bitcoin', 'Bitcoin Cash', 'Cardano', 'Ethereum', 'EOS', 'Groestlcoin', 'Litecoin', 'Ripple', 'Stellar'))

        st.sidebar.subheader('Market:')
        market = st.sidebar.selectbox('', ('Bitcoin', 'Ethereum', 'Tether', 'US Dollar'))

        st.sidebar.subheader('Interval:')
        interval = st.sidebar.selectbox('', ('1 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day', '1 Week', '1 Month'))

        label = 'Crytpocurrency'

    st.title(f'Simple {label} Trading.')
    st.subheader(f'Stock Data Sourced from {exchange} in {interval} Intervals.')

    data, requested_date, current_price = load_data(stock, market, interval, exchange)

    st.sidebar.info('Advanced Options:')
    if st.sidebar.checkbox('The Sourced Data'):
        st.success ('Sourcing...')
        st.write(data.tail(10))
        st.text ('Done!')
    
    analysis, df = analyse(data) 

    if st.sidebar.checkbox('Technical Analysis Performed'):
            st.success ('Analyzing...')
            st.write(analysis.tail(10))
            st.text("Done!!!")

    indicators = indications(df)

    if st.sidebar.checkbox('Trading Indications Identified'):
            st.success('Thinking Like a Trader...')
            st.write(indicators.tail(10))
            st.text('Finished.')

    fig = graph(stock, market, data)

    st.success('Graphing...')
    st.plotly_chart(fig)


    if exchange != 'Yahoo Finance':
        if market == 'Bitcoin':
            currency = 'BTC '
        elif market == 'Ethereum':
            currency = 'ETH '
        elif market == 'Tether':
            currency = 'USDT '
        else:
            currency = 'USD '
    elif stock == 'Airbus' or stock == 'BMW' or stock == 'Volkswagen':
        currency = 'EUR '
    elif stock == 'Samsung':
        currency = 'KRW '
    else:
        currency = 'USD '
    

if __name__ == '__main__':
    main()
