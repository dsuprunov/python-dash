from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
from icecream import ic

import config


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
    dcc.Tabs(id='tabs-main-labels', value='tab-explore', children=[
        dcc.Tab(label='Explore', value='tab-explore'),
        dcc.Tab(label='Visualize', value='tab-visualize'),
        dcc.Tab(label='Export', value='tab-export'),
    ]),
    html.Div(id='tabs-main-content')
])


@callback(Output('tabs-main-content', 'children'),
          Input('tabs-main-labels', 'value'))
def render_tabs_main_content(tab):
    df = pd.read_csv(config.DATA_CSV)
    df.replace('?', np.nan, inplace=True)

    match tab:
        case 'tab-explore':
            return html.Div([
                dcc.Dropdown(
                    df.columns,
                    id='tab-explore-data-filter',
                    value=df.columns,
                    multi=True,
                ),
                dash_table.DataTable(
                    id='tab-explore-data-table',
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    data=df.to_dict('records'),
                    page_size=10,
                    page_action='native',
                ),
                dcc.Dropdown(
                    id='tab-explore-inspect-filter',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=''
                ),
                html.Div(id='tab-explore-inspect-graph'),
            ])

        case 'tab-visualize':
            return html.Div([
                html.Div('Visualize: Nothing here yet...')
            ])

        case 'tab-export':
            return html.Div([
                html.Div('Export: Nothing here yet...')
            ])

        case _:
            html.Div('Oops, something went wrong. You should not see this.')


@callback([Output('tab-explore-data-table', 'columns'),
           Output('tab-explore-inspect-filter', 'options'),
           Output('tab-explore-inspect-graph', 'children')],
          Input('tab-explore-data-filter', 'value'))
def render_tab_explore_data_table(columns):
    if not columns:
        return [], [], html.Div()

    return [{'name': col, 'id': col} for col in columns], columns, html.Div()


if __name__ == '__main__':
    app.run(debug=True)
