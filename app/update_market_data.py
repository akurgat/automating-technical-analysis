import json
import requests
import datetime as dt
import pandas as pd

def update_market_data():
    try:
        url = 'https://api.binance.com/api/v3/exchangeInfo'
        data = requests.get(url).json()
        df_binance = pd.DataFrame(data['symbols'])[pd.DataFrame(data['symbols'])['status'] == 'TRADING'][['symbol', 'baseAsset', 'quoteAsset']]
        df_binance = df_binance[(df_binance['quoteAsset'].isin(['BNB', 'BTC', 'BUSD', 'ETH', 'USDT']))]
        df_binance.columns = ['Binance Pair', 'Currency', 'Market']
        df_binance = df_binance.reset_index(drop = True)
        df_binance.loc[0, 'Last Update'] = dt.date.today()

        df_binance.to_csv('market_data/binance.txt', index = False)
    except:
        pass

    try:
        url = 'https://api.binance.us/api/v3/exchangeInfo'
        data = requests.get(url).json()
        df_binance_us = pd.DataFrame(data['symbols'])[pd.DataFrame(data['symbols'])['status'] == 'TRADING'][['symbol', 'baseAsset', 'quoteAsset']]
        df_binance_us = df_binance_us[(df_binance_us['quoteAsset'].isin(['BTC', 'BUSD', 'ETH', 'USD', 'USDT']))]
        df_binance_us.columns = ['Binance Pair', 'Currency', 'Market']
        df_binance_us = df_binance_us.reset_index(drop = True)
        df_binance_us.loc[0, 'Last Update'] = dt.date.today()

        df_binance_us.to_csv('market_data/binance_us.txt', index = False)
    except:
        pass

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
        df_nasdaq = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[4]
        df_nasdaq = df_nasdaq[['Ticker', 'Company']]
        df_nasdaq.columns = ['Ticker', 'Company']
        df_nasdaq['Index Fund'] = 'US NASDAQ 100'
        df_nasdaq['Currency'] = 'USD'
        df_nasdaq['Currency_Name'] = 'US Dollar'
    except:
        df_nasdaq = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
    try:
        df_russell = pd.read_html('https://en.wikipedia.org/wiki/Russell_1000_Index')[2]
        df_russell = df_russell[['Ticker', 'Company']]
        df_russell['Index Fund'] = 'US Russell 1000'
        df_russell['Currency'] = 'USD'
        df_russell['Currency_Name'] = 'US Dollar'
    except:
        df_russell = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
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
        df_ftse = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')[4]
        df_ftse = df_ftse[['Ticker', 'Company']]
        df_ftse['Ticker'] = df_ftse['Ticker'].apply(lambda x: x + '.L')
        df_ftse['Index Fund'] = 'British FTSE 100'
        df_ftse['Currency'] = 'GBP'
        df_ftse['Currency_Name'] = 'British Pound'
    except:
        df_ftse = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
    try:
        df_dax = pd.read_html('https://en.wikipedia.org/wiki/DAX')[4]
        df_dax = df_dax[['Ticker', 'Company']]
        df_dax.columns = ['Ticker', 'Company']
        df_dax['Index Fund'] = 'German DAX'
        df_dax['Currency'] = 'EUR'
        df_dax['Currency_Name'] = 'Euro'
    except:
        df_dax = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
    try:
        df_cac = pd.read_html('https://en.wikipedia.org/wiki/CAC_40')[4]
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
        df_nifty = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[2]
        df_nifty = df_nifty[['Symbol', 'Company Name']]
        df_nifty.columns = ['Ticker', 'Company']
        df_nifty['Ticker'] = df_nifty['Ticker'].apply(lambda x: x + '.NS')
        df_nifty['Index Fund'] = 'Indian Nifty 50'
        df_nifty['Currency'] = 'INR'
        df_nifty['Currency_Name'] = 'Indian Rupee'
    except:
        df_nifty = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])
    try:
        df_asx = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200')[1]
        df_asx = df_asx[['Code', 'Company']]
        df_asx.columns = ['Ticker', 'Company']
        df_asx['Ticker'] = df_asx['Ticker'].apply(lambda x: x + '.AX')
        df_asx['Index Fund'] = 'Australian S&P ASX 200'
        df_asx['Currency'] = 'AUD'
        df_asx['Currency_Name'] = 'Australian Dollar'
    except:
        df_asx = pd.DataFrame(columns = ['Ticker', 'Company', 'Index Fund', 'Currency', 'Currency_Name'])

    df_stocks = pd.concat([df_snp, df_nasdaq, df_dow, df_russell, df_sse, df_csi, df_ftse, df_dax, df_cac, df_bse_sensex, df_nifty, df_asx], ignore_index = True)
    df_stocks.loc[0, 'Last Update'] = dt.date.today()
    df_stocks.to_csv('market_data/stocks.txt', index = False)

    try:
        df_forex = pd.read_html('https://finance.yahoo.com/currencies')[0]
        df_forex = df_forex[['Symbol', 'Name']].iloc[:-1]
        df_forex.columns = ['Ticker', 'Currencies']
        df_forex['Currency'] = df_forex['Currencies'].astype('str').apply(lambda x: x.split('/')[0])
        df_forex['Market'] = df_forex['Currencies'].astype('str').apply(lambda x: x.split('/')[1])
        df_forex['Currencies'] = df_forex['Currencies'].apply(lambda x: x.replace('/', ' to '))
        df_forex.loc[0, 'Last Update'] = dt.date.today()
        df_forex.to_csv('market_data/forex.txt', index = False)
    except:
        pass

    try:
        df_futures = pd.read_html('https://finance.yahoo.com/commodities')[0]
        df_futures = df_futures[['Symbol', 'Name']]
        df_futures.columns = ['Ticker', 'Futures']
        for futures_ in [['BTC=F', 'Bitcoin Futures'], ['ETH=F', 'Ether Futures'],  ['DX=F', 'US Dollar Index']]:
            df_futures.loc[len(df_futures)] = futures_
        df_futures = df_futures.drop_duplicates(subset = ['Ticker', 'Futures'], keep = False)
        df_futures.loc[0, 'Last Update'] = dt.date.today()
        df_futures.to_csv('market_data/futures.txt', index = False)
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
        