# -*- coding: utf-8 -*-

from datetime import datetime
from daisy.utils import datetimeutil

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app


from pymongo import MongoClient
conn = MongoClient("mongodb://127.0.0.1")
db = conn['boss-dev']


def build_daily_figure_data(show_date, show_type, page=1, page_size=10):
    """
    显示日单数据
    :param show_date:
    :param show_type:
    :param page:
    :param page_size:
    :return:
    """
    x_data = []
    y_data_order_quantity = []
    y_data_finish_order_quantity = []
    y_data_cancel_order_quantity = []

    # 将datatime格式化为20190613
    show_date_str = datetimeutil.format_prc(show_date, fmt='%Y%m%d')
    spec = {'date': int(show_date_str)}
    page = max(1, page)
    skip_number = (page - 1) * page_size
    daily_data = db.elem_knight_daily_data.find(spec).limit(10).skip(skip_number)
    for data in daily_data:
        identity_card_id = data['identity_card_id']
        staff = db.staff.find_one({'identity_card_id': identity_card_id})
        if staff:
            staff_name = staff['name']
        else:
            staff_name = 'ID: {}'.format(identity_card_id)
        x_data.append(staff_name)
        y_data_order_quantity.append(data['order_quantity'])
        y_data_finish_order_quantity.append(data['finish_order_quantity'])
        y_data_cancel_order_quantity.append(data['cancel_order_quantity'])

    result = {
        'data': [
            {
                'x': x_data,
                'y': y_data_order_quantity,
                # 显示的提示文本
                'text': [],
                # 显示的名称
                'name': u'总单数',
                # 显示的形状
                'type': show_type,
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
            },
        ],
        'layout': {
            'clickmode': 'event+select'
        }
    }
    return result

layout = html.Div(children=[
    html.Div(children=[
        # 日期选择
        dcc.DatePickerSingle(
            id='date-picker-bill-day',
            date=datetime(2017, 12, 13),
            min_date_allowed=datetime(2017, 12, 13),
            max_date_allowed=datetime.now()
        ),

        html.Div(children=[
            html.Ul(
                className='pagination',
                children=[
                    html.Li(
                        children=html.A(
                            href='#',
                            children='<<'
                        )
                    ),
                    html.Li(
                        children=html.A(
                            href='#',
                            children=1
                        )
                    ),
                    html.Li(
                        children=html.A(
                            href='#',
                            children=2
                        )
                    ),
                    html.Li(
                        children=html.A(
                            href='#',
                            children=3
                        )
                    ),
                    html.Li(
                        children=html.A(
                            href='#',
                            children=4
                        )
                    ),
                    html.Li(
                        children=html.A(
                            href='#',
                            children=5
                        )
                    ),
                    html.Li(
                        children=html.A(
                            href='#',
                            children='>>'
                        )
                    ),
                ]
            )
        ]),
    ]),

    # 折线图
    dcc.Graph(
        id='graph-bill-scatter',
        figure=build_daily_figure_data(datetime(2017, 12, 13), 'scatter'),
    ),

    # 直方图
    dcc.Graph(
        id='graph-bill-bar',
        figure=build_daily_figure_data(datetime(2017, 12, 13), 'bar'),
    ),
])


@app.callback(
    [Output('graph-bill-scatter', 'figure'),
     Output('graph-bill-bar', 'figure')],
    [Input('date-picker-bill-day', 'date')])
def update_figure(selected_day):
    """
    :param selected_day:
    :return:
    """
    # 将2017-12-13转成日期类型
    selected_day = datetimeutil.parse_prc_from_day_str(selected_day, fmt='%Y-%m-%d')
    graph_bill_scatter_data = build_daily_figure_data(selected_day, 'scatter')
    graph_bill_bar_data = build_daily_figure_data(selected_day, 'bar')
    return graph_bill_scatter_data, graph_bill_bar_data
