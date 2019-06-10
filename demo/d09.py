# -*- coding:utf-8 -*-

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(
    [
        # 数字输入组件，用于将输入值转换为所需的精度。
        daq.PrecisionInput(
          id='my-daq-precisioninput',
          value=299792458,
          precision=4
        ),
        html.Br(),

        # 颜色选择器
        daq.ColorPicker(
          id='my-daq-colorpicker',
          label="colorPicker"
        ),
        html.Br(),

        # 停止按钮
        daq.StopButton(
          id='my-daq-stopbutton'
        ),
        html.Br(),

        # 切换开关
        daq.ToggleSwitch(
          id='my-daq-toggleswitch'
        ),
        html.Br(),

        # 旋钮组件
        daq.Knob(
          id='my-daq-knob',
          value=8,
          min=0,
          max=10
        ),
        html.Br(),

        # led显示屏
        daq.LEDDisplay(
          id='my-daq-leddisplay',
          value="3.14159265354"
        ),
        html.Br(),

        # 刻度计
        daq.Tank(
          id='my-daq-tank',
          value=5,
          min=0,
          max=10
        ),
        html.Br(),

        # 电源按钮
        daq.PowerButton(
          id='my-daq-powerbutton',
          on=True
        ),
        html.Br(),

        # 温度计
        daq.Thermometer(
          id='my-daq-thermometer',
          value=98.6,
          min=95,
          max=105
        ),
        html.Br(),

        # 指示符:布尔指示灯LED
        daq.Indicator(
          id='my-daq-indicator',
          value=True,
          color="#00cc96"
        ),
        html.Br(),

        # 数字输入组件，可以设置为某个范围之间的值。
        daq.NumericInput(
          id='my-daq-numericinput',
          value=5,
          min=0,
          max=10
        ),
        html.Br(),

        # 渐变条形组件，以百分比形式显示某个范围内的值。
        daq.GraduatedBar(
          id='my-daq-graduatedbar',
          value=4
        ),
        html.Br(),

        # 滑块
        daq.Slider(
          id='my-daq-slider',
          value=17,
          min=0,
          targets={"25": {"label": "TARGET"}},
          max=100
        ),
        html.Br(),

        # 指标组件，指向某个范围之间的某个值。
        daq.Gauge(
          id='my-daq-gauge',
          value=6,
          min=0,
          max=10
        ),
        html.Br(),

        # 开关组件，可在打开和关闭之间切换。
        daq.BooleanSwitch(
          id='my-daq-booleanswitch',
          on=True
        ),
        html.Br(),

    ]
)
