import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output


app = dash.Dash()

df = pd.read_csv('all_stocks_2006-01-01_to_2018-01-01.csv')
tickers = df['Name'].unique()
df.set_index(pd.DatetimeIndex(df['Date']), inplace = True)
df.sort_index(inplace = True)

app.layout = html.Div(children = [
    html.H1('Stocks 2006 - 2018'),
    html.Div([
        html.H3('Chose ticker'),
        dcc.Dropdown(
        id = 'ticker_dropdown',
        options = [{'label': i,  'value': i } for i in tickers],
        value = 'AAPL'
    )], style ={'width': '47%', 'padding': '0px, 25px, 0px', 'display': 'inline-block'}),
    html.Div([
        html.H3('Chose graph type'),
        dcc.Dropdown(
        id = 'type_dropdown',
        options = [{'label': 'Volume',  'value': 'Volume'}, 
        {'label': 'Close',  'value': 'Close'}],
        value = 'Volume'
    )], style ={'width': '47%', 'padding': '0px, 25px, 0px', 'display': 'inline-block'}),
    html.Div(id = 'output_ticker', style = {'font-size': 'Large', 'font-weight': 'bold'}),
    dcc.Graph(id = 'stocks_graph')])

@app.callback([Output('stocks_graph', 'figure'),
            Output('output_ticker', component_property='children')],
            [Input('ticker_dropdown', 'value'),
            Input('type_dropdown', 'value')])
def update_figure(ticker, graph_type):
    dff = df[df['Name'] == ticker]

    fig = go.Figure (data = [go.Scatter (x = dff.index, y = dff[graph_type])])

    selected_ticker = '{}'.format(ticker)

    return fig, selected_ticker

if __name__ == '__main__':
    app.run_server(debug =True)