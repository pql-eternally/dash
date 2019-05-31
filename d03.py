# -*- coding:utf-8 -*-
"""
交互性简介
"""

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()

app.css.append_css({'external_url': "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    dcc.Input(id="num1", value="", type="number"),
    dcc.Input(id="num2", value="", type="number"),
    html.Div(html.Span(id="my-div"))
])


@app.callback(
    Output(component_id="my-div", component_property="children"),
    [Input(component_id="num1", component_property="value"),
     Input(component_id="num2", component_property="value"),]
)
def update_output_div(num1, num2):
    if num1 and num2:
        sum = num1 + num2
    elif num1:
        sum = num1
    elif num2:
        sum = num2
    else:
        sum = 0
    return u'两数相加和为：{}'.format(sum)


if __name__ == '__main__':
    app.run_server(debug=True)