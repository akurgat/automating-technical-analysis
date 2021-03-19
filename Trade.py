from app.technical_indicators import Technical_Calculations, Pivot_Point
from app.indicator_analysis import Indications, Price_Action
from app.exchange_api import *
from app.exchange_preprocessing import *
from app.model import ML
from app.graph import *
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np

def load_data(stock, market, interval, exchange, label):

    if exchange == 'Yahoo! Finance':
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
    start_date = df.index[-3]
    current_price = df.iloc[-1,-1]

    if label == 'Stock':
        current_price = current_price.round(2)
    else:
        current_price = current_price.round(8)

    return df, requested_date, start_date, str(current_price)

def analyse(df, future_price):

    Technical_Calculations(df, df['Adj Close'], df['Open'], df['High'], df['Low'], df['Volume'], future_price = future_price)
    df.dropna(inplace = True)
    analysis = analysis = df.loc[:, 'P':'SR_D']

    return analysis, df

def indications(df):
    Indications(df, df['Adj Close'], df['Open'])
    Price_Action(df)
    df.dropna(inplace = True)

    return df

def main():
    
    st.set_page_config(layout = "wide")
    
    st.sidebar.subheader('Exchange:')
    exchange = st.sidebar.selectbox('', ('Yahoo! Finance', 'Binance', 'Bittrex'))

    markets = stock_crypto_markets(exchange)

    if exchange == 'Yahoo! Finance':
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
        elif exchange == 'Binance':
            interval = st.sidebar.selectbox('', ('5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day'))
        else:
            interval = st.sidebar.selectbox('', ('5 Minute', '30 Minute', '1 Hour', '1 Day'))

        label = 'Cryptocurrency'

    st.sidebar.subheader('Indication:')
    indication = st.sidebar.selectbox('', ('Model Prediction', 'Distinct Analysis', 'General Analysis'))

    st.title(f'Automated Technical Analysis for {label} Trading.')
    st.subheader(f'{label} Data Sourced from {exchange} in {interval} Interval.')
    st.info(f'Predicting...')

    st.cache(max_entries = 5)
    data, requested_date, start_date, current_price = load_data(stock, market, interval, exchange, label)

    st.cache(max_entries = 5)    
    future_price = 30
    analysis, data = analyse(data, future_price = future_price) 

    st.cache(max_entries = 5)
    data = indications(data)

    if exchange != 'Yahoo! Finance':
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
    requested_prediction_now, requested_prediction_future, requested_prediction_future_price, model_prediction_now, model_prediction_future, score_now, score_future, score_future_price = ML(data)

    if requested_prediction_now == 'Hold':
        present_statement_prefix = 'off from taking any action with'
        present_statement_suffix = ' at this time'
    else:
        present_statement_prefix = ''
        present_statement_suffix = ''

    if requested_prediction_future == 'Hold':
        future_statement = 'off from taking any action with'
    else:
        future_statement = ''

    if label != 'Cryptocurrency':
        requested_prediction_future_price = str(round(float(requested_prediction_future_price), 2))

    accuracy_threshold = {score_now: 70., score_future: 50., score_future_price: 50.}
    confidence = dict()
    for score, threshold in accuracy_threshold.items():
        if float(score) >= threshold:
            confidence[score] = f'*({score}% confident.)*'
        else:
            confidence[score] = ''

    st.markdown(f'**Prediction Date & Time (UTC):** {str(requested_date)}')
    st.markdown(f'**Current Price:** {currency} {float(current_price):,.8f}')
    st.markdown(f'**Current Trading Prediction:** You should **{requested_prediction_now.lower()}** {present_statement_prefix} this {label.lower()[:6]}{present_statement_suffix}. {str(confidence[score_now])}')
    st.markdown(f'**Future Trading Prediction:** You should consider **{requested_prediction_future.lower()}ing** {future_statement} this {label.lower()[:6]} in the next **{int(interval.split()[0]) * 10} {str(interval.split()[1]).lower()}s**. {str(confidence[score_future])}')
    st.markdown(f'**Future Price Prediction:** The {label.lower()[:6]} price for  **{stock}** is estimated to be **{currency} {float(requested_prediction_future_price):,.8f}** in the next **{int(interval.split()[0]) * future_price} {str(interval.split()[1]).lower()}s**. {str(confidence[score_future_price])}')

    st.cache(max_entries = 5)
    prediction_fig = prediction_graph(stock, market, data, model_prediction_now, model_prediction_future, indication, start_date = start_date, interval = interval)

    if indication == 'Model Prediction':
        testing_prefix = 'Predicted'

    else:
        testing_prefix = 'Analysed'

    st.success(f'Historical {label[:6]} Price Action...({testing_prefix}.)')
    st.plotly_chart(prediction_fig, use_container_width = True)

    technical_analysis_fig = technical_analysis_graph(analysis)

    st.success (f'Technical Analysis results from the {label[:6]} Data...')
    st.plotly_chart(technical_analysis_fig, use_container_width = True)

    st.markdown('**Parameters Used:**')
    st.markdown('* Moving Average Convergence Divergence: 12, 26, 9.')
    st.markdown('* Relative Strength Index: 14 Days.')
    st.markdown('* Slow Stochastic: 14, 3, 3.')

    st.sidebar.info('Other Options:')
    
    if st.sidebar.checkbox('The Sourced Data'):
        st.success ('Sourcing...')
        st.markdown(f'Sourced {label} Data.')
        st.write(data[['High', 'Low', 'Open', 'Volume', 'Adj Close']].tail(10)) 

if __name__ == '__main__':
    main()
