# -*- coding: utf-8 -*-

from datetime import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc


from pymongo import MongoClient
conn = MongoClient("mongodb://127.0.0.1")
db = conn['boss-dev']

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
    }
]

app = dash.Dash(
    __name__,
    # requests_pathname_prefix='/boss',
    external_stylesheets=external_stylesheets
)


def find_personal_data(identity_card_id):
    x_data = []
    y_data_order_quantity = []
    min_day = 20171201
    max_day = 20171231
    spec = {
        'identity_card_id': identity_card_id,
        'date': {'$gte': min_day, '$lte': max_day},
    }
    daily_data = db.elem_knight_daily_data.find(spec).sort([('date', 1)])
    for data in daily_data:
        current_date = datetime.strptime(str(data['date']), '%Y%m%d')
        day = current_date.day
        x_data.append(day)
        y_data_order_quantity.append(data['order_quantity'])
    return x_data, y_data_order_quantity

layout = html.Div(children=[
    html.Div(
        children=[
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in [1, 2, 3]],
                value='Fertility rate, total (births per woman)'
            ),
            # 折线图
            dcc.Graph(
                id='graph-bill-scatter',
                figure={
                    'data': [
                        {
                            'x': find_personal_data('452427199610223913')[0],
                            'y': find_personal_data('452427199610223913')[1],
                            'text': [],
                            'name': u'总单数',
                            'type': 'scatter',
                        }
                    ],
                    'layout': {
                        'clickmode': 'event+select'
                    }
                }
            ),

            # 直方图
            dcc.Graph(
                id='graph-bill-bar',
            ),
        ]),
])
