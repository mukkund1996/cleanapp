import dash
from datetime import date
from dash import dcc, html
from dash.dependencies import Input, Output
from cleanapp import sheets, helpers
import flask

sheet, records = sheets.get_sheet()

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Clean App"),
    html.Div([html.H3("Select your name:"),
              dcc.Dropdown(
                  id='name-dropdown',
                  options=[
                      {'label': 'Mukkund', 'value': 'mukkund'},
                      {'label': 'Sharanya', 'value': 'sharanya'},
                      {'label': 'Shyam', 'value': 'shyam'},
                      {'label': 'Giovanni', 'value': 'giovanni'}
                  ]
              ),
              ]),
    html.Br(),
    html.Div([html.H3("Your chore for this week is: "), html.Div(id='chore-location')]),
    html.Button('Done', id='done-button', n_clicks=0),
    html.Button('Undo', id='undo-button', n_clicks=0),
    html.Div(id='output-name', style={'display': 'None'}),
    html.Div(id='chore-count', style={'display': 'None'}),
])


@app.callback(
    Output('output-name', 'children'),
    Input('name-dropdown', 'value')
)
def update_output(value):
    return value


@app.callback(
    Output('chore-location', 'children'),
    Input('output-name', 'children')
)
def update_chore(value):
    return helpers.find_chore(records, date.today(), value)


@app.callback(
    Output('chore-count', 'children'),
    [Input('done-button', 'n_clicks'),
     Input('undo-button', 'n_clicks'),
     Input('output-name', 'children')]
)
def update_chore(submit_button, undo_button, person_name):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'done-button' in changed_id:
        helpers.update_value(sheet, records, date.today(), person_name)
    if 'undo-button' in changed_id:
        helpers.update_value(sheet, records, date.today(), person_name, value=0)


if __name__ == '__main__':
    app.run_server(debug=False)
