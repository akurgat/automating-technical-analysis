from app.data_sourcing import Data_Sourcing, data_update
from app.indicator_analysis import Indications
from app.graph import Visualization
from tensorflow.keras.models import load_model
import streamlit as st 
import gc

gc.collect()
data_update()

def main(app_data):
    st.set_page_config(layout = "wide")
    indication = 'Predicted'

    st.sidebar.subheader('Asset:')
    asset_options = sorted(['Cryptocurrency', 'Index Fund', 'Forex', 'Futures & Commodities', 'Stocks'])
    asset = st.sidebar.selectbox('', asset_options, index = 5)

    if asset in ['Index Fund', 'Forex', 'Futures & Commodities', 'Stocks']:
        exchange = 'Yahoo! Finance'
        app_data.exchange_data(exchange)

        if asset == 'Stocks':
            st.sidebar.subheader(f'Stock Index:')
            stock_indexes  = app_data.stock_indexes
            market = st.sidebar.selectbox('', stock_indexes, index = 10)
            app_data.market_data(market)
            assets = app_data.stocks
            asset = f'{market} Companies'
        elif asset == 'Index Fund':
            assets = app_data.indexes
        elif asset == 'Futures & Commodities':
            assets = app_data.futures
        elif asset == 'Forex':
            assets = app_data.forex
        
        st.sidebar.subheader(f'{asset}:')
        equity = st.sidebar.selectbox('', assets)

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
        
        st.sidebar.subheader('Interval:')
        interval = st.sidebar.selectbox('', ('5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day', '1 Week'), index = 4)
        volitility_index = 0     

    elif asset in ['Cryptocurrency']:
        exchange = 'Binance'
        app_data.exchange_data(exchange)
        markets = app_data.markets
        
        st.sidebar.subheader('Market:')
        market = st.sidebar.selectbox('', markets, index = 1)
        app_data.market_data(market)
        assets = app_data.assets
        currency = app_data.currency
        
        st.sidebar.subheader('Crypto:')
        equity = st.sidebar.selectbox('', assets)

        st.sidebar.subheader('Interval:')
        interval = st.sidebar.selectbox('', ('1 Minute', '3 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '6 Hour', '12 Hour', '1 Day', '1 Week'), index = 2)

        volitility_index = 2 
        
    label = asset
        
    st.sidebar.subheader('Trading Volatility:')
    risk = st.sidebar.selectbox('', ('Low', 'Medium', 'High'), index = volitility_index)

    st.title(f'Automated Technical Analysis.')
    st.subheader(f'{label} Data Sourced from {exchange}.')
    st.info(f'Predicting...')
    
    future_price = 1   
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
        present_statement_suffix = ' at this time'
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

    st.markdown(f'**Prediction Date & Time (UTC):** {str(requested_date)}.')
    st.markdown(f'**Current Price:** {currency} {current_price}.')
    st.markdown(f'**{interval} Price Change:** {change_display}.')
    st.markdown(f'**Recommended Trading Action:** You should **{requested_prediction_action.lower()}** {present_statement_prefix} this {label.lower()[:6]}{present_statement_suffix}. {str(confidence[analysis.score_action])}')
    st.markdown(f'**Estimated Forecast Price:** The {label.lower()[:6]} {asset_suffix} for **{equity}** is estimated to be **{currency} {requested_prediction_price}** in the next **{forcast_prefix} {forcast_suffix}**. {str(confidence[analysis.score_price])}')
    if requested_prediction_action == 'Hold':
        st.markdown(f'**Recommended Trading Margins:** You should consider buying more **{equity}** {label.lower()[:6]} at **{currency} {buy_price}** and sell it at **{currency} {sell_price}**.')

    prediction_fig = analysis.prediction_graph(asset)
    
    st.success(f'Historical {label[:6]} Price Action.')
    st.plotly_chart(prediction_fig, use_container_width = True)

    technical_analysis_fig = analysis.technical_analysis_graph()
    st.success (f'Technical Analysis results from the {label[:6]} Data.')
    st.plotly_chart(technical_analysis_fig, use_container_width = True) 
    

if __name__ == '__main__':
    import warnings
    import gc
    warnings.filterwarnings("ignore") 
    gc.collect()
    action_model = load_model("models/action_prediction_model.h5")
    price_model = load_model("models/price_prediction_model.h5")
    app_data = Data_Sourcing()
    main(app_data = app_data)
