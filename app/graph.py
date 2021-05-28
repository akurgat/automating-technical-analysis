from app.model import Prediction
from _plotly_future_ import v4_subplots
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Visualization(Prediction):
    
    def __init__(self, exchange, interval, asset, indication, action_model, price_model, market = None):
        super().__init__(exchange, interval, asset, action_model, price_model, market)  
        super(Visualization, self).get_prediction()
        super(Visualization, self).prediction_postprocessing(indication)

    def prediction_graph(self):
        if self.score_price < 50.:
            future = False
        else:
            future = True

        self.fig_action = make_subplots(specs = [[{"secondary_y": True}]])
        self.fig_action.add_trace(go.Scatter(x = self.df_visulization.index, y = self.df_visulization['Adj Close'], name = "Close Price", connectgaps = False,  
        marker = dict(color = '#000000')), secondary_y = False)

        if future:
            self.fig_action.add_trace(go.Scatter(x = self.df_future_price.index, y = self.df_future_price['Future Price'], name = "Furture Price", 
            connectgaps = False, marker = dict(color = '#A9A9A9', size = 6)), secondary_y = False)

        self.fig_action.add_trace(go.Scatter(x = self.df_visulization.index, y = self.df_visulization['Price_Buy'], mode = 'markers', name = "Buy",  
        marker = dict(color = '#32AB60', opacity = 0.8, size = 7.5)), secondary_y = False)
        self.fig_action.add_trace(go.Scatter(x = self.df_visulization.index, y = self.df_visulization['Price_Sell'], mode = 'markers', name = "Sell", 
        marker = dict(color = '#DB4052', opacity = 0.8, size = 7.5)), secondary_y = False)
        self.fig_action.add_trace(go.Bar(x = self.df_visulization.index, y = self.df_visulization['Volume'], name = "Volume", 
        marker = dict(color = '#5DADE2', opacity = 0.45)), secondary_y = True)

        self.fig_action.update_layout(autosize = False, height = 750, dragmode = False, hovermode = 'x', plot_bgcolor = '#ECF0F1', 
        title = dict(text = f"{self.asset} to {self.market}.", y = 0.95, x = 0.5, xanchor =  'center', yanchor = 'top', font = dict(size = 20)))
        self.fig_action.update_xaxes(title_text = "Date", showline = True, linewidth = 2, linecolor = '#000000', rangeslider_visible = True, 
        range = [self.df_visulization.index.min(), self.df_visulization.index.max()])
        self.fig_action.update_yaxes(title_text = "Close Price & Action", secondary_y = False, showline = True, linewidth = 2, linecolor = '#000000')
        self.fig_action.update_yaxes(title_text = "Volume", secondary_y = True, showline = True, linewidth = 2, linecolor = '#000000')

        return self.fig_action

    def technical_analysis_graph(self):
        self.df_visulization_technical = self.df.iloc[-366:]
        
        self.fig_analysis = make_subplots(rows = 3, cols = 1)
        self.fig_analysis.append_trace(go.Scatter(x = self.df_visulization_technical.index, y = self.df_visulization_technical['MACD'], name = "MACD", 
        marker = dict(color = '#2ECC71')), row = 1, col = 1)
        self.fig_analysis.append_trace(go.Scatter(x = self.df_visulization_technical.index, y = self.df_visulization_technical['MACDS'], name = "MACDS", 
        marker = dict(color = '#E74C3C')), row = 1, col = 1)
        self.fig_analysis.append_trace(go.Bar(x = self.df_visulization_technical.index, y = self.df_visulization_technical['MACDH'], name = "MACDH", 
        marker = dict(color = '#000000')), row = 1, col = 1)
        self.fig_analysis.add_shape(type = 'line', x0 = self.df_visulization_technical.index.min(), x1 = self.df_visulization_technical.index.max(), 
        y0 = 0, y1 = 0, line = dict(color = '#000000', width = 0.5), row = 1, col = 1)

        self.fig_analysis.append_trace(go.Scatter(x = self.df_visulization_technical.index, y = self.df_visulization_technical['RSI'], name = "RSI", 
        marker = dict(color = '#A569BD')), row = 2, col = 1)
        self.fig_analysis.add_shape(type = 'line', x0 = self.df_visulization_technical.index.min(), x1 = self.df_visulization_technical.index.max(), 
        y0 = 30, y1 = 30, line = dict(color = '#008000', width = 1), row = 2, col = 1)
        self.fig_analysis.add_shape(type = 'line', x0 = self.df_visulization_technical.index.min(), x1 = self.df_visulization_technical.index.max(), 
        y0 = 70, y1 = 70, line = dict(color = '#FF0000', width = 1), row = 2, col = 1)

        self.fig_analysis.append_trace(go.Scatter(x = self.df_visulization_technical.index, y = self.df_visulization_technical['SR_K'], name = "Stochastic K", 
        marker = dict(color = '#F39C12')), row = 3, col = 1)
        self.fig_analysis.append_trace(go.Scatter(x = self.df_visulization_technical.index, y = self.df_visulization_technical['SR_D'], name = "Stochastic D", 
        marker = dict(color = '#3780BF')), row = 3, col = 1)
        self.fig_analysis.add_shape(type = 'line', x0 = self.df_visulization_technical.index.min(), x1 = self.df_visulization_technical.index.max(), y0 = 20, y1 = 20, line = dict(color = '#008000', width = 1), row = 3, col = 1)
        self.fig_analysis.add_shape(type = 'line', x0 = self.df_visulization_technical.index.min(), x1 = self.df_visulization_technical.index.max(), y0 = 80, y1 = 80, line = dict(color = '#FF0000', width = 1), row = 3, col = 1)

        self.fig_analysis.update_layout(autosize = False, height = 750, dragmode = False, hovermode = 'x', plot_bgcolor = '#ECF0F1', 
        title = dict(text = "Technical Analysis.", y = 0.95, x = 0.5, xanchor = 'center', yanchor = 'top', font = dict(size = 20)))
        self.fig_analysis.update_shapes(dict(opacity = 0.7))
        self.fig_analysis.update_xaxes(showgrid = True, zeroline = True, showline = True, linewidth = 2, linecolor = '#000000')
        self.fig_analysis.update_xaxes(title_text = "Date", row = 3, col = 1)
        self.fig_analysis.update_yaxes(zeroline = True, showline = True, linewidth = 2, linecolor = '#000000')
        self.fig_analysis.update_yaxes(title_text = "MACD", row = 1, col = 1)
        self.fig_analysis.update_yaxes(title_text = "RSI", range = [0, 100], tickvals = [0, 30, 70, 100], row = 2, col = 1)
        self.fig_analysis.update_yaxes(title_text = "%K & %D", range = [-1, 101], tickvals = [0, 20, 80, 100], row = 3, col = 1)

        return self.fig_analysis
