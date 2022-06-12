import json
import requests
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import gc

pd.set_option("display.precision", 8)

def update_market_data(data):
    
    if data == 'crypto':
        try:
            url = 'https://api.bittrex.com/api/v1.1/public/getmarkets'
            df_bittrex = pd.DataFrame(requests.get(url).json()['result'])[['MarketCurrency', 'BaseCurrency', 'MarketCurrencyLong', 'BaseCurrencyLong', 'MarketName']]
            df_bittrex.columns = ['Currency', 'Market', 'Currency Name', 'Market Name', 'Bittrex Pair']

            url = 'https://api.binance.com/api/v3/exchangeInfo'
            df_binance = pd.DataFrame(requests.get(url).json()['symbols'])
            df_binance = df_binance[df_binance['status'] == 'TRADING'][['symbol', 'baseAsset', 'quoteAsset']]
            df_binance.columns = ['Binance Pair', 'Currency', 'Market']
            df_binance = df_binance[(df_binance['Market'].isin(df_bittrex['Market']))]
            df_binance = df_binance[(df_binance['Currency'].isin(df_bittrex['Currency']))]

            df_crypto = pd.merge(df_bittrex, df_binance, how = 'inner', on = ['Currency', 'Market']).drop_duplicates()
            df_crypto.loc[0, 'Last Update'] = dt.date.today()
            df_crypto[['Currency Name', 'Market Name', 'Bittrex Pair', 'Binance Pair', 'Market', 'Last Update']].to_csv('market_data/crypto.txt', index = False)
        except:
            pass    
    elif data == 'stock':
        try:
            df_stocks = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
            currencies = {'EUR': ['Ireland', 'Netherlands', 'Kingdom of the Netherlands'], 
                          'GBP': ['Bristol', 'United Kingdom', 'Surrey', 'UK'], 
                          'CHf': ['Switzerland'], 
                          'BMD': ['Bermuda']}
            currency_name = {'USD': 'US Dollar', 'EUR': 'Euro', 'GBP': 'British Pound', 'CHf': 'Swiss Franc', 'BMD': 'Bermuda Dollar'}

            for key, values in currencies.items():
                df_stocks.loc[df_stocks['Headquarters Location'].apply(lambda x: x.split(',')[1].strip(' ')).isin(values), 'Currency'] = key
            df_stocks['Currency'] = df_stocks['Currency'].fillna('USD')

            df_stocks = df_stocks[['Symbol', 'Security', 'Currency']]
            df_stocks.columns = ['Ticker', 'Company', 'Currency']
            df_stocks['Currency_Name'] = df_stocks['Currency'].map(currency_name)
            df_stocks.loc[0, 'Last Update'] = dt.date.today()
            df_stocks.to_csv('market_data/snp500.txt', index = False)
        except:
            pass
        
        try:
            df_indexes = pd.read_html('https://finance.yahoo.com/world-indices/')[0]
            df_indexes = df_indexes[['Symbol', 'Name']]
            df_indexes.columns = ['Ticker', 'Indexes']
            df_indexes.loc[0, 'Last Update'] = dt.date.today()
            df_indexes.to_csv('market_data/indexes.txt', index = False)
        except:
            pass

        try:
            df_futures = pd.read_html('https://finance.yahoo.com/commodities')[0]
            df_futures = df_futures[['Symbol', 'Name']]
            df_futures.columns = ['Ticker', 'Futures']
            for futures_ in [['BTC=F', 'Bitcoin Futures'], ['ETH=F', 'Ether Futures']]:
                df_futures.loc[len(df_futures)] = futures_
            df_futures = df_futures.drop_duplicates(subset = ['Ticker', 'Futures'], keep = False)
            df_futures.loc[0, 'Last Update'] = dt.date.today()
            df_futures.to_csv('market_data/futures.txt', index = False)
        except:
            pass

def data_update():
    df_crypto = pd.read_csv('market_data/crypto.txt')
    df_stocks = pd.read_csv('market_data/snp500.txt')
    df_indexes = pd.read_csv('market_data/indexes.txt')
    df_futures = pd.read_csv('market_data/futures.txt')

    if (dt.datetime.now() - pd.to_datetime(df_crypto['Last Update'][0])).days >= 10:
        update_market_data('crypto')
        df_crypto = pd.read_csv('market_data/crypto.txt')

    if (((dt.datetime.now() - pd.to_datetime(df_stocks['Last Update'][0])).days >= 10) or 
        ((dt.datetime.now() - pd.to_datetime(df_indexes['Last Update'][0])).days >= 10) or 
        ((dt.datetime.now() - pd.to_datetime(df_futures['Last Update'][0])).days >= 10)):
        update_market_data('stock')
        df_stocks = pd.read_csv('market_data/snp500.txt')
        df_indexes = pd.read_csv('market_data/indexes.txt')
        df_futures = pd.read_csv('market_data/futures.txt')

    gc.collect()
        
def date_utc(date_):
    date_ = pd.to_datetime(date_, utc = True)
    date_ = date_.dt.tz_localize(None)
    return date_
        
class Data_Sourcing:
    def __init__(self):
        self.df_crypto = pd.read_csv('market_data/crypto.txt')
        self.df_stocks = pd.read_csv('market_data/snp500.txt')
        self.df_indexes = pd.read_csv('market_data/indexes.txt')
        self.df_futures = pd.read_csv('market_data/futures.txt')

    def exchange_data(self, exchange):
        self.exchange = exchange
        if self.exchange == 'Bittrex' or self.exchange == 'Binance':
            self.markets = np.sort(self.df_crypto['Market Name'].unique())
        else: 
            self.stocks = np.sort(self.df_stocks['Company'].unique())
            self.indexes = np.sort(self.df_indexes['Indexes'].unique())
            self.futures = np.sort(self.df_futures['Futures'].unique())

    def market_data(self, market):
        self.market = market
        if self.exchange != 'Yahoo! Finance':
            self.assets = np.sort(self.df_crypto[(self.df_crypto['Market Name'] == self.market)]['Currency Name'].unique())
            self.currency = self.df_crypto[(self.df_crypto['Market Name'] == self.market)]['Market'].values[0]
            
    def intervals(self, selected_interval):
        self.selected_interval = selected_interval
        self.period = None
        exchange_interval = {'Yahoo! Finance': {'5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', '1 Hour':'60m', 
                                         '1 Day':'1d', '1 Week':'1wk', '1 Month':'1mo'}, 
                     'Binance': {'3 Minute':'3m', '5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', 
                                 '1 Hour':'1h', '6 Hour':'6h', '12 Hour':'12h', '1 Day':'1d', '1 Week':'1w', '1 Month':'1M'}, 
                     'Bittrex': {'5 Minute':'fiveMin', '30 Minute':'thirtyMin', '1 Hour':'hour', '1 Day':'day'}}
        
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
        
        if self.exchange != 'Yahoo! Finance':
            self.ticker_market = self.df_crypto[((self.df_crypto['Currency Name'] == self.asset) & 
                 (self.df_crypto['Market Name'] == self.market))][f'{self.exchange} Pair'].values[0]
            self.currency = self.df_crypto[((self.df_crypto['Currency Name'] == self.asset) & 
                 (self.df_crypto['Market Name'] == self.market))]['Market'].values[0]
            if self.exchange == 'Binance':
                url = f"https://api.binance.com/api/v1/klines?symbol={self.ticker_market}&interval={self.exchange_interval}"
                self.df = pd.DataFrame(json.loads(requests.get(url).text))
                self.df.columns = ['open_time', 'Open', 'High', 'Low', 'Adj Close', 'Volume', 'close_time', 
                                'quoted average volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']
                self.df['Date'] = [dt.datetime.fromtimestamp(x/1000.0).replace(microsecond = 0) for x in self.df.close_time]
            elif self.exchange == 'Bittrex':
                url = f"https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={self.ticker_market}&tickInterval={self.exchange_interval}"
                self.df = pd.DataFrame(json.loads(requests.get(url).text)['result'])
                self.df = self.df.rename(columns = {'O':'Open', 'H':'High', 'L':'Low', 'C':'Adj Close', 'V':'Volume', 
                                     'BV':'Base Volume', 'T':'Date'})
                self.df['Date'] = self.df['Date'].apply(lambda x: x.replace('T', ' '))
                
        else:
            try:
                self.ticker = self.df_stocks[(self.df_stocks['Company'] == self.asset)]['Ticker'].values[0]
            except:
                try:
                    self.ticker = self.df_indexes[(self.df_indexes['Indexes'] == self.asset)]['Ticker'].values[0]
                except:
                    self.ticker = self.df_futures[(self.df_futures['Futures'] == self.asset)]['Ticker'].values[0]
                    
            self.df = yf.download(tickers = self.ticker, period = self.period, interval = self.exchange_interval, 
                                  auto_adjust = True, prepost = True, threads = True, proxy = None).reset_index()
            self.df = self.df.rename(columns = {'Datetime':'Date', 'Close': 'Adj Close'})
            self.df = self.df.iloc[-750:]
            
        self.df['Date'] = date_utc(self.df['Date'])
        self.df.set_index('Date', inplace = True)
        self.df = self.df[['High', 'Low', 'Open', 'Volume', 'Adj Close']].apply(pd.to_numeric)
