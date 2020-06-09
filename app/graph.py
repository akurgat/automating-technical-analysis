from _plotly_future_ import v4_subplots
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def prediction_graph(Stock, ticker, data, model_prediction, indication):

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
    fig.add_trace(go.Bar(x = df.index, y = df['Action_Buy'], name = "Buy", opacity = 1,  marker = {'color': '#0BF029'}), secondary_y = False)
    fig.add_trace(go.Bar(x = df.index, y = df['Action_Sell'], name = "Sell", opacity = 1, marker = {'color': '#DB2A07'}), secondary_y = False)
    
    
    fig.update_layout(autosize = False, height = 600, title_text = f"{Stock} to {ticker}", dragmode = False, plot_bgcolor = 'white', hovermode = 'x unified')
    fig.update_xaxes(title_text = "Date")
    fig.update_yaxes(title_text = "Close Price", secondary_y = True)
    fig.update_yaxes(title_text = "Price Action", secondary_y = False, range = [0, 1])

    return fig, df

def technical_analysis_graph(df):

    fig = make_subplots(rows = 3, cols = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['MACD'], name = "MACD (12, 26)", marker = {'color': '#0BF029'}), row = 1, col = 1)
    fig.append_trace(go.Scatter(x = df.index, y = df['MACDS'], name = "MACD Smoothing (9)", marker = {'color': '#DB2A07'}), row = 1, col = 1)
    fig.append_trace(go.Bar(x = df.index, y = df['MACDH'], name = "MACDH", marker = {'color': 'black', 'opacity': 0.6}), row = 1, col = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['RSI'], name = "RSI (14)"), row = 2, col = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['SR_K'], name = "Stochastic K (14, 3)"), row = 3, col = 1)
    fig.append_trace(go.Scatter(x = df.index, y = df['SR_D'], name = "Stochastic_D (3)", marker = {'color': 'skyblue'}), row = 3, col = 1)

    fig.update_layout(title_text = "Technical Analysis", autosize = False, height = 750, dragmode = False, plot_bgcolor = 'white', hovermode = 'closest')

    fig.update_xaxes(title_text = "Date")
    fig.update_yaxes(title_text = "MACD", row = 1, col = 1)
    fig.update_yaxes(title_text = "RSI", range = [0, 100], row = 2, col = 1)
    fig.update_yaxes(title_text = "%K & %D", range = [0, 100], row = 3, col = 1)

    return fig, df