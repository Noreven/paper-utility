import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from dash import callback, Input, Output, html, State, ctx, no_update
from tagger.tagger import parse_csv_for_edit, save_labels

from tagger.tagger import load_csv


def _check_invalid_labels(labels: list):
    return any([label for label in labels if label not in ["0", "1", "2", "TO_READ"]])


def _get_invalid_input(labels: list):
    for index, label in enumerate(labels):
        if label not in ["0", "1", "2", "TO_READ"]:
            return label, index


@callback(
    [
        Output("alert", "children"),
        Output("alert", "is_open"),
        Output("table-data", "data"),
    ],
    [
        Input("save-button", "n_clicks"),
        Input("df-select", "value"),
    ],
    State("table-data", "data"),
    prevent_initial_call=True,
)
def save(_, df_name, data):
    triggered_id = ctx.triggered_id
    if triggered_id == "save-button":
        labels = [row["label"] for row in data]
        if _check_invalid_labels(labels):
            label, index = _get_invalid_input(labels)
            print(label, index)
            return f"ALERT: INVALID INPUT {label} (INDEX: {index})", True, data
        save_labels(labels, df_name)
        reload_df = parse_csv_for_edit(df_name)
        return "", False, reload_df.to_dict("records")
    if triggered_id == "df-select":
        df = parse_csv_for_edit(df_name)
        return "", False, df.to_dict("records")


def alert(label="", index=""):
    text = f"ALERT: INVALID INPUT {label} (INDEX: {index}) "
    return dbc.Alert(
        text,
        id="alert",
        is_open=False,
        style={"text-align": "center"},
    )


def selector():
    return html.Div(
        [
            html.Label("Choose a df: "),
            dbc.Select(
                id="df-select",
                options=[
                    {"label": "RETWEET", "value": "one_or_more_retweet.csv"},
                    {"label": "NO RETWEET", "value": "no_retweet.csv"},
                    {"label": "NEW_TWEET", "value": "new_tweets.csv"},
                ],
                value=0,
            ),
        ],
        style={"border-left": "2rem"},
    )


def table():
    df = parse_csv_for_edit("no_retweet.csv")
    columns = [{"name": i, "id": i} for i in df.columns]
    columns[1].update({"editable": True})
    return DataTable(
        columns=columns,
        id="table-data",
        style_cell={"whiteSpace": "pre-line", "text-align": "left"},
        page_size=20,
    )


def layout():
    return dbc.Container(
        [
            alert(),
            html.Hr(),
            html.Div(
                [
                    selector(),
                    html.Div(
                        [
                            html.Div(
                                "0 = Pro | 1 = Neutral | 2 = Against",
                                style={"margin-right": "10rem"},
                            ),
                        ]
                    ),
                    dbc.Button("save", id="save-button"),
                ],
                style={
                    "display": "flex",
                    "justify-content": "space-between",
                    "margin-right": "2rem",
                    "margin-left": "2rem",
                },
            ),
            html.Hr(),
            table(),
        ],
        style={"border": "1px solid", "margin-left": "16rem", "margin-right": "10rem"},
    )
