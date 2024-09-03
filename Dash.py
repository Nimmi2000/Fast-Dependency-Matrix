from typing import List, Optional

import ragraph.plot
import plotly.graph_objs as go
import ragraph
from ragraph.io.csv import from_csv
from ragraph.analysis import heuristics
from ragraph.node import Node
from ragraph.edge import Edge
from ragraph.plot.components import Tree, Labels, PieMap, Legend
from ragraph.plot.generic import Style
from ragraph.plot import utils


def get_custom_dsm(
        leafs: List[Node],
        edges: List[Edge],
        nodes_map: List[Node],
        edges_map: List[Edge],
        style: Style = Style(),
        style_map: Style = Style(),
        sort: bool = True,
        node_kinds: Optional[List[str]] = None,
) -> go.Figure:
    if sort:
        leafs = utils.get_axis_sequence(leafs, kinds=node_kinds)

    style.labels.textorientation = "vertical"

    first_row = [
        None,
        None,
        None,
        Labels(leafs, style=style),
        Labels(nodes_map, style=style_map),
        None,
        None,
    ]

    second_row = [
        None,
        None,
        None,
        Labels([Node(str(i + 1)) for i in range(len(leafs))], style=style),
        Labels([Node(str(i + 1)) for i in range(len(leafs), len(leafs) + len(nodes_map))], style=style_map),
        None,
        None,
    ]

    style.labels.textorientation = "horizontal"

    third_row = [
        Tree(leafs, style=style),
        Labels(leafs, style=style),
        Labels([Node(str(i + 1)) for i in range(len(leafs))], style=style),
        PieMap(rows=leafs, cols=leafs, edges=edges, style=style),
        PieMap(rows=leafs, cols=nodes_map, edges=edges_map, style=style_map),
        Legend(edges, style=style),
        Legend(edges_map, style=style_map),
    ]

    fig = utils.get_subplots([first_row, second_row, third_row])

    return utils.process_fig(fig=fig, show=False)


def update_dsm():
    # Converting csv files into a graph object.
    g = from_csv(
        nodes_path=f"assets/without_workstation/nodes.csv",
        edges_path=f"assets/without_workstation/edges.csv",
        csv_delimiter=";",
        iter_delimiter=","  # Separates list elements within a cell.
    )

    g_map_n = from_csv(
        nodes_path=f"assets/without_workstation/nodes_mapping.csv",
        csv_delimiter=";",
        iter_delimiter=","  # Separates list elements within a cell.
    )

    g_map_e = from_csv(
        edges_path=f"assets/without_workstation/mapping_dsm.csv",
        csv_delimiter=";",
        iter_delimiter=","  # Separates list elements within a cell.
    )

    heuristics.markov_gamma(
        graph=g,
        alpha=2.0,  # Expansion parameter.
        beta=4.0,  # Inflation parameter.
        mu=3.0,  # Evaporation parameter.
        gamma=5.0,  # Bus detection parameter.
        inplace=True
    )
    
    heuristics.markov_gamma(
        graph=g,
        root=g["Hardware.node14"],
        alpha=2.5,  # Expansion parameter.
        beta=1.5,  # Inflation parameter.
        mu=3.5,  # Evaporation parameter.
        gamma=3.0,  # Bus detection parameter.
        inplace=True
    )

    g["RGB_Camera"].parent = g["Hardware.node14"]
    g["IR_Camera"].parent = g["Hardware.node14"]
    g["Lidar"].parent = g["Hardware.node14"]

    dsm = get_custom_dsm(
        leafs=g.nodes,
        edges=g.edges,
        nodes_map=g_map_n.nodes,
        edges_map=g_map_e.edges,
        style=ragraph.plot.Style(
            piemap=dict(
                display="labels",
                mode="relative",
                fields=g.edge_labels,
            ),
            palettes=dict(
                fields={
                    "Signal_Control": {"categorical": "#FFF200"},
                    "Signal_Status": {"categorical": "#DECA57"},
                    "Energy_880V": {"categorical": "#228FBE"},
                    "Energy_230V": {"categorical": "#4DADD6"},
                    "Energy_24V": {"categorical": "#A3E0FB"},
                    "Energy_Kinetic": {"categorical": "#005073"},
                    "Spatial": {"categorical": "#FF3FD2"},
                }
            )
        ),
        style_map=ragraph.plot.Style(
            piemap=dict(
                display="labels",
                mode="relative",
                fields=g_map_e.edge_labels,
            ),
            palettes=dict(
                fields={
                    "High_reliability_required": {"categorical": "#ff0000"},
                    "Medium_reliability_required": {"categorical":"#EC9706"},
                    "Low_reliability_required": {"categorical":"#008000"},
                }
            )
        )
    )
    dsm.update_layout(
        legend=dict(
            font=dict(
                size=16  # Adjust as needed
            )
        ),
        xaxis_title="Source",
        yaxis_title="Target",
        xaxis=dict(title=dict(text="", standoff=10)),
        yaxis=dict(title=dict(text="", standoff=10))
    )

    return dsm


dsm_final = update_dsm()

dsm_final.show()
