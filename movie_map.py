import dash
from dash.dependencies import Input, State, Output, Event
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *
import networkx as nx
import IMDB_Scrapper as scraper

def build_network(hyperlink):
    """
    Builds the network graph. will eventually be comprised of the web scraping tools.
    :param hyperlink: a hyperlink to an IMDB title
    :return: a graph to connect to the dcc.Graph
    """
    shells = []

    G = scraper.scraper(hyperlink, shells)
    print(shells)
    pos = nx.shell_layout(G, shells)

    #  pos is a dictionary { nodeNumber : ([x, y]), ...}

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=1),
        hoverinfo='none',
        mode='lines'
    )

    xvalues = []
    yvalues = []

    for edge in G.edges():  # [(node1, node2), (node3, node4),...]
        x0, y0 = pos[edge[0]]  # pos = { nodeID : [x, y], nodeID : [x, y], ...}
        x1, y1 = pos[edge[1]]

        xvalues += [x0, x1]
        yvalues += [y0, y1]

        edge_trace['x'] += [x0, x1, None]  # adding x and y to scatter plot
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        marker=Marker(

            showscale=True,
            colorscale='Rainbow',

            reversescale=True,
            color=[],
            size=[],
            sizeref=1,
            #sizemode='area',
            line=dict(width=2))
    )

    node_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

        node_text.append(G.node[node]['title'])

        node_trace['marker']['size'].append(len(G[node]))

        node_trace['marker']['color'].append(G._node[node]['rating'])

    node_trace['marker']['sizeref'] = max(node_trace['marker']['size']) / 50

    node_trace['text'] = node_text

    # resizing and nodes based on number of connections
    '''
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'].append(len(adjacencies[1]))
    '''




    # setting up the figure

    fig = Figure(
        data=[edge_trace, node_trace],
        layout=Layout(
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin={'l': 0, 'r': 0, 't': 10, 'b': 0, 'pad': 0},
            xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    return fig

def main():
    """
    Main program: responsible for setting up html divs and app
    :return:
    """
    app = dash.Dash()


    app.layout = html.Div([
        html.Div(id='target'),  # div that shows output
        dcc.Input(id='input', type='text', value=''),
        html.Button(id='submit', type='submit', children='ok'),

        dcc.Graph(
            id='network-graph',
            style={'height': '100vh', 'width': '100vw'}
        )
    ])

    #decorator for the search bar
    @app.callback(
        Output(component_id='network-graph', component_property='figure'),  # output text, connects to target in html.Div
        [],
        [State('input', 'value')],  # connected to id='input' getting the 'value' property from it
                                    # State('connecting element', value collected)
        [Event('submit', 'click')])  #connected to the html.Button, callback triggered on action
                                     # Event('connecting_id', action)
    def make_map(hyperlink): #state variable is the 'value' property from the State in the decorator
        return build_network(hyperlink)

    app.run_server(debug=False)

if __name__ == '__main__':
    main()