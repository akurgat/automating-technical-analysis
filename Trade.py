from app.data_sourcing import Data_Sourcing
from app.graph import Visualization
from tensorflow.keras.models import load_model
import streamlit as st 

action_model = load_model("models/action_prediction_model.h5")
price_model = load_model("models/price_prediction_model.h5")
app_data = Data_Sourcing()

def main():
    st.set_page_config(layout = "wide")
    st.sidebar.subheader('Indication:')
    indication = st.sidebar.selectbox('', ('Predicted', 'Analysed'))
    
    st.sidebar.subheader('Exchange:')
    exchange = st.sidebar.selectbox('', ('Binance', 'Bittrex', 'Yahoo! Finance'))
    app_data.exchange_data(exchange)

    if exchange == 'Yahoo! Finance':
        assets = app_data.stocks
        market = None
        
        st.sidebar.subheader('Stock:')
        asset = st.sidebar.selectbox('', assets)
        currency = app_data.df_stocks[(app_data.df_stocks['Company'] == asset)]['Currency'].values[0]
            
        st.sidebar.subheader('Interval:')
        interval = st.sidebar.selectbox('', ('1 Hour', '1 Day', '1 Week'))        
        label = 'Stock'
    else:
        markets = app_data.markets
        
        st.sidebar.subheader('Market:')
        market = st.sidebar.selectbox('', markets)
        app_data.market_data(market)
        assets = app_data.assets
        currency = app_data.currency
        
        st.sidebar.subheader('Crypto:')
        asset = st.sidebar.selectbox('', assets)

        st.sidebar.subheader('Interval:')
        if exchange == 'Binance':
            interval = st.sidebar.selectbox('', ('5 Minute', '15 Minute', '30 Minute', '1 Hour', '1 Day'))
        else:
            interval = st.sidebar.selectbox('', ('5 Minute', '30 Minute', '1 Hour', '1 Day'))
        label = 'Cryptocurrency'

    st.title(f'Automated Technical Analysis for {label} Trading.')
    st.subheader(f'{label} Data Sourced from {exchange} in {interval} Interval.')
    st.info(f'Predicting...')
    
    st.cache(max_entries = 5) 
    future_price = 30   
    analysis = Visualization(exchange, interval, asset, indication, action_model, price_model, market)
    requested_date = analysis.df.index[-1]
    current_price = float(analysis.df['Adj Close'][-1])
    requested_prediction_price = float(analysis.requested_prediction_price)

    if label == 'Stock':
        current_price = f'{float(current_price):,.2f}'
        requested_prediction_price = f'{float(requested_prediction_price):,.2f}'
    else:
        current_price = f'{float(current_price):,.8f}'
        requested_prediction_price = f'{float(requested_prediction_price):,.8f}'

    if analysis.requested_prediction_action == 'Hold':
        present_statement_prefix = 'off from taking any action with'
        present_statement_suffix = ' at this time'
    else:
        present_statement_prefix = ''
        present_statement_suffix = ''
                
    accuracy_threshold = {analysis.score_action: 70., analysis.score_price: 50.}
    confidence = dict()
    for score, threshold in accuracy_threshold.items():
        if float(score) >= threshold:
            confidence[score] = f'*({score}% confident.)*'
        else:
            confidence[score] = ''

    st.markdown(f'**Prediction Date & Time (UTC):** {str(requested_date)}')
    st.markdown(f'**Current Price:** {currency} {current_price}')
    st.markdown(f'**Current Trading Prediction:** You should **{analysis.requested_prediction_action.lower()}** {present_statement_prefix} this {label.lower()[:6]}{present_statement_suffix}. {str(confidence[analysis.score_action])}')
    st.markdown(f'**Future Price Prediction:** The {label.lower()[:6]} price for  **{asset}** is estimated to be **{currency} {requested_prediction_price}** in the next **{int(interval.split()[0]) * future_price} {str(interval.split()[1]).lower()}s**. {str(confidence[analysis.score_price])}')

    st.cache(max_entries = 5)
    prediction_fig = analysis.prediction_graph()
    if indication == 'Predicted':
        testing_prefix = 'Predicted'
    else:
        testing_prefix = 'Analysed'

    st.success(f'Historical {label[:6]} Price Action...({testing_prefix}.)')
    st.plotly_chart(prediction_fig, use_container_width = True)

    technical_analysis_fig = analysis.technical_analysis_graph()
    st.success (f'Technical Analysis results from the {label[:6]} Data...')
    st.plotly_chart(technical_analysis_fig, use_container_width = True)

    st.sidebar.info('Other Options:')
    if st.sidebar.checkbox('The Sourced Data'):
        st.success ('Sourcing...')
        st.markdown(f'Sourced {label} Data.')
        st.write(analysis.df[['High', 'Low', 'Open', 'Volume', 'Adj Close']].tail(10)) 

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    main()