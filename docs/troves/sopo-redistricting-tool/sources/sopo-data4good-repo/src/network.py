"""
OSM road network download and travel-distance matrix computation.

Strategy:
  - Download walk + drive networks once, cache to disk.
  - For each school, run single-source Dijkstra from its nearest OSM node.
    This gives O(|schools|) Dijkstra runs instead of O(|blocks| * |schools|).
  - For each block centroid, look up its nearest node distance from
    each school's pre-computed distance dict.
  - Result: distance_matrix[block_id][school_id] = meters
"""
import os
import pickle
import numpy as np
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point

from src.config import STUDY_AREA, CACHE_DIR, WALK_THRESHOLD_METERS


def _cache_path(name: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, name)


def _load_or_build_network(network_type: str):
    """Download OSM network or load from cache."""
    path = _cache_path(f"{network_type}_network.pkl")
    if os.path.exists(path):
        print(f"  Loading cached {network_type} network...")
        with open(path, "rb") as f:
            return pickle.load(f)

    print(f"  Downloading {network_type} network from OSM...")
    G = ox.graph_from_place(STUDY_AREA, network_type=network_type, retain_all=False)
    G = ox.project_graph(G, to_crs="EPSG:32619")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    with open(path, "wb") as f:
        pickle.dump(G, f)
    print(f"  Cached {network_type} network to {path}")
    return G


def _nearest_node(G, x: float, y: float) -> int:
    """Return nearest OSM node id for a projected (x, y) coordinate."""
    return ox.nearest_nodes(G, X=x, Y=y)


def _single_source_distances(G, source_node: int, weight: str) -> dict:
    """
    Run Dijkstra from source_node on G using the given edge weight.
    Returns {node_id: distance_meters}.
    """
    return nx.single_source_dijkstra_path_length(G, source_node, weight=weight)


def build_distance_matrices(blocks_gdf: gpd.GeoDataFrame,
                             schools_gdf: gpd.GeoDataFrame) -> dict:
    """
    Build walk and drive distance matrices.

    Returns:
        {
          "walk": DataFrame[block_id x school_id] = meters,
          "drive": DataFrame[block_id x school_id] = meters,
        }

    Both DataFrames use block_id as index and school_id as columns.
    """
    import pandas as pd

    cache_path = _cache_path("distance_matrices.pkl")
    if os.path.exists(cache_path):
        print("  Loading cached distance matrices...")
        with open(cache_path, "rb") as f:
            return pickle.load(f)

    print("Building distance matrices...")

    G_walk  = _load_or_build_network("walk")
    G_drive = _load_or_build_network("drive")

    block_ids = blocks_gdf["block_id"].tolist()
    school_ids = schools_gdf["school_id"].tolist()

    # Pre-compute nearest OSM node for every block centroid (both networks)
    print("  Snapping block centroids to walk network...")
    block_walk_nodes = {}
    for bid, row in blocks_gdf.iterrows():
        pt = row["centroid_proj"]
        block_walk_nodes[bid] = _nearest_node(G_walk, pt.x, pt.y)

    print("  Snapping block centroids to drive network...")
    block_drive_nodes = {}
    for bid, row in blocks_gdf.iterrows():
        pt = row["centroid_proj"]
        block_drive_nodes[bid] = _nearest_node(G_drive, pt.x, pt.y)

    # Build distance matrices using single-source Dijkstra from each school
    walk_matrix  = {bid: {} for bid in block_ids}
    drive_matrix = {bid: {} for bid in block_ids}

    for sid, srow in schools_gdf.iterrows():
        pt = srow["geometry"]

        # --- Walk network ---
        school_walk_node = _nearest_node(G_walk, pt.x, pt.y)
        print(f"  Walk Dijkstra from {sid}...")
        walk_dists = _single_source_distances(G_walk, school_walk_node, weight="length")
        for bid in block_ids:
            node = block_walk_nodes[bid]
            walk_matrix[bid][sid] = walk_dists.get(node, np.inf)

        # --- Drive network ---
        school_drive_node = _nearest_node(G_drive, pt.x, pt.y)
        print(f"  Drive Dijkstra from {sid}...")
        drive_dists = _single_source_distances(G_drive, school_drive_node, weight="length")
        for bid in block_ids:
            node = block_drive_nodes[bid]
            drive_matrix[bid][sid] = drive_dists.get(node, np.inf)

    walk_df  = pd.DataFrame(walk_matrix).T   # [block_id x school_id]
    drive_df = pd.DataFrame(drive_matrix).T

    result = {"walk": walk_df, "drive": drive_df}

    with open(cache_path, "wb") as f:
        pickle.dump(result, f)
    print(f"  Distance matrices cached to {cache_path}")

    return result


def walkable_mask(walk_df, threshold_m: float = WALK_THRESHOLD_METERS):
    """
    Return a boolean DataFrame[block_id x school_id] indicating
    whether the block is within walking distance of each school.
    """
    return walk_df <= threshold_m
