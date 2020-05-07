from app.technical_indicators import Technical_Calculations
from app.indicator_analysis import Indications, Price_Action
from app.exchange_api import *
from app.exchange_preprocessing import *
from app.model import ML
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


def load_data(stock, market, interval, exchange, label):

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

    df = df.iloc[-650:]
    requested_date = df.index[-1]
    current_price = df.iloc[-1,-1]

    if label == 'Stock':
        current_price = current_price.round(2)
    else:
        current_price = current_price.round(8)

    return df, str(requested_date), str(current_price)

def analyse(df):

    Technical_Calculations(df, df['Adj Close'], df['High'], df['Low'])
    df.dropna(inplace = True)
    analysis = analysis = df.loc[:, 'MACD':'SR_D']

    return analysis, df

def indications(df):

    Indications(df, df['Adj Close'], df['Open'])
    Price_Action(df)
    df.dropna(inplace = True)

    return df

def graph(Stock, ticker, data, model_prediction, indication):

    prediction_length = model_prediction.shape[0]
    df = data.iloc[-prediction_length:]
    df['Model_Predictions'] = model_prediction
    df = df[['Adj Close', 'General_Action', 'Distinct_Action', 'Model_Predictions']]
    df = df.iloc[-250:]

    if indication == 'General Analysis':

        df.loc[((df['General_Action'] == 'Buy')), 'Action_Buy'] = 1
        df.loc[((df['General_Action'] == 'Sell')), 'Action_Sell'] = 1
        df['Action_Buy'].fillna(0, inplace = True)
        df['Action_Sell'].fillna(0, inplace = True)
        
    elif indication == 'Distinct Analysis':

        df.loc[((df['Distinct_Action'] == 'Buy')), 'Action_Buy'] = 1
        df.loc[((df['Distinct_Action'] == 'Sell')), 'Action_Sell'] = 1
        df['Action_Buy'].fillna(0, inplace = True)
        df['Action_Sell'].fillna(0, inplace = True)

    elif indication == 'Model Prediction':

        df.loc[((df['Model_Predictions'] == 'Buy')), 'Action_Buy'] = 1
        df.loc[((df['Model_Predictions'] == 'Sell')), 'Action_Sell'] = 1
        df['Action_Buy'].fillna(0, inplace = True)
        df['Action_Sell'].fillna(0, inplace = True)

    fig = make_subplots(specs = [[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(x = df.index, y = df['Adj Close'], name = "Close Price", opacity = 1), secondary_y = True)
    fig.add_trace(go.Bar(x = df.index, y = df['Action_Sell'], name = "Sell", opacity = 1), secondary_y = False)
    fig.add_trace(go.Bar(x = df.index, y = df['Action_Buy'], name = "Buy", opacity = 1), secondary_y = False)
    
    fig.update_layout(autosize = False, height = 600, title_text = f"{Stock} to {ticker}", dragmode = False, plot_bgcolor = 'white', hovermode = 'x unified')
    fig.update_xaxes(title_text = "Date")
    fig.update_yaxes(title_text = "Close Price", secondary_y = True)
    fig.update_yaxes(title_text = "Price Action", secondary_y = False, range = [0, 1])

    return fig, df

def main():
    
    st.sidebar.subheader('Exchange:')
    exchange = st.sidebar.selectbox('', ('Yahoo Finance', 'Binance', 'Bittrex'))

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

        interval = st.sidebar.selectbox('', ('1 Hour', '1 Day', '1 Week'))        
        label = 'Stock'

    else:
        st.sidebar.subheader('Market:')
        market = st.sidebar.selectbox('', markets)

        coins = exchange_to_coins_loading (exchange, market)
        
        st.sidebar.subheader('Crypto:')
        stock = st.sidebar.selectbox('', coins)

        st.sidebar.subheader('Interval:')
        
        if exchange == 'Bitfinex':
            interval = st.sidebar.selectbox('', ('5 Minute', '15 Minute', '30 Minute', '1 Hour'))
        else:
            interval = st.sidebar.selectbox('', ('5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day'))

        label = 'Cryptocurrency'

    st.sidebar.subheader('Indication:')
    indication = st.sidebar.selectbox('', ('Model Prediction', 'Distinct Analysis', 'General Analysis'))

    st.title(f'Automated Technical Analysis for {label} Trading.')
    st.subheader(f'{label} Data Sourced from {exchange} in {interval} Interval.')
    st.info(f'Predicting...')

    st.cache(max_entries = 5)
    data, requested_date, current_price = load_data(stock, market, interval, exchange, label)

    st.cache(max_entries = 5)    
    analysis, data = analyse(data) 

    st.cache(max_entries = 5)
    data = indications(data)

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

    st.cache(max_entries = 5)
    requested_prediction_now, requested_prediction_future, model_prediction_now, score_now, score_future = ML(data)

    if requested_prediction_now == 'Hold':
        present_statement_prefix = 'off from preforming any action with'
        present_statement_suffix = ' at this time'
    else:
        present_statement_prefix = ''
        present_statement_suffix = ''

    if requested_prediction_future == 'Hold':
        future_statement = 'off from preforming any action with'
    else:
        future_statement = ''

    st.markdown(f'**Date Predicted:** {requested_date}')
    st.markdown(f'**Current Price:** {currency} {current_price}')
    st.markdown(f'**Current Trading Prediction:** You should **{requested_prediction_now}** {present_statement_prefix} this {label.lower()}{present_statement_suffix}.')
    st.markdown(f'**Future Trading Prediction:** You should consider **{requested_prediction_future}ing** {future_statement} this {label.lower()} in the next {int(interval.split()[0]) * 10} {str(interval.split()[1]).lower()}s.')
    st.markdown(f'**Current Trading Prediction Confidence:** {score_now}%')
    st.markdown(f'**Future Trading Prediction Confidence:** {score_future}%')

    st.cache(max_entries = 5)
    fig, df = graph(stock, market, data, model_prediction_now, indication)

    if indication == 'Model Prediction':
        testing_prefix = 'Predicted'

    else:
        testing_prefix = 'Analysed'

    st.success(f'Backtesting {testing_prefix} {label} Data...')
    st.plotly_chart(fig, use_container_width = True)

    st.sidebar.info('Advanced Options:')
    if st.sidebar.checkbox('The Sourced Data'):
        st.success ('Sourcing...')
        st.markdown(f'Sourced {label} Data.')
        st.write(data[['High', 'Low', 'Open', 'Volume', 'Adj Close']].tail(10))
        st.text ('Done!')
    
    if st.sidebar.checkbox('Technical Analysis Performed'):
            st.success ('Analyzing...')
            st.markdown(f'Technical analysis results from the {label} Data.')
            st.write(analysis[['MACD', 'MACDS', 'MACDH', 'RSI', 'SR_K', 'SR_D', 'SMA', 'LMA']].tail(10))
            st.text("Done!!!")
    
if __name__ == '__main__':
    main()
