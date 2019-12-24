from app.technical_indicators import Technical_Calculations
from app.indicator_analysis import Indications, Price_Action
from app.exchange_api import *
from app.exchange_preprocessing import *
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
from _plotly_future_ import v4_subplots
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from pandas.plotting import register_matplotlib_converters
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import cufflinks as cf

register_matplotlib_converters()
init_notebook_mode(connected = True)
cf.go_offline()


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
        stock_ticker = stock_to_ticker(stock) 
        period, stock_interval = yahoo_interval(interval) 
    else:
        cypto_ticker = crypto_to_ticker(stock)
        market_ticker = crypto_markets_to_ticker(market)
        interval = crypto_interval(exchange, interval)

    if exchange == 'Binance':
        df = binance_market_data(cypto_ticker, market_ticker, interval)
    elif exchange == 'Bitfinex':
        df = bitfinex_market_data(cypto_ticker, market_ticker, interval)
    elif exchange == 'Bittrex':
        df = bittrex_market_data(cypto_ticker, market_ticker, interval)
    else:
        df = yahoo_market_data(stock_ticker, period, stock_interval)

    df = df.iloc[-500:]
    requested_date = df.index[-1]
    current_price = df.iloc[-1,-1].round(2)

    return df, str(requested_date), str(current_price)

def analyse(df):

    Technical_Calculations(df, df['Adj Close'], df['High'], df['Low'])
    df.dropna(inplace = True)
    analysis = analysis = df.iloc[:, 5:13]

    return analysis, df

def indications(df):

    Indications(df, df['Adj Close'], df['Open'])
    Price_Action(df)
    df.dropna(inplace = True)
    indicators = df.iloc[:, 13:-1]

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

    markets = stock_crypto_markets(exchange)

    if exchange == 'Yahoo Finance':
        st.sidebar.subheader('Stock:')
        stock = st.sidebar.selectbox('', markets)

        if stock == 'Airbus' or stock == 'BMW' or stock == 'Volkswagen':
            market = 'Euros'
        elif stock == 'Samsung':
            market = 'Korean Won'
        else:
            market = 'US Dollar'

        interval = st.sidebar.selectbox('', ('1 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day', '1 Week', '1 Month'))        
        label = 'Stock'

    else:

        st.sidebar.subheader('Market:')
        market = st.sidebar.selectbox('', markets)

        coins = exchange_to_coins_loading (exchange, market)
        
        st.sidebar.subheader('Crypto:')
        stock = st.sidebar.selectbox('', coins)

        st.sidebar.subheader('Interval:')
        
        if exchange == 'Bitfinex':
            interval = st.sidebar.selectbox('', ('1 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour'))
        else:
            interval = st.sidebar.selectbox('', ('1 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day'))

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

    #if st.sidebar.checkbox ('The Price to Trade Action'):
    st.success('Graphing...')
    st.plotly_chart(fig)
    #st.balloons()

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
