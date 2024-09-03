# Importing the required method.
from ragraph.io.csv import from_csv
import ragraph.plot 
from ragraph.analysis import heuristics


def print_nodes(g: ragraph.graph.Graph) -> None:
    """
    Function to print the node and edge objects of a graph.

    Parameters:
    g (Graph): The graph object.

    Returns:
    None
    """
    # Let's print the node objects of the graph.
    print("Node object names stored within g:")
    for idx, node in enumerate(g.nodes):
        print(" {}.".format(idx), node.name)
    print("")

    # Lets print the edge objects data of the graph.
    print("Edge information stored within g:")
    for idx, edge in enumerate(g.edges):
        print(" {}.".format(idx), edge.source.name, edge.target.name, edge.kind, edge.labels, edge.annotations.motivation)
    print("")

# Converting csv files into a graph object. 
g = from_csv(
    nodes_path="assets/nodes_new.csv",
    edges_path="assets/edges_new.csv",
    csv_delimiter=";",
    iter_delimiter=","  # Separates list elements within a cell.  
)

# Clustering the graph. 
roots = heuristics.markov_gamma(
    graph=g, 
    alpha=2,    # Expension parameter.
    beta=2.0,   # Inflation parameter.
    mu=2.0,     # Evaporation parameter.
    gamma=2.0,   # Bus detection parameter.
    inplace=True
)

# Then when plotting
dsm = ragraph.plot.dsm(
    # show = True,
    leafs = g.nodes,
    edges = g.edges,
    style= ragraph.plot.Style(
        piemap=dict(
            display="labels",
            mode= "relative",
            fields=g.edge_labels,
        ),
    )
)

print(type(dsm))

dsm.layout.autosize = True

print(dsm.layout.autosize)