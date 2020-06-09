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
    
    fig.add_trace(go.Scatter(x = df.index, y = df['Adj Close'], name = "Close Price", connectgaps = False), secondary_y = False)
    fig.add_trace(go.Bar(x = df.index, y = df['Action_Buy'], name = "Buy", opacity = 1,  marker = {'color': '#32AB60', 'opacity' : 0.6}), secondary_y = True)
    fig.add_trace(go.Bar(x = df.index, y = df['Action_Sell'], name = "Sell", opacity = 1, marker = {'color': '#DB4052', 'opacity' : 0.6}), secondary_y = True)
    
    fig.update_layout(autosize = False, height = 750, dragmode = False, hovermode = 'x unified', 
    title = {'text': f"{Stock} to {ticker}.", 'y' : 0.95, 'x' : 0.5, 'xanchor' :  'center', 'yanchor' : 'top', 'font' : {'size' : 20}})

    fig.update_xaxes(title_text = "Date", showline = True, linewidth = 2, linecolor = 'black', rangeslider_visible = True)
    fig.update_yaxes(title_text = "Close Price", secondary_y = False, showline = True, linewidth = 2, linecolor = 'black')
    fig.update_yaxes(title_text = "Price Action", secondary_y = True, range = [0, 1], showline = True, linewidth = 2, linecolor = 'black')

    return fig, df

def technical_analysis_graph(df):

    fig = make_subplots(rows = 3, cols = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['MACD'], name = "MACD", marker = {'color': '#32AB60'}), row = 1, col = 1)
    fig.append_trace(go.Scatter(x = df.index, y = df['MACDS'], name = "MACDS", marker = {'color': '#DB4052'}), row = 1, col = 1)
    fig.append_trace(go.Bar(x = df.index, y = df['MACDH'], name = "MACDH", marker = {'color': 'black'}), row = 1, col = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['RSI'], name = "RSI", marker = {'color': '#800080'}), row = 2, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 30, y1 = 30, line = dict(color = 'black', width = 1), row = 2, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 70, y1 = 70, line = dict(color = 'black', width = 1), row = 2, col = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['SR_K'], name = "Stochastic K", marker = {'color': '#FF9933'}), row = 3, col = 1)
    fig.append_trace(go.Scatter(x = df.index, y = df['SR_D'], name = "Stochastic D", marker = {'color': '#3780BF'}), row = 3, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 20, y1 = 20, line = dict(color = 'black', width = 1), row = 3, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 80, y1 = 80, line = dict(color = 'black', width = 1), row = 3, col = 1)

    fig.update_layout(autosize = False, height = 750, dragmode = False, hovermode = 'closest', 
    title = {'text': "Technical Analysis.", 'y' : 0.95, 'x' : 0.5, 'xanchor' :  'center', 'yanchor' : 'top', 'font' : {'size' : 20}})

    fig.update_xaxes(showgrid = True, zeroline = True, showline = True, linewidth = 2, linecolor = 'black')
    fig.update_xaxes(title_text = "Date", row = 3, col = 1)
    fig.update_yaxes(zeroline = True, showline = True, linewidth = 2, linecolor = 'black')
    fig.update_yaxes(title_text = "MACD", row = 1, col = 1)
    fig.update_yaxes(title_text = "RSI", range = [0, 100], tickvals = [0, 30, 70, 100], row = 2, col = 1)
    fig.update_yaxes(title_text = "%K & %D", range = [0, 100], tickvals = [0, 20, 80, 100], row = 3, col = 1)

    return fig