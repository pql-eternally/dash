# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div([
    # 单选下拉框
    dcc.Dropdown(
        options=[
            {'label': '春', 'value': '1'},
            {'label': '夏', 'value': '2'},
            {'label': '秋', 'value': '3'},
            {'label': '冬', 'value': '4'},
        ],
        value='2',
        style={
            'width': '200px',
            'height': '100%'
        }
    ),

    # 换行
    html.Br(),

    # 多选下拉框
    dcc.Dropdown(
        options=[
            {'label': '玩游戏', 'value': 'play_game'},
            {'label': '下象棋', 'value': 'play_chess'},
            {'label': '打篮球', 'value': 'play_basketball'},
            {'label': '看电影', 'value': 'watch_movie'},
            {'label': '听音乐', 'value': 'listen_music'},
        ],
        value='listen_music',
        multi=True,
        style={
            'width': '500px',
            'height': '100%'
        }
    ),

    html.Br(),

    # 滑动进度条
    dcc.Slider(
        min=0,
        max=100,
        step=1,
        value=60,
        marks={i: str(i) for i in range(0, 101, 10)}
    ),
    html.Br(),

    # 范围滑块
    dcc.RangeSlider(
        min=0,
        max=100,
        step=2,
        marks={i: str(i) for i in range(0, 101, 5)},
        value=[30, 80]
    ),
    html.Br(),

    # 输入框 input标签
    dcc.Input(
        placeholder='Please Input text...',
        type='text',
        required=True,
        value='Hello Dash'
    ),
    html.Br(),

    # 文本域
    dcc.Textarea(
        placeholder='text area',
        value='',
        style={
            'width': '300px',
        },
        rows=5
    ),
    html.Br(),

    # 多选框
    dcc.Checklist(
        options=[
            {'label': 'python', 'value': 'python'},
            {'label': 'java', 'value': 'java'},
            {'label': 'c', 'value': 'c'},
            {'label': 'c++', 'value': 'c++'},
            {'label': 'ruby', 'value': 'ruby'},
            {'label': 'android', 'value': 'android'},
        ],
        values=['python', 'java', 'android'],
        # 多选框样式
        labelStyle={
            # 可选：inline, block, inline-block
            'display': 'block'
        }
    ),
    html.Br(),

    # 单选按钮
    dcc.RadioItems(
        options=[
            {'label': 'python', 'value': 'python'},
            {'label': 'java', 'value': 'java'},
            {'label': 'c', 'value': 'c'},
            {'label': 'c++', 'value': 'c++'},
            {'label': 'ruby', 'value': 'ruby'},
            {'label': 'android', 'value': 'android'},
        ],
        value='python',
        labelStyle={'display': 'inline-block'}
    ),
    html.Br(),

    #
    dcc.Upload()
])