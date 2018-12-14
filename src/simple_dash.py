import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from components import Header, make_dash_table, print_button
import pandas as pd
import flask
import glob
import os
# from flask_functions import create_scrollable_table, generate_table
import dash_table

image_directory = '../shot_charts/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

image_filename = '../images/all_shots_final.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename1 = '../images/shot_compare.jpg'
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())

image_filename2 = '../images/atlanta_united.jpg'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

app = dash.Dash(__name__)
server = app.server


#tables
fact_dict = {'League': 'Argentina Super League', 'Clubs': 26, 'Number of Players': 625, 'Number of Goals': 321, 'Number of Shots': 3437, 
           'Updated Week': 13}
df_facts = pd.DataFrame(['League: Argentina Super League', 'Teams: 26', 'Players: 625', 'Goals: 373', 'Shots: 3437', 'Updated Week: 15'] ,index = fact_dict.keys(), columns=['Info'])

xg_df = pd.read_csv('../data/xgb_df.csv') #complete table
xg_df.drop(columns=['Unnamed: 0'], inplace=True)
xg_df['total_xG'] = round(xg_df['total_xG'], 2)

top_scorers = xg_df.sort_values(by=['goals'], ascending=False).head(20).copy() #top 20 scorers
top_scorers_dict = {'Top 20 Scorers': {'Shots Per Game': 'Shots Per Game: 2.28', 'Avg xG/Attempt': 'Avg xG/Attempt: 0.16', 'Avg Distance/Attempt (yards)': 'Avg Distance/Attempt: 15.32'},
                    'Rest of League': {'Shots Per Game': 'Shots Per Game: 1.5', 'Avg xG/Attempt': 'Avg xG/Attempt: 0.11', 'Avg Distance/Attempt (yards)': 'Avg Distance/Attempt: 18.04'}}
top_sc_comp = pd.DataFrame(top_scorers_dict)


top_contributors = xg_df.sort_values(by=['total_xG+xA'], ascending=False).head(20).copy() #top 20 total xG + xA
top_per_90 = xg_df[xg_df['total_minutes_played'] > 500].sort_values(by=['xG+xA/90'], ascending=False).copy() #per 90
young_top_20 = xg_df[(xg_df['transfer_value(USD)'] < 8) & (xg_df['total_minutes_played'] >= 300 ) & (xg_df['age'] <= 25)].sort_values(by=['xG+xA/90'], ascending=False).head(20).copy()

## Page layouts

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

overview = html.Div([  # page 1

        # print_button(),

        html.Div([
            Header(),

            # Row 1
            html.Div([

                html.Div([
                    html.H6('Model Summary',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            The xG model is a way to measure each player's contribution \
                            to the rare events that occur in a soccer game. \
                            Expected goal (xG) is the probability of a shot beinga goal, and is calculated \
                            based on factors like distance and angle. Expected assist (xA) \
                            is awarded to any pass directly preceding a   \
                            shot. A pass leading to a shot with an xG of 0.3 will be valued at \
                            0.3 xA. By comparing these metrics to a player's proposed transfer value \
                            and age, high value or high potential players  \
                            may be identified for a potential transfer to the MLS."),

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
                    html.H6('xG vs Actual Goals',  
                            className="gs-header gs-text-header padded"),
                    dcc.Graph(
                        id = "graph-1",
                        figure={
                            'data': [
                                go.Bar(
                                    x = ["XG Boost", "Random Forest", "Gradient Boosting", "Ensemble"],
                                    y = ["407", "377", "384", "389"],
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
                                    y = ["373", "373", "373", "373"],
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
                    html.H6("Average xG of Different Events",  #input static image of makes and misses    
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id="graph-2",
                        figure={
                            'data': [
                                go.Bar(
                                    x = ["Goal (non-pen)", "Assisted Attempt", "Penalty Attempt"],
                                    y = ["0.22", "0.12", "0.91"],
                                    marker = {
                                      "color": "rgb(53, 83, 255)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = "Event True"
                                ),
                                go.Bar(
                                    x = ["Goal (non-pen)", "Assisted Attempt", "Penalty Attempt"],
                                    y = ["0.11", "0.10", "0.11"],
                                    marker = {
                                      "color": "rgb(255, 225, 53)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                        }
                                    },
                                    name = "Event False"
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
                                  "range": [0, 1],
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

            ], className="row "),

            # Row 5 - d
            html.Div([

                html.Div([
                    html.H6('Shot Map',
                            className="gs-header gs-table-header padded"),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
                ], className="twelve columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")


####################################################
top_scorers = html.Div([  # page 2

        html.Div([
            Header(),

            html.Div([

                html.Div([
                    html.H6('Striker Factory',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            South America is famous for producing world class forwards \
                            which provide an essential stream of revenue for South American  \
                            clubs. In 2006, Atlético Madrid paid $22 million for the teenage \
                            Sergio Agüero. Since then, Argentina Superleague has continued to produce \
                            top young attackers; Lautaro Martínez moved to Inter Milan in 2018  \
                            for $16 million while Lucas Alario moved to Germany in 2017 for  \
                            $27 million. Because of this consistent exodus of top talent, \
                            the top goal scorers of the Argentina Super League are mostly composed of \
                            older players with a few up-and-coming stars."),

                ], className="six columns"),

            #     html.Div([
            #         html.H6(["League and Model Facts"],
            #                 className="gs-header gs-table-header padded"),
            #         html.Table(make_dash_table(top_sc_comp))
            #     ], className="six columns"),

            # ], className="row "),

                html.Div([
                    html.H6(["Top 20 vs. Rest of League"],
                            className="gs-header gs-table-header padded"),
                    dash_table.DataTable(
                        id='Top 20 Scorer Comparison',
                        columns=[{"name": i, "id": i} for i in top_sc_comp.columns],
                        data=top_sc_comp.to_dict("rows"),
                        style_cell_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }]
                    )
                ], className="six columns"),

            ], className="row "),

            #next row
            # html.Div([

            #     html.Div([
            #         html.H6("Top 20 Goal Leaders",
            #                 className="gs-header gs-table-header padded"),
            #         dash_table.DataTable(
            #             id = 'Top Contributors',
            #             columns=[{"name": i, "id": i} for i in top_scorers.columns],
            #             data=top_scorers.to_dict("rows"),
            #             css=[{
            #             'selector': '.dash-cell div.dash-cell-value',
            #             'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
            #         }],
            #             style_header={'fontWeight': 'bold'},
            #             style_data_conditional=[{
            #         'if': {'column_id': 'goals'},
            #         'backgroundColor': 'crimson',
            #         'color': 'white',
            #         'fontWeight': 'bold' }],
            #             n_fixed_columns=2,
            #             # style_cell={'textAlign': 'right'},
            #             style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
            #                         'maxHeight': '150', 'maxWidth': '800'},
            #             style_data={'whiteSpace': 'normal'}),
            #         ], className="twelve columns")

            # ], className="row "),

            #next row
                        html.Div([

                html.Div([
                    html.H6("Actual Goal Production vs. Expected Goals(Double Click Top Scorers Above) ",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='xG vs Goals',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=xg_df[xg_df['position_id'] == i]['goals'],
                                    y= xg_df[xg_df['position_id'] == i]['total_xG'],
                                    text= xg_df[xg_df['position_id'] == i]['player_name'],
                                    mode='markers',
                                    opacity=0.7,
                                    marker={
                                        'size': 15,
                                        'line': {'width': 0.5, 'color': 'white'}
                                    },
                                    name= i
                                ) for i in xg_df[xg_df['goals'] >= 2].position_id.unique()
                            ],
                            'layout': go.Layout(
                                xaxis={'title': 'Goals Scored', 'range': [0, 15]},
                                yaxis={'title': 'Predicted Goals', 'range': [0, 15]},
                                margin={'l': 35, 'b': 35, 't': 8, 'r': 8},
                                # legend={'x': 0, 'y': 1},
                                hovermode='closest'
                            )
                        }
                    )
                    
                    ], className="twelve columns")
                
            ], className='row')

        ], className="subpage")

    ], className="page")

            # html.Div([

            #     html.Div([
            #         html.H6('Shot Map',
            #                 className="gs-header gs-table-header padded"),
            #         html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()))
            #     ], className="twelve columns"),

            # ], className="row "),



# total_contributions = html.Div([ # page 3

#         html.Div([

#             Header(),

#             # Row 1

#             html.Div([
#                     html.Div([
#                         html.H6('Goal Creators',
#                             className="gs-header gs-text-header padded"),

#                     html.Br([]),

#                     html.P("\
#                             Shown below is the table of the top 20 contributors in terms \
#                             of combined xG + xA. Out of 20 players in the top scoring   \
#                             list, eight players also make the top 20 of total xG + xA  \
#                             contributions. Through xG + xA, we see that players like Franco Soldano  \
#                             and Germán Herrera have contributed a total of 6.52 and 5.35  \
#                             worth of goal contributions, despite only scoring two goals."),  

#                 ], className="six columns"),

#                     html.Div([html.H6('Contributing',
#                             className="gs-header gs-text-header padded"),

#                     html.Br([]),

#                     html.P("\
#                             The eight players who are top 20 in combined xG + xA but not \
#                             in the top 20 in scoring include Carlos Tevez, Claudio Bieler, \
#                             Franco Soldano, Germán Herrera, Jonatan Cristaldo, Leonardo Sequeira \
#                             Luís Leal, Mariano Pavone, Nicolás Fernández, Nicolás Reniero, \
#                             Santiago García and Sebastián Ribas. Despite none of them scoring \
#                             over 3 goals, the eight players have created an expected value of 4.97  \
#                             goals through shots and passes."),
                            
#                 ], className="six columns"),

#             ],  className="row"),
            
#             #Row 2

#             html.Div([

#                 html.Div([
#                     html.H6("Top xG + xA Contributors",
#                             className="gs-header gs-table-header padded"),
#                     dash_table.DataTable(
#                         id = 'Top Contributors',
#                         columns=[{"name": i, "id": i} for i in top_contributors.columns],
#                         data=top_contributors.to_dict("rows"),
#                         css=[{
#                         'selector': '.dash-cell div.dash-cell-value',
#                         'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
#                     }],
#                         style_data_conditional=[{
#                     'if': {'column_id': 'total_xG+xA'},
#                     'backgroundColor': 'crimson',
#                     'color': 'white',
#                     'fontWeight': 'bold'}],
#                         style_header={'fontWeight': 'bold'},
#                         n_fixed_columns=2,
#                         # style_cell={'textAlign': 'right'},
#                         style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
#                                     'maxHeight': '300', 'maxWidth': '800'},
#                         style_data={'whiteSpace': 'normal'}),
#                     ], className="twelve columns")

#             ], className="row "),

#         ], className="subpage")

#     ], className="page")



per_90 = html.Div([ # page 3

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
                    'backgroundColor': 'crimson',
                    'color': 'white', }],
                        n_fixed_columns=2,
                        style_header={'fontWeight': 'bold'},
                        # style_cell={'textAlign': 'right'},
                        style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
                                    'maxHeight': '300', 'maxWidth': '800'},
                        style_data={'whiteSpace': 'normal'}),
                    ], className="twelve columns")

            ], className="row "),

            # Row 2
            html.Div([

                html.Div([
                    html.H6("xG + xA per 90 Minutes vs Transfer Value (Minimum 300 Minutes)",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='xG+xA/90 vs. transfer_value',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=top_per_90[top_per_90['position_id'] == i]['transfer_value(USD)'],
                                    y=top_per_90[top_per_90['position_id'] == i]['xG+xA/90'],
                                    text= top_per_90[top_per_90['position_id'] == i]['player_name'],
                                    mode='markers',
                                    opacity=0.7,
                                    marker={
                                        'size': 15,
                                        'line': {'width': 0.5, 'color': 'white'}
                                    },
                                    name=i
                                ) for i in top_per_90.position_id.unique()
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

gems = html.Div([ # page 4

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
                        style_header={'fontWeight': 'bold'},
                        css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                        style_data_conditional=[{
                    'if': {'column_id': 'transfer_value(USD)'},
                    'backgroundColor': 'crimson',
                    'color': 'white',
                    'fontWeight': 'bold' 
                    }, 
                    {
                    'if': {'column_id': 'xG+xA/90'},
                    'backgroundColor': 'crimson',
                    'color': 'white',
                    'fontWegiht': 'bold' }],
                        n_fixed_columns=2,
                        # style_cell={'textAlign': 'right'},
                        style_table={'overflowX': 'scroll', 'overflowY': 'scroll',
                                    'maxHeight': '150', 'maxWidth': '800'},
                        style_data={'whiteSpace': 'normal'}),
                    ], className="twelve columns")

            ], className="row "),


            #Row 2
            html.Div([

                html.Div([
                    html.H6("xG + xA per 90 Minutes vs Transfer Value",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='xG+xA/90 vs. transfer_value',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=young_top_20[young_top_20['position_id'] == i]['transfer_value(USD)'],
                                    y=young_top_20[young_top_20['position_id'] == i]['xG+xA/90'],
                                    text= young_top_20[young_top_20['position_id'] == i]['player_name'],
                                    mode='markers',
                                    opacity=0.7,
                                    marker={
                                        'size': 15,
                                        'line': {'width': 0.5, 'color': 'white'}
                                    },
                                    name= i
                                ) for i in young_top_20.position_id.unique()
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

app.config.suppress_callback_exceptions = True

shot_charts = html.Div([ # page 5

        html.Div([

            Header(),

            html.Div([

                html.Div([
                    html.H6("Player Shot Charts",
                            className="gs-header gs-table-header padded"),
                    dcc.Dropdown(
                        id = 'image-dropdown',
                        options=[{'label': i, 'value': i} for i in list_of_images],
                        placeholder='Select player shot chart',
                        value=list_of_images[0]
                    ),
                    html.Img(id='image'),
                ])

            ], className="row ")

        ], className="subpage")

    ], className="page")

about = html.Div([ # page 6

        html.Div([

            Header(),

            # Row 1

            html.Div([
                    html.Div([
                        html.H6('About the Model',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            All shot and player data was gathered from afa.com.ar and   \
                            transfermarkt.co.uk/ . All charts and tables displayed on  \
                            the website are based on the XGBoost model. Some interesting observations \
                            about the model's prediction include the very high value it predicts for  \
                            penalty kicks (0.91 xG versus a worldwide conversation rate closer to 0.75) \
                            and its predictions for top scorers (the top three scorers greatly outperformed \
                            their xG). Whether this is due to luck, or the skill of the top scorers must \
                            be further investigated.  "),  

                ], className="six columns"),

                    html.Div([html.H6('Inspiration',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            The purpose of the expected goal model is to better evaluate  \
                            player contributions so that teams can more confidently invest  \
                            in South American talent. MLS champions Atlanta United, have shown \
                            that doing so not only improves the level of play but also  \
                            provides more revenue to reinvest through future player sales ( Miguel \
                            Almiron purchased for $8m, will move to Europe for $15-20m). \
                            Hopefully other American clubs can follow suit and make the MLS \
                            the stepping stone to Europe, to improve the strength of the \
                            league and generate future transfer fee revenue for reinvestment. "),
                            
                ], className="six columns"),

            ],  className="row"),

            html.Div([

                html.Div([
                    html.H6(' ',
                            className="gs-header gs-table-header padded"),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()))
                ], className="twelve columns"),

            ], className="row "),

            html.Div([

                html.Div([
                    html.H6(' ',
                            className="gs-header gs-table-header padded"),

                html.Br([]),
                html.A('Contact', href='https://www.linkedin.com/in/d-v-dlee/', target='_blank')
                ], className="twelve columns"),

            ], className="row "),

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
    elif pathname == '/argentina_superliga/per_90':
        return per_90
    elif pathname == '/argentina_superliga/gems':
        return gems
    elif pathname == '/argentina_superliga/shot_charts':
        return shot_charts
    elif pathname == '/argentina_superliga/about':
        return about
    elif pathname == '/argentina_superliga/full-view':
        return overview,top_scorers,total_contributions,per_90,gems
    # elif pathname == 'https://www.linkedin.com/in/d-v-dlee/':

    else:
        return overview

#page 5 callbacks
@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])
def update_image_src(value):
    return static_image_route + value

@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)


# # # # # # # # #
# detail the way that external_css and external_js work and link to alternative method locally hosted
# # # # # # # # #

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,300,600",
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
    app.run_server(debug=False)