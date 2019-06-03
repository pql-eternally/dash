# -*-coding:utf-8-*-

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.development.base_component import Component

from datetime import datetime as dt

app = dash.Dash()

app.layout = html.Div([
    # type: ["text","number","password","email","range","search","tel","url","hidden"].
    dcc.Input(id="id-year", value="2015-09-24", type="text"),
    dcc.DatePickerRange(
        id="birthday-range",
        start_date=dt(1990, 1, 1),
        end_date=dt(2019, 6, 1),
        start_date_placeholder_text='xyy',
        end_date_placeholder_text='pql',
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)