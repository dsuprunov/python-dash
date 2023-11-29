import dash
from dash import Input
from dash import Output
from dash import html
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px


import config


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label='Inspect', tab_id='tab-inspect', active_tab_style={'font-weight': 'bold'}),
                    dbc.Tab(label='Visualize', tab_id='tab-visualize', active_tab_style={'font-weight': 'bold'}),
                    dbc.Tab(label='Export', tab_id='tab-export', active_tab_style={'font-weight': 'bold'}),
                ],
                id='card-tabs',
                active_tab='tab-inspect',
            )
        ),
        dbc.CardBody(html.P(id='card-content', className='card-text')),
    ]
)


@app.callback(
    Output('card-content', 'children'),
    [Input('card-tabs', 'active_tab')]
)
def tab_content(active_tab):
    match active_tab:
        case 'tab-inspect':
            return tab_inspect()

        case 'tab-visualize':
            return tab_visualize()

        case 'tab-export':
            return tab_export()

        case _:
            html.P("This shouldn't ever be displayed...")
    return f'This is tab {active_tab}'


def tab_inspect():
    df = pd.read_csv(config.DATA_CSV)
    df.replace('?', np.nan, inplace=True)

    # ToDo: add input to set/select rows per page

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            page_action='native',  # pagination
            # sort_action='native',  # sorting
            # filter_action='native',  # filtering
            # fixed_rows={'headers': True},  # scrolling with fix headers
        )
    ])


def tab_visualize():
    np.random.seed(42)
    df = pd.DataFrame({
        'X': np.random.rand(50),
        'Y': np.random.rand(50),
    })

    return html.Div([
        dcc.Graph(
            id='scatter-plot',
            figure=px.scatter(df, x='X', y='Y', title='Scatter Plot')
        )
    ])


def tab_export():
    return html.Div([
        html.P('Nothing here yet...')
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
