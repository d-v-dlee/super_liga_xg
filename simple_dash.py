import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from components import Header, make_dash_table, print_button

import pandas as pd

from flask_functions import create_scrollable_table, generate_table
import dash_table


app = dash.Dash(__name__)
server = app.server


#tables
fact_dict = {'League': 'Argentina Super Liga', 'Clubs': 26, 'Number of Players': 625, 'Number of Goals': 321, 'Number of Shots': 2955, 
           'Updated Week': 13}
df_facts = pd.DataFrame(['League: Argentina Super Liga', 'Teams: 26', 'Players: 625', 'Goals: 321', 'Shots: 2955', 'Updated Week: 13'] ,index = fact_dict.keys(), columns=['Info'])

xg_df = pd.read_csv('xgboost_table.csv') #complete table
xg_df.drop(columns=['Unnamed: 0'], inplace=True)

top_scorers = xg_df.sort_values(by=['goals'], ascending=False).copy() #top 20 scorers
top_contributors = xg_df.sort_values(by=['total_xG+xA'], ascending=False).copy() #top 20 total xG + xA
top_per_90 = xg_df[xg_df['total_minutes_played'] > 500].sort_values(by=['xG+xA/90'], ascending=False).copy() #per 90
young_top_20 = xg_df[(xg_df['transfer_value(USD)'] < 8) & (xg_df['total_minutes_played'] >= 300 ) & (xg_df['age'] <= 25)].sort_values(by=['xG+xA/90'], ascending=False).head(20).copy()

## Page layouts

overview = html.Div([  # page 1

        # print_button(),

        html.Div([
            Header(),

            # Row 3
            html.Div([

                html.Div([
                    html.H6('Product Summary',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            The xG model is a way to measure each player's contribution \
                            to the rare events that occur in a soccer game. \
                            While goals and assists are a concrete representation of a \
                            player's production, the expected goals (xG) and expected \
                            assists (xA) model tries to better evaluate a player by \
                            calculating the probability of successful events. By doing so,  \
                            and comparing these metrics to their proposed transfer value \
                            (via Transfer Market) and age, high value or high potential players  \
                            may be identified for a potentially transfer to the MLS"),

                ], className="six columns"),

                html.Div([
                    html.H6(["League and Model Facts"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_facts))
                ], className="six columns"),

            ], className="row "),

            # Row 4

            html.Div([

                html.Div([
                    html.H6('Shots and Goals', # need to insert static image   
                            className="gs-header gs-text-header padded"),
                    dcc.Graph(
                        id = "graph-1",
                        figure={
                            'data': [
                                go.Bar(
                                    x = ["XG Boost", "Random Forest", "Gradient Boosting", "Ensemble"],
                                    y = ["382", "325", "316", "341"],
                                    marker = {
                                      "color": "rgb(53, 83, 255)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = "xG Predicted by Different Models"
                                ),
                                go.Bar(
                                    x = ["XG Boost", "Random Forest", "Gradient Boosting", "Ensemble"],
                                    y = ["321", "321", "321", "321"],
                                    marker = {
                                      "color": "rgb(255, 225, 53)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                        }
                                    },
                                    name = "Actual Goals"
                                ),
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                bargap = 0.35,
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0228945952895,
                                  "y": -0.189563896463,
                                  "orientation": "h",
                                  "yanchor": "top"
                                },
                                margin = {
                                  "r": 0,
                                  "t": 20,
                                  "b": 10,
                                  "l": 10
                                },
                                showlegend = True,
                                title = "",
                                width = 340,
                                xaxis = {
                                  "autorange": True,
                                  "range": [-0.5, 4.5],
                                  "showline": True,
                                  "title": "",
                                  "type": "category"
                                },
                                yaxis = {
                                  "autorange": True,
                                  "range": [0, 400],
                                  "showgrid": True,
                                  "showline": True,
                                  "title": "",
                                  "type": "linear",
                                  "zeroline": False
                                }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="six columns"),

                html.Div([
                    html.H6("Shot Data",  #input static image of makes and misses    
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id="graph-2",
                        figure={
                            'data': [
                                go.Scatter(
                                    x = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"],
                                    y = ["10000", "7500", "9000", "10000", "10500", "11000", "14000", "18000", "19000", "20500", "24000"],
                                    line = {"color": "rgb(53, 83, 255)"},
                                    mode = "lines",
                                    name = "500 Index Fund Inv"
                                )
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                title = "",
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                width = 340,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0277108433735,
                                  "y": -0.142606516291,
                                  "orientation": "h"
                                },
                                margin = {
                                  "r": 20,
                                  "t": 20,
                                  "b": 20,
                                  "l": 50
                                },
                                showlegend = True,
                                xaxis = {
                                  "autorange": True,
                                  "linecolor": "rgb(0, 0, 0)",
                                  "linewidth": 1,
                                  "range": [2008, 2018],
                                  "showgrid": False,
                                  "showline": True,
                                  "title": "",
                                  "type": "linear"
                                },
                                yaxis = {
                                  "autorange": False,
                                  "gridcolor": "rgba(127, 127, 127, 0.2)",
                                  "mirror": False,
                                  "nticks": 4,
                                  "range": [0, 30000],
                                  "showgrid": True,
                                  "showline": True,
                                  "ticklen": 10,
                                  "ticks": "outside",
                                  "title": "$",
                                  "type": "linear",
                                  "zeroline": False,
                                  "zerolinewidth": 4
                                }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="six columns"),

            ], className="row ") #potentially delete this

            # Row 5 - deleted

            

        ], className="subpage")

    ], className="page")

####################################################
top_scorers = html.Div([  # page 2

        html.Div([
            Header(),

            html.Div([

                html.Div([
                    html.H6("Top Goal Scorers",
                            className="gs-header gs-table-header padded"),
                    dash_table.DataTable(
                        id = 'Top 5 Scorers',
                        columns=[{"name": i, "id": i} for i in top_scorers.columns],
                        data=top_scorers.to_dict("rows"),
                        n_fixed_columns=2,
                        style_data_conditional=[{
                    'if': {'column_id': 'goals'},
                    'backgroundColor': '#3D9970',
                    'color': 'white', }],
                        css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                        # style_cell={'textAlign': 'right'},
                        style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
                                    'maxHeight': '300'},
                        style_data={'whiteSpace': 'normal'},
                        # css=[{
                        #     'selector': '.dash-cell div.dash-cell-value',
                        #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                        # }]
                    )
                ], className="twelve columns")

            ], className="row "),

        ], className="subpage")

    ], className="page")

total_contributions = html.Div([ # page 3

        html.Div([

            Header(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6("Top xG + xA Contributors",
                            className="gs-header gs-table-header padded"),
                    dash_table.DataTable(
                        id = 'Top Contributors',
                        columns=[{"name": i, "id": i} for i in top_contributors.columns],
                        data=top_contributors.to_dict("rows"),
                        css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                        style_data_conditional=[{
                    'if': {'column_id': 'total_xG+xA'},
                    'backgroundColor': '#3D9970',
                    'color': 'white', }],
                        n_fixed_columns=2,
                        # style_cell={'textAlign': 'right'},
                        style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
                                    'maxHeight': '300'},
                        style_data={'whiteSpace': 'normal'}),
                    ], className="twelve columns")

            ], className="row "),

        ], className="subpage")

    ], className="page")



per_90 = html.Div([ # page 4

        html.Div([

            Header(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6("Top xG+xA/90",
                            className="gs-header gs-table-header padded"),
                    dash_table.DataTable(
                        id = 'Top Contributors',
                        columns=[{"name": i, "id": i} for i in top_per_90.columns],
                        data=top_per_90.to_dict("rows"),
                        css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                        style_data_conditional=[{
                    'if': {'column_id': 'xG+xA/90'},
                    'backgroundColor': '#3D9970',
                    'color': 'white', }],
                        n_fixed_columns=2,
                        # style_cell={'textAlign': 'right'},
                        style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
                                    'maxHeight': '300'},
                        style_data={'whiteSpace': 'normal'}),
                    ], className="twelve columns")

            ], className="row "),

        ], className="subpage")

    ], className="page")

gems = html.Div([ # page 5

        html.Div([

            Header(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6("Top Youngsters by xG+xA/90 with Transfer Value Under $8 Million",
                            className="gs-header gs-table-header padded"),
                    dash_table.DataTable(
                        id = 'Top Youngsters',
                        columns=[{"name": i, "id": i} for i in young_top_20.columns],
                        data=young_top_20.to_dict("rows"),
                        css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                        style_data_conditional=[{
                    'if': {'column_id': 'transfer_value(USD)'},
                    'backgroundColor': '#3D9970',
                    'color': 'white', 
                    }, 
                    {
                    'if': {'column_id': 'xG+xA/90'},
                    'backgroundColor': '#3D9970',
                    'color': 'white', }],
                        n_fixed_columns=2,
                        # style_cell={'textAlign': 'right'},
                        style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
                                    'maxHeight': '300'},
                        style_data={'whiteSpace': 'normal'}),
                    ], className="twelve columns")

            ], className="row "),

            #Row 2
            html.Div([

                html.Div([
                    html.Strong([""]),
                    dcc.Graph(
                        id='xG+xA/90 vs. transfer_value',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=young_top_20[young_top_20['player_name'] == i]['transfer_value(USD)'],
                                    y=young_top_20[young_top_20['player_name'] == i]['xG+xA/90'],
                                    text= young_top_20[young_top_20['player_name'] == i]['player_name'],
                                    mode='markers',
                                    opacity=0.7,
                                    marker={
                                        'size': 15,
                                        'line': {'width': 0.5, 'color': 'white'}
                                    },
                                    name=i
                                ) for i in young_top_20.player_name.unique()
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
                    
                    ], className="twelve columns")
                
            ], className='row')

        ], className="subpage")

    ], className="page")










# Describe the layout, or the UI, of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
# # # # # # # # #
# detail in depth what the callback below is doing
# # # # # # # # #
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/argentina_superliga' or pathname == '/argentina_superliga/overview':
        return overview
    elif pathname == '/argentina_superliga/top_scorers':
        return top_scorers
    elif pathname == '/argentina_superliga/total_contributions':
        return total_contributions
    elif pathname == '/argentina_superliga/per_90':
        return per_90
    elif pathname == '/argentina_superliga/gems':
        return gems
    elif pathname == '/argentina_superliga/about':
        return about
    else:
        return 'noPage'

# # # # # # # # #
# detail the way that external_css and external_js work and link to alternative method locally hosted
# # # # # # # # #

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

# external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#                "https://codepen.io/bcd/pen/YaXojL.js"]

# for js in external_js:
#     app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=True)