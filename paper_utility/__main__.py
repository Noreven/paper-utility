from dash import Dash
import dash_bootstrap_components as dbc
from tagger.frontend.layout import layout


def main():
    app = Dash(__name__, prevent_initial_callbacks=True)
    app.layout = layout()
    return app


if __name__ == "__main__":
    app = main()
    app.run_server(debug=True)
