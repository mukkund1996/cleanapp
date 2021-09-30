import dash
import flask
import plotly.express as px
from datetime import date
from dash import dcc, html
from dash.dependencies import Input, Output
from cleanapp import sheets, helpers, config

sheet, records = sheets.get_sheet()
current_date = date.today()

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Clean App"),
    html.Div([
        html.H3("Select your name:"),
        dcc.Dropdown(
            id="name-dropdown",
            options=[
                {"label": "Mukkund", "value": "mukkund"},
                {"label": "Sharanya", "value": "sharanya"},
                {"label": "Shyam", "value": "shyam"},
                {"label": "Giovanni", "value": "giovanni"}
            ], className="dropdown"
        )
    ], className="inline-items sections"),
    dcc.Graph(id="pi-chart"),
    html.Div([html.Div([
        html.Div("Your chore for this week is: "),
        html.Div(id="chore-location", style={"font-weight": "bold"})
    ], className="inline-items"),
        html.Div(id="chore-status", className="inline-items", style={"padding": "2% 0%"}),
        html.Div([
            html.Button(
                "Already Done it!",
                id="done-button",
                n_clicks=0,
                className="button-style",
                style={"background": config.BG_COLORS[0]}
            ),
            html.Button(
                "Undo Changes",
                id="undo-button",
                n_clicks=0,
                className="button-style",
                style={"background": config.BG_COLORS[1], "color": "white"}
            )
        ], className="inline-items")], className="sections", style={"padding": "3% 0%"}),
    html.Div(id="output-name", style={"display": "None"}),
    html.Div(id="chore-count", style={"display": "None"}),
], className="center-elements", id="parent-div")


@app.callback(
    Output("output-name", "children"),
    Input("name-dropdown", "value")
)
def update_output(value):
    return value


@app.callback(
    Output("chore-location", "children"),
    Input("output-name", "children")
)
def update_chore(value):
    return helpers.find_chore(records, current_date, value)


@app.callback(
    Output("chore-count", "children"),
    [Input("done-button", "n_clicks"),
     Input("undo-button", "n_clicks"),
     Input("output-name", "children")]
)
def update_chore(submit_button, undo_button, person_name):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "done-button" in changed_id:
        helpers.update_value(sheet, records, current_date, person_name)
    if "undo-button" in changed_id:
        helpers.update_value(sheet, records, current_date, person_name, value=0)


@app.callback(
    Output("chore-status", "children"),
    Input("name-dropdown", "value")
)
def display_outcome(person_name):
    outcome = helpers.find_outcome(records, current_date, person_name)
    if outcome == 0:
        return "You have yet to do the task."
    elif outcome == -1:
        return "You have chosen to skip the task!"
    else:
        return "You have finished the task!"


@app.callback(
    Output("pi-chart", "figure"),
    Input("name-dropdown", "value"))
def update_figure(person_name):
    if person_name is None:
        return {
            "layout": {
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                },
                "annotations": [
                    {
                        "text": "Please select your name.",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ],
                "height": 400,
                "width": 400,
            }
        }
    filtered_df = records.loc[:current_date.isocalendar()[1]][person_name]
    completed_weeks = int(filtered_df.sum())
    total_weeks = filtered_df.shape[0]
    fig = px.pie(
        values=[completed_weeks, total_weeks],
        names=["Completed", "Incomplete"],
        title="Task Completion Overview",
        height=400,
        width=400
    )
    fig.update_traces(
        hoverinfo="label+percent",
        textinfo="value",
        textfont_size=20,
        marker=dict(colors=config.BG_COLORS,
                    line=dict(color="#FFFFFF", width=2))
    )
    fig.update_layout(transition_duration=500, title_x=0.5)

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
