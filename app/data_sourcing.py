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
            df_dow = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1]
            df_dow['Currency'] = 'USD'
            df_dow = df_dow[['Symbol', 'Company']]
            df_dow.columns = ['Ticker', 'Company']
            df_dow['Index Fund'] = 'US Dow Jones'
            df_dow['Currency'] = 'USD'
            df_dow['Currency_Name'] = 'US Dollar'
        except:
            df_dow = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_nasdaq = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[3]
            df_nasdaq = df_nasdaq[['Ticker', 'Company']]
            df_nasdaq.columns = ['Ticker', 'Company']
            df_nasdaq['Index Fund'] = 'US NASDAQ 100'
            df_nasdaq['Currency'] = 'USD'
            df_nasdaq['Currency_Name'] = 'US Dollar'
        except:
            df_nasdaq = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_snp = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
            df_snp = df_snp[['Symbol', 'Security']]
            df_snp.columns = ['Ticker', 'Company']
            df_snp['Index Fund'] = 'US S&P 500'
            df_snp['Currency'] = 'USD'
            df_snp['Currency_Name'] = 'US Dollar'
        except:
            df_snp = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_sse = pd.read_html('https://en.wikipedia.org/wiki/SSE_50_Index')[1]
            df_sse = df_sse[['Ticker symbol', 'Name']]
            df_sse.columns = ['Ticker', 'Company']
            df_sse['Ticker'] = df_sse['Ticker'].apply(lambda x: x.split(' ')[1] + '.SS')
            df_sse['Index Fund'] = 'Chinese SSE 50'
            df_sse['Currency'] = 'CNY'
            df_sse['Currency_Name'] = 'Chinese Yuan'
        except:
            df_sse = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_csi = pd.read_html('https://en.wikipedia.org/wiki/CSI_300_Index')[3]
            df_csi.loc[df_csi['Stock exchange'] == 'Shanghai', 'Ticker'] =  df_csi['Index'].astype('str') + '.SS'
            df_csi.loc[df_csi['Stock exchange'] == 'Shenzhen', 'Ticker'] =  df_csi['Index'].astype('str') + '.SZ'
            tickers = []
            zeros = ['0']
            for ticker in df_csi['Ticker'].values:
                if len(ticker) < 9:
                    sum_zeros = zeros * (9 - len(ticker))
                    ticker = ''.join(sum_zeros) + ticker
                tickers.append(ticker)
            df_csi['Ticker'] = tickers
            df_csi = df_csi[['Ticker', 'Company']]
            df_csi['Index Fund'] = 'Chinese CSI 300'
            df_csi['Currency'] = 'CNY'
            df_csi['Currency_Name'] = 'Chinese Yuan'
        except:
            df_csi = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_ftse = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')[3]
            df_ftse = df_ftse[['EPIC', 'Company']]
            df_ftse.columns = ['Ticker', 'Company']
            df_ftse['Ticker'] = df_ftse['Ticker'].apply(lambda x: x + '.L')
            df_ftse['Index Fund'] = 'British FTSE 100'
            df_ftse['Currency'] = 'GBP'
            df_ftse['Currency_Name'] = 'British Pound'
        except:
            df_ftse = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_dax = pd.read_html('https://en.wikipedia.org/wiki/DAX')[3]
            df_dax = df_dax[['Ticker symbol', 'Company']]
            df_dax.columns = ['Ticker', 'Company']
            df_dax['Index Fund'] = 'German DAX'
            df_dax['Currency'] = 'EUR'
            df_dax['Currency_Name'] = 'Euro'
        except:
            df_dax = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_cac = pd.read_html('https://en.wikipedia.org/wiki/CAC_40')[3]
            df_cac = df_cac[['Ticker', 'Company']]
            df_cac.columns = ['Ticker', 'Company']
            df_cac['Index Fund'] = 'French CAC 40'
            df_cac['Currency'] = 'EUR'
            df_cac['Currency_Name'] = 'Euro'
        except:
            df_cac = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_bse_sensex = pd.read_html('https://en.wikipedia.org/wiki/BSE_SENSEX')[1]
            df_bse_sensex = df_bse_sensex[['Symbol', 'Companies']]
            df_bse_sensex.columns = ['Ticker', 'Company']
            df_bse_sensex['Index Fund'] = 'Indian S&P BSE SENSEX'
            df_bse_sensex['Currency'] = 'INR'
            df_bse_sensex['Currency_Name'] = 'Indian Rupee'
        except:
            df_bse_sensex = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_nifty = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
            df_nifty = df_nifty[['Symbol', 'Company Name']]
            df_nifty.columns = ['Ticker', 'Company']
            df_nifty['Ticker'] = df_nifty['Ticker'].apply(lambda x: x + '.NS')
            df_nifty['Index Fund'] = 'Indian Nifty 50'
            df_nifty['Currency'] = 'INR'
            df_nifty['Currency_Name'] = 'Indian Rupee'
        except:
            df_nifty = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
        try:
            df_asx = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200')[0]
            df_asx = df_asx[['Code', 'Company']]
            df_asx.columns = ['Ticker', 'Company']
            df_asx['Ticker'] = df_asx['Ticker'].apply(lambda x: x + '.AX')
            df_asx['Index Fund'] = 'Australian S&P ASX 200'
            df_asx['Currency'] = 'AUD'
            df_asx['Currency_Name'] = 'Australian Dollar'
        except:
            df_asx = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])

        df_stocks = pd.concat([df_snp, df_nasdaq, df_dow, df_sse, df_csi, df_ftse, df_dax, df_cac, df_bse_sensex, df_nifty, df_asx], ignore_index = True)
        df_stocks.loc[0, 'Last Update'] = dt.date.today()
        df_stocks.to_csv('stocks.txt', index = False)
        
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

        try:
            df_forex = pd.read_html('https://finance.yahoo.com/currencies')[0]
            df_forex = df_forex[['Symbol', 'Name']]
            df_forex.columns = ['Ticker', 'Currencies']
            df_forex['Currency'] = df_forex['Currencies'].apply(lambda x: x.split('/')[0])
            df_forex['Market'] = df_forex['Currencies'].apply(lambda x: x.split('/')[1])
            df_forex['Currencies'] = df_forex['Currencies'].apply(lambda x: x.replace('/', ' to '))
            df_forex.loc[0, 'Last Update'] = dt.date.today()
            df_forex.to_csv('forex.txt', index = False)
        except:
            pass

def data_update():
    df_crypto = pd.read_csv('market_data/crypto.txt')
    df_stocks = pd.read_csv('market_data/stocks.txt')
    df_indexes = pd.read_csv('market_data/indexes.txt')
    df_futures = pd.read_csv('market_data/futures.txt')
    df_forex = pd.read_csv('market_data/forex.txt')

    if (dt.datetime.now() - pd.to_datetime(df_crypto['Last Update'][0])).days >= 10:
        update_market_data('crypto')
        df_crypto = pd.read_csv('market_data/crypto.txt')

    if (((dt.datetime.now() - pd.to_datetime(df_stocks['Last Update'][0])).days >= 10) or 
        ((dt.datetime.now() - pd.to_datetime(df_indexes['Last Update'][0])).days >= 10) or 
        ((dt.datetime.now() - pd.to_datetime(df_futures['Last Update'][0])).days >= 10) or 
        ((dt.datetime.now() - pd.to_datetime(df_forex['Last Update'][0])).days >= 10)):
        update_market_data('stock')
        df_stocks = pd.read_csv('market_data/stocks.txt')
        df_indexes = pd.read_csv('market_data/indexes.txt')
        df_futures = pd.read_csv('market_data/futures.txt')
        df_forex = pd.read_csv('market_data/forex.txt')

    gc.collect()
        
def date_utc(date_):
    date_ = pd.to_datetime(date_, utc = True)
    date_ = date_.dt.tz_localize(None)
    return date_
        
class Data_Sourcing:
    def __init__(self):
        self.df_crypto = pd.read_csv('market_data/crypto.txt')
        self.df_stocks = pd.read_csv('market_data/stocks.txt')
        self.df_indexes = pd.read_csv('market_data/indexes.txt')
        self.df_futures = pd.read_csv('market_data/futures.txt')
        self.df_forex = pd.read_csv('market_data/forex.txt')

    def exchange_data(self, exchange):
        self.exchange = exchange
        if self.exchange == 'Bittrex' or self.exchange == 'Binance':
            self.markets = np.sort(self.df_crypto['Market Name'].unique())
        else: 
            self.stock_indexes = np.sort(self.df_stocks['Index Fund'].unique())
            self.indexes = np.sort(self.df_indexes['Indexes'].unique())
            self.futures = np.sort(self.df_futures['Futures'].unique())
            self.forex = np.sort(self.df_forex['Currencies'].unique())

    def market_data(self, market):
        self.market = market
        if self.exchange != 'Yahoo! Finance':
            self.assets = np.sort(self.df_crypto[(self.df_crypto['Market Name'] == self.market)]['Currency Name'].unique())
            self.currency = self.df_crypto[(self.df_crypto['Market Name'] == self.market)]['Market'].values[0]
        else:
            self.stocks = np.sort(self.df_stocks[(self.df_stocks['Index Fund'] == self.market)]['Company'].unique())
            
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
                url = f"https://api.binance.com/api/v3/klines?symbol={self.ticker_market}&interval={self.exchange_interval}"
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
                self.ticker = self.df_stocks[(self.df_stocks['Company'] == self.asset) & (self.df_stocks['Index Fund'] == self.market)]['Ticker'].values[0]
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
