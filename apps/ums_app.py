import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/ums/'
)

app.layout = html.Div(children=[

])

