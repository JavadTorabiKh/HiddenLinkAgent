"""Build and load the industrial knowledge graph."""
import json
from pathlib import Path
import networkx as nx


def load_graph(path: str = "data/entities.json") -> nx.DiGraph:
    """Load entities and edges from JSON into a directed graph.

    Args:
        path: Path to the JSON knowledge file.

    Returns:
        A networkx DiGraph with node attributes and weighted edges.
    """
    with open(Path(path), "r", encoding="utf-8") as f:
        data = json.load(f)

    g = nx.DiGraph()

    # Add nodes with their metadata
    for node_id, meta in data["entities"].items():
        g.add_node(node_id, **meta)

    # Add weighted edges
    for edge in data["edges"]:
        g.add_edge(
            edge["source"],
            edge["target"],
            relation=edge["relation"],
            weight=edge.get("weight", 1.0),
        )

    return g


def describe_node(g: nx.DiGraph, node_id: str) -> str:
    """Return a human readable label for a node."""
    return g.nodes[node_id].get("label", node_id)