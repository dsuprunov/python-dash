from dash import Dash
from dash import html
from dash import dash_table
import pandas as pd
import numpy as np

import config


df = pd.read_csv(config.DATA_CSV)
df.replace('?', np.nan, inplace=True)

app = Dash(__name__)
app.layout = html.Div([
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])


if __name__ == '__main__':
    app.run(debug=True)
