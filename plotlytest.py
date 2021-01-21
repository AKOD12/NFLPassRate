import pandas as pd 
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as pgo
import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df=pd.read_csv('pbp_2020_labels.csv')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dhc.Div([
   dcc.Graph(id='pass-rate'),
   dhc.Label('Select Season(s):'),
    dcc.RangeSlider(
        id='szn',
        min=2006,
        max=2020,
        step=1,
        marks={i: '{}'.format(i) if i == 2006 else str(i) for i in range(2006,2021)},
        value=[2020,2020]
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
    Output('pass-rate', 'figure'),
    Input('slct-down', 'value'),
    Input('time-remain', 'value'),
    Input('dtg', 'value'),
    Input('win-prob', 'value')
)

def update_graph(dn, time_left, dist, win):
    pass_data=df.loc[(df.down<(int(dn))+1) & (df.half_seconds_remaining>time_left) &
        (df.wp>=(win/100)) & (df.wp<=(1-(win/100))) & (df.ydstogo==dist)]
    rate=pass_data.groupby('posteam')[['pass']].mean()
    rate.sort_values('pass',ascending=False,inplace=True)

    fig=px.bar(pass_data, x=np.arange(1,33), y=rate['pass'],
    title=f'Pass Rate by Team on Down #{dn} with {dist} yards to go Excluding the Final {int(time_left/60)} Minutes of Halves'
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


