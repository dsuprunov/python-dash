from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import numpy as np

import config


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)

app.layout = html.Div([
    dcc.Tabs(id='tabs-labels', value='tab-explore', children=[
        dcc.Tab(label='Explore', value='tab-explore'),
        dcc.Tab(label='Visualize', value='tab-visualize'),
        dcc.Tab(label='Export', value='tab-export'),
    ]),
    html.Div(id='tabs-content')
])


@callback(Output('tabs-content', 'children'),
          Input('tabs-labels', 'value'))
def render_tab_content(tab):
    match tab:
        case 'tab-explore':
            df = pd.read_csv(config.DATA_CSV)
            df.replace('?', np.nan, inplace=True)

            return html.Div([
                html.Br(),
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    data=df.to_dict('records'),
                    page_size=10,
                    page_action='native',
                ),
                dcc.Dropdown(
                    id='tab-explore-columns-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value=''
                ),
                html.Div(id='tab-explore-columns-output')
            ])

        case 'tab-visualize':
            return html.Div([
                dcc.Graph(
                    id='tab-visualize-graph',
                    figure={
                        'data': [{
                            'x': [1, 2, 3],
                            'y': [5, 10, 6],
                            'type': 'bar'
                        }]
                    }
                )
            ])

        case 'tab-export':
            return html.Div([
                html.Div('Nothing here yet...')
            ])

        case _:
            html.Div('Oops, something went wrong. You should not see this.')


@app.callback(
    Output('tab-explore-columns-output', 'children'),
    [Input('tab-explore-columns-dropdown', 'value')]
)
def render_explore_content(selected_column):
    if selected_column == '':
        return ''

    df = pd.read_csv(config.DATA_CSV)
    df.replace('?', np.nan, inplace=True)

    if selected_column not in df.columns:
        return ''

    df = df[selected_column].value_counts(normalize=True) * 100
    df = df.reset_index()

    return dcc.Graph(
        id='tab-explore-columns-output-graph',
        figure=px.bar(
            df,
            x=selected_column,
            y='proportion',
            labels={'selected_column': 'Percentage (%)'},
            title='Percentage Distribution'
        ),
    )



if __name__ == '__main__':
    app.run(debug=True)
