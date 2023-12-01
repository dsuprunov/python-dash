from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
from icecream import ic

import config


df = pd.read_csv(config.DATA_CSV)
df.replace('?', np.nan, inplace=True)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='data-table-columns-filter',
        options=df.columns,
        value=df.columns,
        multi=True,
        placeholder='Select columns to display'
    ),
    dash_table.DataTable(
        id='data-table-content',
        page_current=0,
        page_size=config.DATA_TABLE_PAGE_SIZE,
        page_action='custom',
        sort_action='custom',
        sort_mode='single',
        sort_by=[]
    ),
    dcc.Dropdown(
        id='data-table-inspect-filter',
        options=df.columns,
        value='',
        placeholder='Select column to see distribution'
    ),
    html.Div(id='data-table-inspect-graph'),
])


@callback(
    Output('data-table-columns-filter', 'value'),
    Output('data-table-inspect-filter', 'options'),
    Input('data-table-columns-filter', 'value')
)
def render_data_table_columns_filter(values):
    dff = list(filter(lambda x: x in values, df.columns))

    return dff, [''] + dff


@callback(
    Output('data-table-inspect-filter', 'value'),
    Output('data-table-inspect-graph', 'children'),
    Input('data-table-inspect-filter', 'options'),
    Input('data-table-inspect-filter', 'value'),
)
def render_data_table_inspect_content(options, value):
    if value not in options or value == '':
        return None, None

    dff = df[value].value_counts(normalize=True) * 100
    dff = dff.reset_index()

    return value, dcc.Graph(
        id='data-table-inspect-graph-content',
        figure=px.bar(
            dff,
            x=value,
            y='proportion',
            labels={'selected_column': 'Percentage (%)'},
            title='Percentage Distribution'
        ),
    )


@callback(
    Output('data-table-content', 'columns'),
    Output('data-table-content', 'data'),
    Output('data-table-content', 'sort_by'),
    Input('data-table-content', 'page_current'),
    Input('data-table-content', 'page_size'),
    Input('data-table-content', 'sort_by'),
    Input('data-table-columns-filter', 'value'))
def render_data_table_content(page_current, page_size, sort_by, columns_filter):
    dff = df.loc[:, columns_filter]
    new_sort_by = sort_by

    if len(sort_by):
        if sort_by[0]['column_id'] not in columns_filter:
            new_sort_by = []
        else:
            dff = dff.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )

    columns = [{'name': i, 'id': i} for i in dff.columns]
    data = (dff
            .iloc[page_current * page_size : (page_current + 1) * page_size]
            .to_dict('records')
    )

    return columns, data, new_sort_by


if __name__ == '__main__':
    app.run(debug=True)
