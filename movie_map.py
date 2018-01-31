import dash
from dash.dependencies import Input, State, Output, Event
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *
import networkx as nx
import IMDB_Scrapper as scraper


def get_annotation(node):
    """
     Creates the annotation for each node. Title, year, IMDB rating, and syunopsis
     note that year is a placeholder for now
    :param node: a networkx Graph node object
    :return: an annotation (str)
    :param node:
    :return:
    """
    hover_text = '{title}, {year}<br>' \
                 'IMDB score: {score}<br>' \
                 '{summary}<br>'.format(title=node['title'],
                                        year=2018,
                                        score=str(node['rating']),
                                        summary=format_summary_text(node['synopsis']))
    return hover_text


def format_summary_text(summary):
    """
    a tool to format the summary text so that it displays on multuple lines. adds line breaks every 30 characters
    :param summary: a string containing the nodes synopsis information
    :return: a formatted summary with line breaks every 30 characters
    """
    word_list = summary.split(' ')
    line_length = 0
    for i in range(len(word_list)):
        line_length += len(word_list[i])
        if line_length >= 30:
            word_list.insert(i, '<br>')
            line_length = 0

    return ' '.join(word_list)


def build_network(movie_title):
    """
    Builds the network graph. will eventually be comprised of the web scraping tools.
    :param hyperlink: a hyperlink to an IMDB title
    :return: a graph to connect to the dcc.Graph
    """
    #create the shells list for the shell_layout
    shells = []

    # create the networkx Graph recursively by web scraping IMDB
    G = scraper.scraper(movie_title, shells)

    print(shells) # logging

    # creat a dictionary of x,y positions by node
    pos = nx.shell_layout(G, nlist=shells, scale=0.5)
    #  pos is a dictionary { nodeNumber : ([x, y]), ...}

    # initializing and styling the edges for plotting
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=1),
        hoverinfo='none',
        mode='lines'
    )

    xvalues = []
    yvalues = []

    # getting the x, y information from each node and graphing the edges
    for edge in G.edges():  # [(node1, node2), (node3, node4),...]
        x0, y0 = pos[edge[0]]  # pos = { nodeID : [x, y], nodeID : [x, y], ...}
        x1, y1 = pos[edge[1]]

        xvalues += [x0, x1]
        yvalues += [y0, y1]

        edge_trace['x'] += [x0, x1, None]  # adding x and y to scatter plot
        edge_trace['y'] += [y0, y1, None]

    # initializing and styling the scatter plot which will map the nodes.
    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        hovertext=[],
        name='',
        textposition='bottom',
        textfont=dict(
            color='rgb(255, 255, 255)'
        ),
        mode='markers+text',
        marker=Marker(
            showscale=True,
            colorscale=[[0.0, 'rgb(221, 34, 49)'],
                        [0.1111111111111111, 'rgb(218, 58, 30)'],
                        [0.2222222222222222, 'rgb(215, 99, 26)'],
                        [0.3333333333333333, 'rgb(212, 139, 22)'],
                        [0.4444444444444444, 'rgb(209, 180, 19)'],
                        [0.5555555555555556, 'rgb(189, 206, 15)'],
                        [0.6666666666666666, 'rgb(142, 203, 12)'],
                        [0.7777777777777778, 'rgb(94, 200, 9)'],
                        [0.8888888888888888, 'rgb(2, 194, 6)'],
                        [1.0, 'rgb(0, 245, 7)']],
            reversescale=False,
            colorbar=dict(
                title='IMDB Rating',
                titleside='top',
            ),
            color=[],
            size=[],
            sizeref=1,
            line=dict(width=2))
    )

    # function to crete annotated text on hover



    # setting marker information on scatter plot from the networkx Graph object
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)

        node_trace['text'].append(G._node[node]['title'])

        node_trace['hovertext'].append(get_annotation(G._node[node]))

        node_trace['marker']['size'].append(len(G[node]))

        node_trace['marker']['color'].append(G._node[node]['rating'])


    # sizing the nodes
    node_trace['marker']['sizeref'] = max(node_trace['marker']['size']) / 50

    # initializing and styling the figure
    fig = Figure(
        data=[edge_trace, node_trace],
        layout=Layout(
            titlefont=dict(size=16),
            showlegend=False,
            plot_bgcolor='rgb(0,0,0)',
            paper_bgcolor='rgb(0,0,0)',
            hovermode='closest',
            margin={'l': 0, 'r': 0, 't': 10, 'b': 0, 'pad': 0},
            xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    return fig


def main():
    """
    responsible for setting up html divs and app
    :return: void
    """
    app = dash.Dash()

    # initializing and styling Dash App components
    app.layout = html.Div(style={'backgroundColor': 'rgb(0,0,0)'}, children=[
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