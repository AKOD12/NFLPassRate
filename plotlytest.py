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
   dhc.Label('Select Down(s):'),
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
    dhc.Label('Select Minimum and Maximum Win Probability:'),
     dcc.RangeSlider(
         id='win-prob',
         min=0,
         max=100,
         step=5,
         marks={i: 'WP {}'.format(i) if i == 0 else str(i) for i in range(0, 101,5)},
         value=[25,75],
     ),
    dhc.Div(id='szn-output')
    ],)

@app.callback(
    Output('pass-rate', 'figure'),
    Input('slct-down', 'value')
)

def update_graph(dn):
    pass_data=df.loc[(df.down<(int(dn))+1) & (df.half_seconds_remaining>120) &
                             (df.wp>=0.25) & (df.wp<=0.75)]
    rate=pass_data.groupby('posteam')[['pass']].mean()
    rate.sort_values('pass',ascending=False,inplace=True)

    fig=px.bar(pass_data, x=np.arange(1,33), y=rate['pass'],
    title=f'Pass Rate by Team on Down #{dn}'
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


