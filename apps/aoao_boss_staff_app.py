# -*- coding:utf-8 -*-

import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_table

from dash.dependencies import Input, Output, State
from . import constants
from .app import app

from pymongo import MongoClient
conn = MongoClient("mongodb://127.0.0.1")
db = conn['boss-dev']


def get_platforms():
    """
    获取平台列表
    """
    spec = {
        'state': 100
    }
    platforms = db.platform.find(spec)
    return platforms


def get_suppliers(platform_codes=None):
    """
    获取供应商列表
    :param platform_codes: 平台codes
    :return:
    """

    if not platform_codes:
        return []

    spec = {
        'platform_code': {'$in': platform_codes},
        'state': 100
    }
    suppliers = db.supplier.find(spec)
    return suppliers


def get_cities(platform_codes, supplier_ids):
    """
    获取城市列表
    :param platform_codes: 平台codes
    :param supplier_ids: 供应商ids
    :return:
    """

    if not platform_codes or not supplier_ids:
        return []

    spec = {
        'platform_code': {'$in': platform_codes},
        'supplier_list': {'$in': supplier_ids}
    }
    cities = db.city.find(spec)
    return cities


def get_biz_districts(platform_codes, supplier_ids, city_spellings):
    """
    获取商圈列表
    :param platform_codes: 平台codes
    :param supplier_ids: 供应商ids
    :param city_spellings: 城市代码
    :return:
    """
    if not platform_codes or not supplier_ids or not city_spellings:
        return []

    spec = {
        'platform_code': {'$in': platform_codes},
        'supplier_list': {'$in': supplier_ids},
        'city_spelling': {'$in': city_spellings}
    }
    cities = db.biz_district.find(spec)
    return cities


def get_staff_states():
    """
    员工状态列表
    :return:
    """
    return [
        {'name': u'待签约', 'value': 1},
        {'name': u'已签约-正常', 'value': 100},
        {'name': u'已签约-待换签', 'value': 101},
        {'name': u'已签约-待续签', 'value': 102},
        {'name': u'已签约-待补签', 'value': 103},
        {'name': u'已解约', 'value': -100}
    ]


def find_staffs(spec, page=1, page_size=constants.PAGE_SIZE):
    """
    根据条件查询员工
    :param spec: 查询条件
    :param page: 页数
    :param page_size: 没页数量
    :return:
    """

    page = max(1, page)
    skip_number = (page - 1) * page_size
    staffs = db.staff.find(spec).limit(page_size).skip(skip_number)
    return staffs


def transform_staff_records(spec, page=1, page_size=constants.PAGE_SIZE):
    visible_fields = [column['id'] for column in constants.STAFF_VISIBLE_FIELD_COLUMNS]
    staffs = find_staffs(spec=spec, page=page, page_size=page_size)
    data = []
    for staff in staffs:
        staff_data = {}
        for field in visible_fields:
            staff_data[field] = staff.get(field)
        data.append(staff_data)
    return pd.DataFrame(data)


def build_staff_spec_by_children(form_children):
    """
    构建员工查询条件
    :return:
    """
    spec = {}
    for child in form_children:
        props = child['props']
        element_id = props['id']

        element_value = props['value']
        if not element_value:
            continue

        if element_id == 'platforms':
            spec['platform_list'] = {'$in': element_value}
        elif element_id == 'suppliers':
            spec['supplier_list'] = {'$in': element_value}
        elif element_id == 'cities':
            spec['city_spelling_list'] = {'$in': element_value}
        elif element_id == 'biz_districts':
            spec['biz_district_list'] = {'$in': element_value}
        elif element_id == 'name':
            spec['name'] = element_value
        elif element_id == 'phone':
            spec['phone'] = element_value
        elif element_id == 'state':
            spec['state'] = element_value
    return spec


def build_staff_spec(platform_list, supplier_list, city_spelling_list, biz_district_list, name, phone, state):
    """
    构建员工的查询记录
    :param platform_list:
    :param supplier_list:
    :param city_spelling_list:
    :param biz_district_list:
    :param name:
    :param phone:
    :param state:
    :return:
    """
    spec = {}
    if platform_list:
        spec['platform_list'] = {'$in': platform_list}
    if supplier_list:
        spec['supplier_list'] = {'$in': supplier_list}
    if city_spelling_list:
        spec['city_spelling_list'] = {'$in': city_spelling_list}
    if biz_district_list:
        spec['biz_district_list'] = {'$in': biz_district_list}
    if name:
        spec['name'] = name
    if phone:
        spec['phone'] = phone
    if state:
        spec['state'] = state
    else:
        spec['state'] = {'$ne': -101}
    return spec


layout = html.Div(className='container', children=[
    html.Div(className='jumbotron', children=[
        html.Form(id='search-staff-form', children=[
            html.Div(className='row', children=[
                html.Div(className='col-md-4', children=[
                    # html.Span(
                    #     className='input-group-addon',
                    #     children=u'平台'
                    # ),
                    dcc.Dropdown(
                        id='platforms',
                        placeholder=u'请选择平台',
                        options=[{'label': platform['name'], 'value': platform['platform_code']} for platform in get_platforms()],
                        multi=True,
                        value='',
                    ),
                ]),
                html.Div(className='col-md-4', children=[
                    dcc.Dropdown(
                        id='suppliers',
                        placeholder=u'请选择供应商',
                        multi=True,
                        value=''
                    ),
                ]),
                html.Div(className='col-md-4', children=[
                    dcc.Dropdown(
                        id='cities',
                        placeholder=u'请选择城市',
                        multi=True,
                        value=''
                    ),
                ]),
            ]),
            html.Div(className='row margin-top-10', children=[
                html.Div(className='col-md-4', children=[
                    dcc.Dropdown(
                        id='biz_districts',
                        placeholder=u'请选择商圈',
                        multi=True,
                        value=''
                    ),
                ]),
                html.Div(className='col-md-4', children=[
                    dcc.Input(
                        id='name',
                        placeholder=u'请输入姓名',
                        type='text',
                        value='',
                        style={
                            'width': '100%'
                        }
                    ),
                ]),
                html.Div(className='col-md-4', children=[
                    dcc.Input(
                        id='phone',
                        placeholder=u'请输入手机号',
                        type='tel',
                        value='',
                        style={
                            'width': '100%'
                        }
                    ),
                ]),
            ]),
            html.Div(className='row margin-top-10', children=[html.Div(
                className='col-md-4', children=[
                    dcc.Dropdown(
                        id='state',
                        placeholder=u'请选择签约状态',
                        options=[{'label': staff_state['name'], 'value': staff_state['value']}
                                 for staff_state in get_staff_states()],
                        value=100
                    ),
                ]),
            ]),
        ]),
        html.Div(
            className='col-md-12 split-line margin-top-10'
        ),
        html.Div(className='row margin-top-10 margin-bottom-10', style={'float': 'right'}, children=[
            html.Button(
                id='search_staff',
                className='search-staff-btn btn-success',
                n_clicks=0,
                children=u'查询'
            ),
        ]),
    ]),

    dash_table.DataTable(
        id='table-staff',
        columns=[{'name': column['name'], 'id': column['id']} for column in constants.STAFF_VISIBLE_FIELD_COLUMNS],
        data=transform_staff_records({'state': 100}).to_dict('records'),
        pagination_settings={
            'current_page': 1,
            'page_size': constants.PAGE_SIZE
        },
        # 分页
        pagination_mode='be',
        sorting='be',
        sorting_type='single',
        # 水平滚动时固定的列
        # n_fixed_columns=1,
        # 垂直滚动时固定的列
        # n_fixed_rows=1,
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_cell={
            'whiteSpace': 'no-wrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'minWidth': '20px',
            'maxWidth': '180px',
        },
        style_table={
            'maxWidth': '100%'
        },
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
        style_as_list_view=True
    )
])


@app.callback(
    Output('suppliers', 'options'),
    [Input('platforms', 'value')])
def set_supplier_values(platform_codes):
    suppliers = get_suppliers(platform_codes)
    return [{'label': supplier['name'], 'value': str(supplier['_id'])} for supplier in suppliers]


@app.callback(
    Output('cities', 'options'),
    [Input('platforms', 'value'),
     Input('suppliers', 'value')])
def set_city_values(platform_codes, supplier_ids):
    cities = get_cities(platform_codes, supplier_ids)
    return [{'label': u'{0}-{1}'.format(city['city_name'], city['platform_name']), 'value': city['city_spelling']} for city in cities]


@app.callback(
    Output('biz_districts', 'options'),
    [Input('platforms', 'value'),
     Input('suppliers', 'value'),
     Input('cities', 'value')])
def set_biz_district_value(platform_codes, supplier_ids, city_spellings):
    biz_districts = get_biz_districts(platform_codes, supplier_ids, city_spellings)
    return [{'label': biz_district['name'], 'value': str(biz_district['_id'])} for biz_district in biz_districts]


@app.callback(
    Output('suppliers', 'value'),
    [Input('platforms', 'value')])
def reset_platform(_):
    """
    平台变化，清空供应商选择项
    :param _:
    :return:
    """
    return ''


@app.callback(
    Output('cities', 'value'),
    [Input('suppliers', 'value')])
def reset_supplier(_):
    """
    供应商变化，清空城市选择项
    :param _:
    :return:
    """
    return ''



@app.callback(
    Output('table-staff', 'data'),
    [Input('search_staff', 'n_clicks'),
     Input('table-staff', 'pagination_settings')],
    [State('platforms', 'value'),
     State('suppliers', 'value'),
     State('cities', 'value'),
     State('biz_districts', 'value'),
     State('name', 'value'),
     State('phone', 'value'),
     State('state', 'value')])
def update_table_staff(n_clicks, pagination_settings, platform_list, supplier_list, city_spelling_list,
                       biz_district_list, name, phone, state):
    """
    在点击上一页、下一页、查询时触发更新表格数据
    :param n_clicks: 点击查询按钮时触发，每次值会加1
    :param pagination_settings: dash table 分页设置信息
    :param platform_list:
    :param supplier_list:
    :param city_spelling_list:
    :param biz_district_list:
    :param name:
    :param phone:
    :param state:
    :return:
    """

    page = pagination_settings['current_page']
    page_size = pagination_settings['page_size']
    spec = build_staff_spec(platform_list, supplier_list, city_spelling_list, biz_district_list, name, phone, state)
    df = transform_staff_records(spec, page, page_size)
    return df.to_dict('records')
