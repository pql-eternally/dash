# -*- coding: utf-8 -*-

from datetime import datetime

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from app import app


from pymongo import MongoClient
conn = MongoClient("mongodb://127.0.0.1")
db = conn['boss-dev']


def find_identity_card_ids():
    # identity_card_ids = db.elem_knight_daily_data.group([
    #     {"$group": {"_id" : "$identity_card_id"}},
    #     {'$limit': 10}
    # ])

    daily_data = db.elem_knight_daily_data.find({}).limit(100)
    identity_card_ids = [data['identity_card_id'] for data in daily_data]
    return list(set(identity_card_ids))


def build_personal_figure_data(id_card, show_type='', min_day=20171201, max_day=20171231):
    x_data = []
    y_data_order_quantity = []
    y_data_finish_order_quantity = []
    y_data_cancel_order_quantity = []
    spec = {
        'identity_card_id': id_card,
        'date': {'$gte': min_day, '$lte': max_day},
    }
    daily_data = db.elem_knight_daily_data.find(spec).sort([('date', 1)])
    for data in daily_data:
        current_date = datetime.strptime(str(data['date']), '%Y%m%d')
        day = current_date.day
        x_data.append(day)
        y_data_order_quantity.append(data['order_quantity'])
        y_data_finish_order_quantity.append(data['finish_order_quantity'])
        y_data_cancel_order_quantity.append(data['cancel_order_quantity'])

    return {
        'data': [
            {
                'x': x_data,
                'y': y_data_order_quantity,
                'text': [],
                'name': u'总单数',
                'type': show_type
            },
            {
                'x': x_data,
                'y': y_data_finish_order_quantity,
                'text': [],
                'name': u'完成单数',
                'type': show_type,
            },
            {
                'x': x_data,
                'y': y_data_cancel_order_quantity,
                'text': [],
                'name': u'超时单数',
                'type': show_type,
            }
        ]
    }

layout = html.Div(children=[
    html.Div(
        children=[
            dcc.Dropdown(
                id='dp-id-card',
                options=[{'label': identity_card_id, 'value': identity_card_id} for identity_card_id in find_identity_card_ids()],
                value=''
            ),
            # 折线图
            dcc.Graph(
                id='graph-personal-bill-scatter'
            ),
            # 直方图
            dcc.Graph(
                id='graph-personal-bill-bar',
            ),
        ]),
])


@app.callback(
    [Output('graph-personal-bill-scatter', 'figure'),
     Output('graph-personal-bill-bar', 'figure')],
    [Input('dp-id-card', 'value')])
def update_personal_figure(id_card):
    """

    :param id_card:
    :return:
    """

    return build_personal_figure_data(id_card, 'scatter'), build_personal_figure_data(id_card, 'bar')