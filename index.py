import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import staff_app, bill_app, personal_bill_app
from apps.app import app, run

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/staff':
        return staff_app.layout
    elif pathname == '/apps/bill':
        return bill_app.layout
    elif pathname == '/apps/personal_bill':
        return personal_bill_app.layout
    else:
        return '404 Not Found'

if __name__ == '__main__':
    run(app)
