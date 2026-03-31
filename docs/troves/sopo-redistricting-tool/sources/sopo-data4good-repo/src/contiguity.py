"""
Block adjacency graph and contiguity enforcement.

Two blocks are adjacent if their geometries share a boundary edge
(i.e., they touch along more than a single point).

The adjacency graph is used during capacity balancing to ensure that
reassigning a block does not disconnect a school's zone.
"""
import networkx as nx
import geopandas as gpd
from shapely.geometry import MultiPolygon


def build_adjacency_graph(blocks_gdf: gpd.GeoDataFrame) -> nx.Graph:
    """
    Build a block-adjacency graph from polygon geometries.

    Two blocks are neighbours if they share a boundary of positive length
    (i.e., they share an edge, not just a point vertex).

    Returns: nx.Graph where nodes are block_ids.
    """
    G = nx.Graph()
    block_ids = blocks_gdf["block_id"].tolist()
    G.add_nodes_from(block_ids)

    # Spatial index for fast neighbour lookup
    sindex = blocks_gdf.sindex

    for i, (_, row_i) in enumerate(blocks_gdf.iterrows()):
        bid_i = row_i["block_id"]
        geom_i = row_i["geometry"]

        # Candidate neighbours (bounding box overlap)
        candidates = list(sindex.intersection(geom_i.bounds))
        for j in candidates:
            if j <= i:
                continue
            row_j = blocks_gdf.iloc[j]
            bid_j = row_j["block_id"]
            geom_j = row_j["geometry"]

            # Shared boundary must be a LineString/MultiLineString (length > 0)
            try:
                shared = geom_i.intersection(geom_j)
                if not shared.is_empty and shared.geom_type not in ("Point", "MultiPoint"):
                    G.add_edge(bid_i, bid_j)
            except Exception:
                pass

    return G


def is_zone_contiguous(block_ids_in_zone: list, adjacency: nx.Graph) -> bool:
    """
    Return True if the given block IDs form a connected subgraph.
    """
    if len(block_ids_in_zone) <= 1:
        return True
    subgraph = adjacency.subgraph(block_ids_in_zone)
    return nx.is_connected(subgraph)


def removal_preserves_contiguity(
    block_id: str,
    school_id: str,
    assignments: dict,
    adjacency: nx.Graph,
) -> bool:
    """
    Return True if removing block_id from school_id's zone leaves
    the zone still contiguous (or if the zone has only one block).
    """
    zone_blocks = [b for b, s in assignments.items() if s == school_id and b != block_id]
    if len(zone_blocks) == 0:
        return True
    return is_zone_contiguous(zone_blocks, adjacency)


def addition_is_contiguous(
    block_id: str,
    school_id: str,
    assignments: dict,
    adjacency: nx.Graph,
) -> bool:
    """
    Return True if block_id can be added to school_id's zone while
    preserving contiguity.

    A block can be added if:
      (a) the school's zone is currently empty, OR
      (b) block_id is adjacent to at least one block already in the zone.
    """
    zone_blocks = [b for b, s in assignments.items() if s == school_id]
    if len(zone_blocks) == 0:
        return True
    # block_id must share an edge with at least one block in the zone
    neighbours = set(adjacency.neighbors(block_id))
    return bool(neighbours & set(zone_blocks))


def validate_all_zones(assignments: dict, adjacency: nx.Graph) -> dict:
    """
    Check contiguity for all school zones.

    Returns: {school_id: bool} — True if the zone is contiguous.
    """
    from collections import defaultdict
    zones = defaultdict(list)
    for block_id, school_id in assignments.items():
        if school_id is not None:
            zones[school_id].append(block_id)

    return {sid: is_zone_contiguous(blocks, adjacency)
            for sid, blocks in zones.items()}
