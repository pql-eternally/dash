# -*- coding:utf-8 -*-

import dash
import dash_table
import pandas as pd

df = pd.read_csv('pql.csv')

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
