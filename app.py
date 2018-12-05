import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from flask_functions import top_20_young

import plotly.plotly as py
import plotly.graph_objs as go

df = top_20_young()

def generate_table(dataframe, max_rows=20):
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div(children=[
#     html.H3(children='Top 20 Young Players by xG+xA/90'),
#     generate_table(df)
# ])

app.layout = html.Div([
    dcc.Graph(
        id='xG+xA/90 vs. transfer_value',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['player_name'] == i]['transfer_value(USD)'],
                    y=df[df['player_name'] == i]['xG+xA/90'],
                    text=df[df['player_name'] == i]['player_name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.player_name.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Transfer Value (M)'},
                yaxis={'title': 'xG + xA per 90 minutes'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                # legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)