from app.update_market_data import update_market_data
import json
import requests
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import gc

pd.set_option("display.precision", 8)

def data_update():
    #df_crypto = pd.read_csv('market_data/binance.txt')
    df_crypto = pd.read_csv('market_data/binance_us.txt')
    df_stocks = pd.read_csv('market_data/stocks.txt')
    df_indexes = pd.read_csv('market_data/indexes.txt')
    df_futures = pd.read_csv('market_data/futures.txt')
    df_forex = pd.read_csv('market_data/forex.txt')

    day_limit = 15

    if (((dt.datetime.now() - pd.to_datetime(df_crypto['Last Update'][0])).days >= day_limit) or 
        ((dt.datetime.now() - pd.to_datetime(df_stocks['Last Update'][0])).days >= day_limit) or 
        ((dt.datetime.now() - pd.to_datetime(df_indexes['Last Update'][0])).days >= day_limit) or 
        ((dt.datetime.now() - pd.to_datetime(df_futures['Last Update'][0])).days >= day_limit) or 
        ((dt.datetime.now() - pd.to_datetime(df_forex['Last Update'][0])).days >= day_limit)):
        update_market_data()

    gc.collect()
        
def date_utc(date_):
    date_ = pd.to_datetime(date_, utc = True)
    date_ = date_.dt.tz_localize(None)
    return date_
        
class Data_Sourcing:
    def __init__(self):
        #self.df_crypto = pd.read_csv('market_data/binance.txt')
        self.df_crypto = pd.read_csv('market_data/binance_us.txt')
        self.df_stocks = pd.read_csv('market_data/stocks.txt')
        self.df_indexes = pd.read_csv('market_data/indexes.txt')
        self.df_futures = pd.read_csv('market_data/futures.txt')
        self.df_forex = pd.read_csv('market_data/forex.txt')

    def exchange_data(self, exchange):
        self.exchange = exchange
        if self.exchange == 'Binance':
            self.markets = np.sort(self.df_crypto['Market'].unique())
        else: 
            self.stock_indexes = np.sort(self.df_stocks['Index Fund'].unique())
            self.indexes = np.sort(self.df_indexes['Indexes'].unique())
            self.futures = np.sort(self.df_futures['Futures'].unique())
            self.forex = np.sort(self.df_forex['Currencies'].unique())

    def market_data(self, market):
        self.market = market
        if self.exchange != 'Yahoo! Finance':
            self.assets = np.sort(self.df_crypto[(self.df_crypto['Market'] == self.market)]['Currency'].unique())
            self.currency = self.market
        else:
            self.stocks = np.sort(self.df_stocks[(self.df_stocks['Index Fund'] == self.market)]['Company'].unique())
            
    def intervals(self, selected_interval):
        self.selected_interval = selected_interval
        self.period = None
        exchange_interval = {'Yahoo! Finance': {'5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', '1 Hour':'60m', 
                                                '1 Day':'1d', '1 Week':'1wk', '1 Month':'1mo'}, 
                            'Binance': {'1 Minute':'1m', '3 Minute':'3m', '5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', 
                                        '1 Hour':'1h', '6 Hour':'6h', '12 Hour':'12h', '1 Day':'1d', '1 Week':'1w', '1 Month':'1M'}}
        
        self.exchange_interval = exchange_interval[self.exchange][self.selected_interval]
        
        if self.exchange == 'Yahoo! Finance':
            if self.selected_interval == '1 Minute':
                self.period = '7d'
            elif self.selected_interval == '5 Minute' or self.selected_interval == '15 Minute' or self.selected_interval == '30 Minute':
                self.period = '1mo'
            elif self.selected_interval == '1 Hour':
                self.period = '2y'
            else:
                self.period = 'max'
                    
    def apis(self, asset):
        self.asset = asset
        limit = 600
        
        if self.exchange != 'Yahoo! Finance':
            self.ticker_market = self.df_crypto[((self.df_crypto['Currency'] == self.asset) & 
                 (self.df_crypto['Market'] == self.market))][f'{self.exchange} Pair'].values[0]
            self.currency = self.markets
            if self.exchange == 'Binance':
                try:
                    url = f"https://api.binance.com/api/v3/klines?symbol={self.ticker_market}&interval={self.exchange_interval}&limit={limit}"
                    self.df = pd.DataFrame(json.loads(requests.get(url).text))
                except:
                    url = f"https://api.binance.us/api/v3/klines?symbol={self.ticker_market}&interval={self.exchange_interval}&limit={limit}"
                    self.df = pd.DataFrame(json.loads(requests.get(url).text))
                self.df.columns = ['open_time', 'Open', 'High', 'Low', 'Adj Close', 'Volume', 'close_time', 
                                'quoted average volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']
                self.df['Date'] = [dt.datetime.fromtimestamp(x/1000.0).replace(microsecond = 0) for x in self.df.open_time]
                
        else:
            try:
                self.ticker = self.df_stocks[((self.df_stocks['Company'] == self.asset) & (self.df_stocks['Index Fund'] == self.market))]['Ticker'].values[0]
                self.market = self.df_stocks[((self.df_stocks['Company'] == self.asset) & 
                                              (self.df_stocks['Index Fund'] == self.market))]['Currency_Name'].unique()[0]
            except:
                try:
                    self.ticker = self.df_indexes[(self.df_indexes['Indexes'] == self.asset)]['Ticker'].values[0]
                except:
                    try:
                        self.ticker = self.df_futures[(self.df_futures['Futures'] == self.asset)]['Ticker'].values[0]
                    except:
                        self.ticker = self.df_forex[(self.df_forex['Currencies'] == self.asset)]['Ticker'].values[0]
                    
            self.df = yf.download(tickers = self.ticker, period = self.period, interval = self.exchange_interval, 
                                  auto_adjust = True, prepost = True, threads = True, proxy = None).reset_index()
            self.df = self.df.rename(columns = {'Datetime':'Date', 'Close': 'Adj Close'})
            self.df = self.df.iloc[-750:]
            
        self.df['Date'] = date_utc(self.df['Date'])
        self.df.set_index('Date', inplace = True)
        self.df = self.df[['High', 'Low', 'Open', 'Volume', 'Adj Close']].apply(pd.to_numeric)
