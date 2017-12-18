import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.offline as py
from plotly.graph_objs import *
import networkx as nx

G = nx.balanced_tree(3, 2)

pos = nx.spring_layout(G)
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

#compute midpoint
midx = (max(xvalues) + min(xvalues)) / 2
midy = (max(yvalues) + min(yvalues)) / 2
averageX = sum(xvalues) / len(xvalues)
averageY = sum(yvalues) / len(yvalues)

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    marker=Marker(
        showscale=False,
        colorscale='Earth',
        reversescale=True,
        color=[],
    line=dict(width=2))
)

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'].append(x)
    node_trace['y'].append(y)

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

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Graph(
        id='network shiiiit',
        style={'height': '100vh', 'width': '100vw'},
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)





