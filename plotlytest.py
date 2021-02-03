import pandas as pd 
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as pgo
import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output
import time
import dash_bootstrap_components as dbc  

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

nfl_color_codes = {'ARI':'#97233F','ATL':'#A71930','BAL':'#241773','BUF':'#00338D','CAR':'#0085CA','CHI':'#00143F',
          'CIN':'#FB4F14','CLE':'#FB4F14','DAL':'#B0B7BC','DEN':'#002244','DET':'#046EB4','GB':'#24423C',
          'HOU':'#C9243F','IND':'#003D79','JAX':'#136677','KC':'#CA2430','LA':'#002147','LAC':'#2072BA',
          'LV':'#C4C9CC','MIA':'#0091A0','MIN':'#4F2E84','NE':'#0A2342','NO':'#A08A58','NYG':'#192E6C',
          'NYJ':'#203731','PHI':'#014A53','PIT':'#FFC20E','SEA':'#7AC142','SF':'#C9243F','TB':'#D40909',
          'TEN':'#4095D1','WAS':'#FFC20F'}


app = dash.Dash(title="NFL Situational Pass Rate", external_stylesheets=external_stylesheets)
server=app.server

app.layout = dhc.Div(
   children=[dbc.Spinner(children=[dcc.Graph(id='loading-output')], type='grow'),
   dhc.Label('Select Season:'),
    dcc.Dropdown(
        id='szn',
        options=[
            {'label': '2020', 'value': 2020},
            {'label': '2019', 'value': 2019},
            {'label': '2018', 'value': 2018},
            {'label': '2017', 'value': 2017},
            {'label': '2016', 'value': 2016},
            {'label': '2015', 'value': 2015},
            {'label': '2014', 'value': 2014},
            {'label': '2013', 'value': 2013},
            {'label': '2012', 'value': 2012},
            {'label': '2011', 'value': 2011},
            {'label': '2010', 'value': 2010},
            {'label': '2009', 'value': 2009},
            {'label': '2008', 'value': 2008},
            {'label': '2007', 'value': 2007},
            {'label': '2006', 'value': 2006}
            ],
        value=2020
    ),
   dhc.Label('Select Down:'),
    dcc.Dropdown(
        id='slct-down',
        options=[
            {'label': '1', 'value': 1},
            {'label': '2', 'value': 2},
            {'label': '3', 'value': 3},
            {'label': '4', 'value': 4}
        ],
        value=1
    ),
    dhc.Label('Exclude Plays when One Team has a Win Probability Less Than:'),
     dcc.Slider(
         id='win-prob',
         min=0,
         max=40,
         step=5,
         marks={i: 'WP {}'.format(i) if i == 0 else str(i) for i in range(0, 41,5)},
         value=25,
     ),
    dhc.Label('Select the Amount of Time at the End of Halves that you would like to Exclude:'),
     dcc.Dropdown(
         id='time-remain',
        options=[
            {'label': '0 Minutes', 'value': 0},
            {'label': '1 Minute', 'value': 60},
            {'label': '2 Minutes', 'value': 120},
            {'label': '3 Minutes', 'value': 180},
            {'label': '4 Minutes', 'value': 240},
            {'label': '5 Minutes', 'value': 300}
        ],
        value=120
        ),
    dhc.Label('Select Distance to First Down/Touchdown(Goal to Go Situation):'),
     dcc.Dropdown(
         id='dtg',
         options=[
            {'label': '1 Yard', 'value': 1},
            {'label': '2 Yards', 'value': 2},
            {'label': '3 Yards', 'value': 3},
            {'label': '4 Yards', 'value': 4},
            {'label': '5 Yards', 'value': 5},
            {'label': '6 Yards', 'value': 6},
            {'label': '7 Yards', 'value': 7},
            {'label': '8 Yards', 'value': 8},
            {'label': '9 Yards', 'value': 9},
            {'label': '10 Yards', 'value': 10},
            {'label': '11 Yards', 'value': 11},
            {'label': '12 Yards', 'value': 12},
            {'label': '13 Yards', 'value': 13},
            {'label': '14 Yards', 'value': 14},
            {'label': '15 Yards', 'value': 15},
            {'label': '20 Yards', 'value': 20}
            ],
        value=10
     ),
    ],)

@app.callback(
    Output("loading-output", "figure"),
    Input('slct-down', 'value'),
    Input('time-remain', 'value'),
    Input('dtg', 'value'),
    Input('win-prob', 'value'),
    Input('szn', 'value')
)

def update_graph(dn, time_left, dist, win, season):
    df = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                         'play_by_play_' + str(season) + '.csv.gz?raw=True',
                         compression='gzip', low_memory=False)

    pass_data=df.loc[(df.down==(int(dn))) & (df.half_seconds_remaining>time_left) &
        (df.wp>=(win/100)) & (df.wp<=(1-(win/100))) & (df.ydstogo==dist)]
    rate=pass_data.groupby('posteam')[['pass']].mean()
    rate.sort_values('pass',ascending=False,inplace=True)

    fig=px.bar(pass_data, x=rate.index, y=rate['pass']*100,
    labels={'x': 'Team', 'y': 'Pass Rate (%)'},
    title=f'Pass Rate by Team on Down #{dn} with {dist} yards to go Excluding the Final {int(time_left/60)} Minutes of Halves when the Win Probability is between {win}% and {100-win}%',
    color=rate.index,
    color_discrete_map=nfl_color_codes
    )
    fig.update_traces(showlegend=False)
    fig.add_hline(y=rate['pass'].mean()*100, annotation_text="NFL Average")
    fig.add_annotation(x=20, y=60, text="Figure and Site by Ankith Kodali      Data: @nflfastR")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


