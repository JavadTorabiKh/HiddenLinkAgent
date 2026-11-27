"""Find and rank industrial connections between two entities."""
from typing import List, Tuple
import networkx as nx


def find_connections(
    g: nx.DiGraph,
    source: str,
    target: str,
    max_paths: int = 5,
) -> List[List[str]]:
    """Find simple directed paths between source and target.

    Args:
        g: Knowledge graph.
        source: Starting node id.
        target: Ending node id.
        max_paths: Maximum number of paths to return.

    Returns:
        A list of paths, each path is a list of node ids.
    """
    if source not in g or target not in g:
        return []

    paths = []
    # Use shortest simple paths to keep the agent lightweight
    for path in nx.shortest_simple_paths(g, source, target, weight="weight"):
        paths.append(path)
        if len(paths) >= max_paths:
            break
    return paths


def path_to_sentence(g: nx.DiGraph, path: List[str]) -> str:
    """Convert a path into a readable explanation using edge relations."""
    parts = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        relation = g.edges[u, v].get("relation", "relates_to")
        parts.append(f"{g.nodes[u].get('label', u)} --[{relation}]--> {g.nodes[v].get('label', v)}")
    return " ; ".join(parts)