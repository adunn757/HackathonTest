import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import numpy as np
import pandas as pd

import plotly.express as px

df = pd.read_pickle("prepared_df")
df1 = df[['longitude', 'latitude', 'Latest Rating Overall']].copy()
df1 = df1.dropna()

fig = ff.create_hexbin_mapbox(
    data_frame=df1, lat="latitude", lon="longitude",
    nx_hexagon=15, opacity=0.5, labels={"color": "Average Grade"},
    color='Latest Rating Overall', agg_func=np.mean
)
fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
fig.update_layout(mapbox_style="open-street-map")
fig.write_html('first_figure.html', auto_open=False)

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {'margin-left': '25%', 'margin-right': '5%', 'padding': '20px 10p'}

TEXT_STYLE = {'textAlign': 'center', 'color': '#191970'}

controls = dbc.FormGroup(
    [
        html.P('Variable', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': 'Grade - Overall', 'value': 'Latest Rating Overall'},
                    {'label': 'Grade - Caring', 'value': 'Latest Rating Caring'},
                    {'label': 'Grade - Effective', 'value': 'Latest Rating Effective'},
                    {'label': 'Grade - Responsive', 'value': 'Latest Rating Responsive'},
                    {'label': 'Grade - Safe', 'value': 'Latest Rating Safe'},
                    {'label': 'Grade - Well Led', 'value': 'Latest Rating Well-led'},
                    {'label': 'Number of Care Home Beds', 'value': 'Care homes beds'},],
            value='Latest Rating Overall',  # default value
            multi=False
        ),

        html.Br(),
        html.P('Resolution (Number of Hexagons)', style={'textAlign': 'center'}),
        dcc.RangeSlider(id='range_slider', min = 5, max=100, step=5, value=[15], marks={
            10: '10',
            20: '20',
            30: '30',
            40: '40',
            50: '50',
            60: '60',
            70: '70',
            80: '80',
            90: '90',
            100: '100'}),
    ]
)

sidebar = html.Div([html.H2('Parameters', style=TEXT_STYLE), html.Hr(), controls], style=SIDEBAR_STYLE,)

content_graph = dbc.Row([dbc.Col(dcc.Graph(id='graph_1', figure=fig), md=12,)])

content = html.Div(
    [
        html.H2('Regional Variation In Care Home Data', style=TEXT_STYLE),
        html.Hr(),
        content_graph,
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

@app.callback(
    Output('graph_1', 'figure'),
    [Input('dropdown', 'value'), Input('range_slider', 'value')])
def update_graph_1(dropdown_value, range_slider_value):
    df1 = df[['longitude', 'latitude', dropdown_value]].copy()
    df1 = df1.dropna()

    fig = ff.create_hexbin_mapbox(
        data_frame=df1, lat="latitude", lon="longitude",
        nx_hexagon=range_slider_value[0], opacity=0.5, labels={"color": "Average Grade"},
        color=dropdown_value, agg_func=np.mean
    )
    fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
    fig.update_layout(mapbox_style="open-street-map")
    fig.write_html('first_figure.html', auto_open=False)
    return fig




if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port = 8080)