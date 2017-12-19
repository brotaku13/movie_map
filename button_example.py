import dash
from dash.dependencies import Input, State, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.offline as py
from plotly.graph_objs import *
import networkx as nx

def main():
    """
    Main program: responsible for setting up html divs and app
    :return:
    """
    app = dash.Dash()


    app.layout = html.Div([
        html.Div(id='target', children=''),  # div that shows output
        dcc.Input(id='input', type='text', value='Enter an IMDB hyperlink'),
        html.Button(id='submit', type='submit', children='ok'),
    ])

    #decorator for the search bar
    @app.callback(
        Output(component_id='target', component_property='children'),  # output text, connects to target in html.Div
        [],
        [State('input', 'value')],  # connected to id='input' getting the 'value' property from it
                                    # State('connecting element', value collected)
        [Event('submit', 'click')])  #connected to the html.Button, callback triggered on action
                                     # Event('connecting_id', action)
    def make_map(state): #state variable is the 'value' property from the State in the decorator
        return "callback received value: {}".format(state)

    app.run_server(debug=False)
if __name__ == '__main__':
    main()