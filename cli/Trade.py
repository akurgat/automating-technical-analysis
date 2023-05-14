"""main function refactored for cli module:
Note to humans: 
This is for LLM : remove if not using GPT-3 or 4 via openAI
1. removed all streamlit code
2. replaced all st.sidebar.subheader with print statements
3. if sidebar.selectbox use list comprehension to get the value
4. change from tensorflow.keras.models import load_model  to 
keras.models import load_model due to Mac M1 chip issues:
5. TODO: testing  ubuntu 23 server
6. create an api for this app
"""

import os
from traceback import print_tb
from app.data_sourcing import Data_Sourcing, data_update
from app.indicator_analysis import Indications
from app.graph import Visualization
from keras.models import load_model




# import streamlit as st 
import gc
import datetime


gc.collect()
# TODO: fix this path data_update()
data_update()



results = []
partial_results = []




def main(app_data,symbol,session_interval,session_tolerance,asset_type,ini_file):
    # st.set_page_config(layout = "wide")
    # print("------ main function ------")
    indication = 'Predicted'
    # st.sidebar.subheader('Asset:')
    # print(f"Asset: {asset_type}")
    asset_options = sorted(['Cryptocurrency', 'Index Fund', 'Forex', 'Futures & Commodities', 'Stocks'])
    # asset = st.sidebar.selectbox('', asset_options, index = 4)
    asset = [asset for asset in asset_options if asset_type[0] in asset][0] if asset_type[0] in asset_options else None
    if asset is None:
        print(f"Asset: {asset_type} not found in {asset_options}")
        return False
    # print(f"Asset: {asset}")
    
    
    if asset in ['Index Fund', 'Forex', 'Futures & Commodities', 'Stocks']:
        exchange = 'Yahoo! Finance'
        app_data.exchange_data(exchange)

        if asset == 'Stocks':
            # st.sidebar.subheader(f'Stock Index:')
            # print(f"Stock Index: {symbol[0]}")
            stock_indexes  = app_data.stock_indexes
            # market = st.sidebar.selectbox('', stock_indexes, index = 11)
            # TODO: scan the stock_indexes for the symbol and return the index by name
            market = stock_indexes[11]
            app_data.market_data(market)
            assets = app_data.stocks
            asset = f'{market} Companies'
        elif asset == 'Index Fund':
            assets = app_data.indexes
        elif asset == 'Futures & Commodities':
            assets = app_data.futures
        elif asset == 'Forex':
            assets = app_data.forex

        # st.sidebar.subheader(f'{asset}:')
        # print(f"{asset}: {symbol[0]}")
        # equity = st.sidebar.selectbox('', assets)
        equity = symbol[0]
        
        try:    
            if asset == 'Futures & Commodities':
                currency = 'USD'
                market = None
            elif asset == 'Index Fund':
                currency = 'Pts'
                market = None
            elif asset == 'Forex':
                currency = app_data.df_forex[(app_data.df_forex['Currencies'] == equity)]['Currency'].unique()[0]
                market = app_data.df_forex[(app_data.df_forex['Currencies'] == equity)]['Market'].unique()[0]
            elif asset == f'{market} Companies':
                currency = app_data.df_stocks[((app_data.df_stocks['Company'] == equity) & (app_data.df_stocks['Index Fund'] == market))]['Currency'].unique()[0]
                asset = 'Stock'
        except Exception as e:
            # This is a temp fix until I read the code traceback and fix the issue!
            if 'currency' not in locals():
                currency = 'USD'            
        # st.sidebar.subheader('Interval:')
        # print(f"Interval: {session_interval}")
        # interval = st.sidebar.selectbox('', ('5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day', '1 Week'), index = 4)
        interval = session_interval[0]
        volitility_index = 0     

    elif asset in ['Cryptocurrency']:
        raise NotImplementedError("cyrpto not implemented yet, if you want to use it, please implement it and remove this error and do a pull request")
        exchange = 'Binance'
        app_data.exchange_data(exchange)
        markets = app_data.markets
        
        st.sidebar.subheader('Market:')
        market = st.sidebar.selectbox('', markets, index = 3)
        app_data.market_data(market)
        assets = app_data.assets
        currency = app_data.currency
        
        st.sidebar.subheader('Crypto:')
        equity = st.sidebar.selectbox('', assets)

        st.sidebar.subheader('Interval:')
        interval = st.sidebar.selectbox('', ('1 Minute', '3 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '6 Hour', '12 Hour', '1 Day', '1 Week'), index = 8)

        volitility_index = 2 
    
    
    label = asset
    risk = session_tolerance[0]
    
    

    try:
        action_model = load_model(ini_file['models_path']['action_prediction_model'])
        price_model = load_model(ini_file['models_path']['price_prediction_model'])
    except Exception as e:
        # print(f"Error loading models trying root: {e}")
        root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        action_model = load_model(os.path.join(root_directory, 'models', 'action_prediction_model.h5'))
        price_model = load_model(os.path.join(root_directory, 'models', 'price_prediction_model.h5'))
        
        
    future_price = 1   
    # we could do  a while loop here to keep the app running and updating the data:    
    analysis = Visualization(exchange, interval, equity, indication, action_model, price_model, market)
    analysis_day = Indications(exchange, '1 Day', equity, market)
    requested_date = analysis.df.index[-1]
    current_price = float(analysis.df['Adj Close'][-1])
    change = float(analysis.df['Adj Close'].pct_change()[-1]) * 100
    requested_prediction_price = float(analysis.requested_prediction_price)
    requested_prediction_action = analysis.requested_prediction_action

    risks = {'Low': [analysis_day.df['S1'].values[-1], analysis_day.df['R1'].values[-1]], 
            'Medium': [analysis_day.df['S2'].values[-1], analysis_day.df['R2'].values[-1]],   
            'High': [analysis_day.df['S3'].values[-1], analysis_day.df['R3'].values[-1]],}
    buy_price = float(risks[risk][0])
    sell_price = float(risks[risk][1])

    if change > 0:
        change_display = f'A **{float(change):,.2f}%** gain'
    elif change < 0:
        change_display = f'A **{float(change):,.2f}%** loss'
    else:
        change_display = 'UNCH'

    if exchange == 'Yahoo! Finance':
        current_price = f'{float(current_price):,.2f}'
        requested_prediction_price = f'{float(requested_prediction_price):,.2f}'
        buy_price = f'{float(buy_price):,.2f}'
        sell_price = f'{float(sell_price):,.2f}'
    else:
        current_price = f'{float(current_price):,.8f}'
        requested_prediction_price = f'{float(requested_prediction_price):,.8f}'
        buy_price = f'{float(buy_price):,.8f}'
        sell_price = f'{float(sell_price):,.8f}'

    if analysis.requested_prediction_action == 'Hold':
        present_statement_prefix = 'off from taking any action with'
        present_statement_suffix = 'at this time'
    else:
        present_statement_prefix = ''
        present_statement_suffix = ''
                
    accuracy_threshold = {analysis.score_action: 75., analysis.score_price: 75.}
    confidence = dict()
    for score, threshold in accuracy_threshold.items():
        if float(score) >= threshold:
            confidence[score] = f'*({score}% confident)*'
        else:
            confidence[score] = ''

    forcast_prefix = int(interval.split()[0]) * future_price
    if forcast_prefix > 1:
        forcast_suffix = str(interval.split()[1]).lower() + 's'
    else:
        forcast_suffix = str(interval.split()[1]).lower()

    asset_suffix = 'price'
    show_results = True if ini_file['settings']['results_verbose'] == 'True' else False
    if (show_results): # TODO - pass a variable to determine if we should show the results or not            
        print(f'**Prediction Date & Time (UTC):** {str(requested_date)}.')
        print(f'**Current Price:** {currency} {current_price}.')
        print(f'**{interval} Price Change:** {change_display}.')
        print(f'**Recommended Trading Action:** You should **{requested_prediction_action.lower()}** {present_statement_prefix} this {label.lower()[:6]}{present_statement_suffix}. {str(confidence[analysis.score_action])}')
        print(f'**Estimated Forecast Price:** The {label.lower()[:6]} {asset_suffix} for **{equity}** is estimated to be **{currency} {requested_prediction_price}** in the next **{forcast_prefix} {forcast_suffix}**. {str(confidence[analysis.score_price])}')
        if requested_prediction_action == 'Hold':
            print(f'**Recommended Trading Margins:** You should consider buying more **{equity}** {label.lower()[:6]} at **{currency} {buy_price}** and sell it at **{currency} {sell_price}**.')

    todays_date = datetime.datetime.now().strftime("%m-%d-%Y")
    time_generated = datetime.datetime.now().strftime("%I:%M:%S %p")

    display_results = True if ini_file['settings']['display_graphs'] == 'True' else False
    if (display_results):
        prediction_fig = analysis.prediction_graph(asset)
        # TODO: use the output function to display the results: disable showing the graphs by default in tehe ini file
        # st.success(f'Historical {label[:6]} Price Action.')
        print(f'Historical {label[:6]} Price Action.')
        # plot the historical price action using fig
        print(prediction_fig.show())
        # st.plotly_chart(prediction_fig, use_container_width = True)
        technical_analysis_fig = analysis.technical_analysis_graph()
        # st.plotly_chart(technical_analysis_fig, use_container_width = True) 
        print(technical_analysis_fig.show())
        # Finally we can save or return the results
    try:
        predicted_results = {
            "equity":equity,
            "current_price": current_price,
            'side': requested_prediction_action.lower(),
            'confidence': str(confidence[analysis.score_action]).replace('*', '').replace('(', '').replace(')', ''),
            "requested_prediction_price": requested_prediction_price,
            "buy_price": buy_price,
            "sell_price": sell_price,
            "forecast_score": str(confidence[analysis.score_price]).replace('*', '').replace('(', '').replace(')', ''),
            "date_used_for_analysis": str(requested_date),
            "interval": interval,
            
            "date_generated": str(todays_date),
            "time_generated": str(time_generated)
        }
        # append the results due to the fact that we are not handling multiple stocks or a loop for results
        results.append(predicted_results)
    except Exception as e:
        print(e.__traceback__)
        


            
    
    
    
    
    
    



def predict_direction(stock,interval,risk,asset,verbose,cli_file):
    """Predicts the direction of the stock price movement
    
    Args: 
        stock (str): The stock symbol 
        interval (str): The time interval to use for the prediction
        risk (str): The risk level to use for the prediction
        asset (str): The asset type to use for the prediction
        verbose (bool): Whether to show the results or not
        cli_file (str): The path to the cli file
    Returns:
        dict: The results of the prediction    
    """
    
    import warnings
    warnings.filterwarnings("ignore")    
    gc.collect() # garbage collection to free up memory I think the system should handle this.
    app_data = Data_Sourcing()
    error = []
    for tickers in stock:
        try:
            main(
                app_data=app_data,
                symbol=[tickers], # TODO: add support for multiple stocks this isn't a good way to do it
                session_interval=interval,
                session_tolerance=risk,
                asset_type=asset,
                ini_file=cli_file
                )
        except Exception as e:
            # print(e.__traceback__)
            error.append[{'success':False, 'error':str(e)}]
            continue
    return results
    # print traceback error for debugging purposes:







# if __name__ == '__main__':
#     import warnings
#     import gc
#     warnings.filterwarnings("ignore") 
#     gc.collect()
#     action_model = load_model("models/action_prediction_model.h5")
#     price_model = load_model("models/price_prediction_model.h5")
#     app_data = Data_Sourcing()
#     main(app_data = app_data)
