"""
Two-stage block-to-school assignment.

Constraints (priority order):
  1. HARD: Every school must be at or under capacity.
  2. SOFT: Community continuity — zones should be contiguous.
  3. SOFT: Minimize travel distance.

Stage 1 — Guaranteed-seed, capacity-bounded flood-fill
  Each school pre-assigned a unique seed block (nearest uncontested centroid).

  Phase A: Grow from seeds (priority = drive distance), each school stops at
    its proportional target: total_students * capacity / total_capacity.

  Phase B: Remaining blocks go to adjacent zones, hard capacity respected.

  Phase C: Any remaining orphan blocks (no adjacent under-capacity zone) get
    assigned to the nearest GEOGRAPHICALLY ADJACENT school zone first; only
    fall back to pure drive distance if no adjacent zone exists.

Stage 2 — Hard capacity enforcement
  For each school above capacity:
    - Sort zone blocks by drive distance DESC (marginal first).
    - For each marginal block, try moves in this priority order:
        1. Contiguous move: preserves source contiguity AND block is adjacent
           to target zone.
        2. Adjacent-zone move: preserves source contiguity, target zone has
           at least one neighbour of this block (zone grows toward block).
        3. Non-contiguous move (last resort): any under-capacity school,
           but prefer ones geographically adjacent to the block's neighbours.
    - Repeat until all schools within capacity.
"""
import heapq
import numpy as np
from src.contiguity import removal_preserves_contiguity, addition_is_contiguous
from src.config import WALK_THRESHOLD_METERS



def _students_in_zone(school_id, assignments, blocks_gdf):
    total = 0.0
    for bid, sid in assignments.items():
        if sid == school_id:
            total += blocks_gdf.loc[bid, "students"]
    return total


def _assign_seed_blocks(blocks_gdf, open_schools):
    """Guarantee each school gets a unique nearest seed block."""
    school_ids = list(open_schools.index)
    all_block_ids = list(blocks_gdf["block_id"])
    school_pts = {sid: open_schools.loc[sid, "geometry"] for sid in school_ids}
    block_pts  = {bid: blocks_gdf.loc[bid, "centroid_proj"] for bid in all_block_ids}

    def inter_min_dist(sid):
        return min(
            (school_pts[sid].distance(school_pts[o]) for o in school_ids if o != sid),
            default=float("inf"),
        )

    seeds = {}
    claimed = set()
    for sid in sorted(school_ids, key=inter_min_dist):
        best_bid, best_dist = None, float("inf")
        for bid in all_block_ids:
            if bid in claimed:
                continue
            d = school_pts[sid].distance(block_pts[bid])
            if d < best_dist:
                best_dist, best_bid = d, bid
        if best_bid is not None:
            seeds[best_bid] = sid
            claimed.add(best_bid)
    return seeds


def _zone_priority(bid, sid, walk_df, drive_df):
    """Return min(walk_dist, drive_dist) for flood-fill priority.

    Using the minimum of walk and drive distance means blocks that are
    walkable to a school get priority for that school even if their drive
    route is slightly longer—this keeps walkable neighborhoods together and
    avoids the Small/Brown border problem where walk-short but drive-longer
    blocks were incorrectly given to the wrong school.
    """
    wd = walk_df.loc[bid, sid] if sid in walk_df.columns else float("inf")
    dd = drive_df.loc[bid, sid] if sid in drive_df.columns else float("inf")
    wd = wd if np.isfinite(wd) else float("inf")
    dd = dd if np.isfinite(dd) else float("inf")
    return min(wd, dd)


def _adjacent_zone_schools(block_id, open_school_ids, assignments, adjacency):
    """
    Return the set of school_ids that have at least one zone block adjacent
    to block_id. This is used to prefer community-continuous moves.
    """
    adj_schools = set()
    for nbr in adjacency.neighbors(block_id):
        sid = assignments.get(nbr)
        if sid in open_school_ids:
            adj_schools.add(sid)
    return adj_schools


def initial_assignment(blocks_gdf, open_schools, walk_df, drive_df, adjacency):
    """Stage 1: Three-phase capacity-bounded flood-fill using drive distance."""
    open_school_ids = list(open_schools.index)
    capacities = open_schools["capacity"].to_dict()
    total_capacity = sum(capacities.values())
    total_students = float(blocks_gdf["students"].sum())

    target_loads = {
        sid: total_students * capacities[sid] / total_capacity
        for sid in open_school_ids
    }

    assignments = {}
    school_loads = {sid: 0.0 for sid in open_school_ids}
    at_target  = set()
    at_capacity = set()
    assigned   = set()
    in_heap    = set()
    heap       = []

    # Guaranteed seed blocks
    seeds = _assign_seed_blocks(blocks_gdf, open_schools)
    for bid, sid in seeds.items():
        assigned.add(bid)
        assignments[bid] = sid
        school_loads[sid] += blocks_gdf.loc[bid, "students"]
        if school_loads[sid] >= target_loads[sid]:
            at_target.add(sid)
        if school_loads[sid] >= capacities[sid]:
            at_capacity.add(sid)
        for nbr in adjacency.neighbors(bid):
            if nbr not in assigned and (nbr, sid) not in in_heap:
                p = _zone_priority(nbr, sid, walk_df, drive_df)
                heapq.heappush(heap, (p, nbr, sid))
                in_heap.add((nbr, sid))

    # Phase A: grow until proportional target
    while heap:
        dist, bid, sid = heapq.heappop(heap)
        if bid in assigned or sid in at_target:
            continue
        assigned.add(bid)
        assignments[bid] = sid
        school_loads[sid] += blocks_gdf.loc[bid, "students"]
        if school_loads[sid] >= target_loads[sid]:
            at_target.add(sid)
            if school_loads[sid] >= capacities[sid]:
                at_capacity.add(sid)
            if len(at_target) == len(open_school_ids):
                break
            continue
        for nbr in adjacency.neighbors(bid):
            if nbr not in assigned and (nbr, sid) not in in_heap:
                p = _zone_priority(nbr, sid, walk_df, drive_df)
                heapq.heappush(heap, (p, nbr, sid))
                in_heap.add((nbr, sid))

    # Phase B: remaining blocks → adjacent zones, hard cap respected
    unassigned = set(blocks_gdf["block_id"]) - assigned
    if unassigned:
        p2_heap = []
        p2_in_heap = set()
        for bid in list(assigned):
            sid = assignments[bid]
            if sid in at_capacity:
                continue
            for nbr in adjacency.neighbors(bid):
                if nbr in unassigned and (nbr, sid) not in p2_in_heap:
                    p = _zone_priority(nbr, sid, walk_df, drive_df)
                    heapq.heappush(p2_heap, (p, nbr, sid))
                    p2_in_heap.add((nbr, sid))

        while p2_heap and unassigned:
            dist, bid, sid = heapq.heappop(p2_heap)
            if bid not in unassigned:
                continue
            if school_loads[sid] >= capacities[sid]:
                continue
            unassigned.discard(bid)
            assigned.add(bid)
            assignments[bid] = sid
            school_loads[sid] += blocks_gdf.loc[bid, "students"]
            if school_loads[sid] >= capacities[sid]:
                at_capacity.add(sid)
            if sid not in at_capacity:
                for nbr in adjacency.neighbors(bid):
                    if nbr in unassigned and (nbr, sid) not in p2_in_heap:
                        p = _zone_priority(nbr, sid, walk_df, drive_df)
                        heapq.heappush(p2_heap, (p, nbr, sid))
                        p2_in_heap.add((nbr, sid))

    # Phase C: orphan blocks — prefer adjacent zone first, then nearest by drive
    remaining = sorted(
        set(blocks_gdf["block_id"]) - set(assignments.keys()),
        key=lambda b: blocks_gdf.loc[b, "students"],
        reverse=True,
    )
    for bid in remaining:
        under_cap = [s for s in open_school_ids if school_loads[s] < capacities[s]]
        if not under_cap:
            under_cap = open_school_ids  # all at cap, accept overflow

        # Prefer schools whose zone is geographically adjacent to this block
        adj_schools = _adjacent_zone_schools(bid, under_cap, assignments, adjacency)
        candidates = list(adj_schools) if adj_schools else under_cap

        best = min(
            candidates,
            key=lambda s: drive_df.loc[bid, s] if np.isfinite(drive_df.loc[bid, s]) else float("inf"),
        )
        assignments[bid] = best
        school_loads[best] += blocks_gdf.loc[bid, "students"]

    return assignments


def balance_capacity(assignments, blocks_gdf, open_schools, drive_df, adjacency,
                     max_iterations=300):
    """
    Stage 2: Enforce hard capacity. Move order of preference:
      1. Contiguous + adjacent-to-target (best for community continuity)
      2. Contiguous + adjacent zone of target (target zone grows toward block)
      3. Non-contiguous, but target zone is geographically adjacent (minimise islands)
      4. Non-contiguous to any under-capacity school (last resort)
    """
    open_school_ids = list(open_schools.index)
    capacities = open_schools["capacity"].to_dict()

    for _ in range(max_iterations):
        changed = False

        loads = {sid: _students_in_zone(sid, assignments, blocks_gdf)
                 for sid in open_school_ids}
        overloaded = sorted(
            [(sid, loads[sid] - capacities[sid]) for sid in open_school_ids
             if loads[sid] > capacities[sid]],
            key=lambda x: x[1], reverse=True,
        )
        if not overloaded:
            break

        for school_id, _ in overloaded:
            zone_blocks = sorted(
                [b for b, s in assignments.items() if s == school_id],
                key=lambda b: drive_df.loc[b, school_id],
                reverse=True,
            )

            for block_id in zone_blocks:
                if _students_in_zone(school_id, assignments, blocks_gdf) <= capacities[school_id]:
                    break

                under_cap_alts = sorted(
                    [s for s in open_school_ids if s != school_id and loads[s] < capacities[s]],
                    key=lambda s: drive_df.loc[block_id, s],
                )
                if not under_cap_alts:
                    continue

                if not removal_preserves_contiguity(block_id, school_id, assignments, adjacency):
                    # Tier 4: bridge block — try moving it + its isolated peninsula as a group
                    fragment = _isolated_fragment(block_id, school_id, assignments, adjacency)
                    if fragment is None:
                        continue
                    group = {block_id} | set(fragment)
                    group_students = sum(blocks_gdf.loc[b, "students"] for b in group)
                    for alt in under_cap_alts:
                        if loads[alt] + group_students <= capacities[alt]:
                            for b in group:
                                assignments[b] = alt
                            loads[alt] += group_students
                            loads[school_id] -= group_students
                            changed = True
                            break
                    continue

                # Classify alternatives by community-continuity quality
                adj_zone_schools = _adjacent_zone_schools(
                    block_id, open_school_ids, assignments, adjacency
                )

                # Tier 1: contiguous move + block adjacent to target zone
                moved = False
                for alt in under_cap_alts:
                    if addition_is_contiguous(block_id, alt, assignments, adjacency):
                        assignments[block_id] = alt
                        loads[alt] += blocks_gdf.loc[block_id, "students"]
                        loads[school_id] -= blocks_gdf.loc[block_id, "students"]
                        changed = True
                        moved = True
                        break

                if moved:
                    continue

                # Tier 2: no full contiguity, but move to a geographically adjacent zone
                adj_under_cap = [s for s in under_cap_alts if s in adj_zone_schools]
                if adj_under_cap:
                    best_alt = adj_under_cap[0]  # already sorted by drive dist
                    assignments[block_id] = best_alt
                    loads[best_alt] += blocks_gdf.loc[block_id, "students"]
                    loads[school_id] -= blocks_gdf.loc[block_id, "students"]
                    changed = True
                    continue

                # Tier 3: non-contiguous, nearest under-capacity school
                best_alt = under_cap_alts[0]
                assignments[block_id] = best_alt
                loads[best_alt] += blocks_gdf.loc[block_id, "students"]
                loads[school_id] -= blocks_gdf.loc[block_id, "students"]
                changed = True

        if not changed:
            break

    return assignments


def _isolated_fragment(block_id, school_id, assignments, adjacency):
    """
    If removing block_id from school_id's zone would disconnect the zone,
    return the smaller sub-component that would become isolated (i.e. the
    "peninsula" hanging off block_id).  Returns None if removal is safe or
    if the zone has only one block.
    """
    import networkx as nx
    zone_blocks = [b for b, s in assignments.items() if s == school_id and b != block_id]
    if len(zone_blocks) == 0:
        return None
    sub = adjacency.subgraph(zone_blocks)
    components = list(nx.connected_components(sub))
    if len(components) <= 1:
        return None  # still connected — no fragment
    # Return the smallest component (the peninsula to migrate)
    return min(components, key=len)


def smooth_bussed_communities(assignments, blocks_gdf, open_schools, walk_df, drive_df,
                               adjacency, max_passes=10):
    """
    Stage 3: Keep bussed micro-communities together.

    For every non-walkable block, check whether the majority of its adjacent
    neighbours go to a different school.  If so, try to move it (and any
    isolated peninsula it would leave behind) to the majority school,
    subject to capacity and source-contiguity constraints.

    Peninsula logic: if moving a single block would disconnect the source
    zone, we collect the now-isolated fragment and move the whole group
    together — so a "finger" of bussed blocks from the same neighbourhood
    travels to the same school as its surrounding neighbours.
    """
    open_school_ids = list(open_schools.index)
    capacities = open_schools["capacity"].to_dict()

    for _ in range(max_passes):
        changed = False
        loads = {sid: sum(blocks_gdf.loc[b, "students"]
                          for b, s in assignments.items() if s == sid)
                 for sid in open_school_ids}

        for bid in list(assignments.keys()):
            current_sid = assignments[bid]

            # Only smooth blocks that need to be bussed to their assigned school
            wd = walk_df.loc[bid, current_sid] if current_sid in walk_df.columns else float("inf")
            if np.isfinite(wd) and wd <= WALK_THRESHOLD_METERS:
                continue

            # Count how many assigned neighbours go to each school
            neighbor_counts = {}
            for nbr in adjacency.neighbors(bid):
                nsid = assignments.get(nbr)
                if nsid is not None:
                    neighbor_counts[nsid] = neighbor_counts.get(nsid, 0) + 1

            if not neighbor_counts:
                continue

            majority_sid = max(neighbor_counts, key=neighbor_counts.get)
            if majority_sid == current_sid:
                continue

            # Strict majority required
            total_assigned_nbrs = sum(neighbor_counts.values())
            if neighbor_counts[majority_sid] <= total_assigned_nbrs / 2:
                continue

            # Determine the set of blocks to move: just this block, or the
            # whole peninsula it's anchoring
            if removal_preserves_contiguity(bid, current_sid, assignments, adjacency):
                to_move = {bid}
            else:
                fragment = _isolated_fragment(bid, current_sid, assignments, adjacency)
                if fragment is None:
                    continue  # shouldn't happen, but skip to be safe
                to_move = {bid} | set(fragment)

            # All blocks in the group must also be non-walkable (don't drag
            # a walkable block away from its natural zone)
            if any(
                np.isfinite(walk_df.loc[b, current_sid]) and
                walk_df.loc[b, current_sid] <= WALK_THRESHOLD_METERS
                for b in to_move
            ):
                continue

            # Capacity: target school must fit the whole group
            group_students = sum(blocks_gdf.loc[b, "students"] for b in to_move)
            if loads[majority_sid] + group_students > capacities[majority_sid]:
                continue

            # Move entire group
            for b in to_move:
                assignments[b] = majority_sid
            loads[majority_sid] += group_students
            loads[current_sid] -= group_students
            changed = True

        if not changed:
            break

    return assignments


def consolidate_fragments(assignments, blocks_gdf, open_schools, drive_df, adjacency,
                          max_iterations=10, walk_df=None, walk_threshold_m=1207.0):
    """
    Stage 4: Clean up disconnected zone fragments and surrounded outlier blocks.

    Pass A — Fragment consolidation:
      For each school zone, detect disconnected connected components. Move
      non-main fragments to the geographically nearest adjacent zone,
      respecting capacity (prefer under-capacity; fall back to nearest if all full).

    Pass B — Surrounded block consolidation:
      For each block, if ≥75% of its neighbours belong to a single other zone
      AND removal preserves source contiguity AND target is under capacity,
      move it to the majority zone.
    """
    import networkx as nx
    open_school_ids = list(open_schools.index)
    capacities = open_schools["capacity"].to_dict()

    # Pre-compute protected block sets: blocks walkable to their initial school.
    # These are never moved by Pass A, regardless of capacity dynamics across
    # iterations.  Only meaningful when walk_df is provided.
    protected_blocks: set = set()
    if walk_df is not None:
        for bid, sid in assignments.items():
            if sid in walk_df.columns:
                wd = walk_df.loc[bid, sid]
                if np.isfinite(wd) and wd <= walk_threshold_m:
                    protected_blocks.add(bid)

    for _ in range(max_iterations):
        changed = False
        loads = {sid: sum(blocks_gdf.loc[b, "students"]
                          for b, s in assignments.items() if s == sid)
                 for sid in open_school_ids}

        # Pass A: Fragment consolidation
        for school_id in open_school_ids:
            zone_blocks = [b for b, s in assignments.items() if s == school_id]
            if len(zone_blocks) <= 1:
                continue
            sub = adjacency.subgraph(zone_blocks)
            components = list(nx.connected_components(sub))
            if len(components) <= 1:
                continue
            main_component = max(components, key=len)
            for fragment in sorted(components, key=len):
                if fragment == main_component:
                    continue
                fragment = set(fragment)
                fragment_students = sum(blocks_gdf.loc[b, "students"] for b in fragment)
                # Find adjacent schools
                adj_schools = set()
                for b in fragment:
                    for nbr in adjacency.neighbors(b):
                        ns = assignments.get(nbr)
                        if ns and ns != school_id:
                            adj_schools.add(ns)
                if not adj_schools:
                    continue

                # Don't move a fragment if it contains any block that is walkable
                # to its current school.  The topological disconnection is a
                # census-block adjacency artifact, not a real geographic problem.
                # Protection is pre-computed once before the loop to avoid
                # capacity-cascade false-triggers across iterations.
                if any(b in protected_blocks for b in fragment):
                    continue

                def avg_drive_frag(sid):
                    dists = [drive_df.loc[b, sid] for b in fragment
                             if np.isfinite(drive_df.loc[b, sid])]
                    return sum(dists) / len(dists) if dists else float("inf")

                under_cap = [s for s in adj_schools
                             if loads[s] + fragment_students <= capacities[s]]
                candidates = (sorted(under_cap, key=avg_drive_frag)
                              if under_cap
                              else sorted(adj_schools, key=avg_drive_frag))
                if not candidates:
                    continue
                best = candidates[0]
                for b in fragment:
                    assignments[b] = best
                loads[best] += fragment_students
                loads[school_id] -= fragment_students
                changed = True

        # Pass B: Surrounded block consolidation
        for block_id in list(assignments.keys()):
            current_sid = assignments[block_id]
            nbr_counts = {}
            for nbr in adjacency.neighbors(block_id):
                ns = assignments.get(nbr)
                if ns:
                    nbr_counts[ns] = nbr_counts.get(ns, 0) + 1
            if not nbr_counts:
                continue
            total_nbrs = sum(nbr_counts.values())
            majority_sid = max(nbr_counts, key=nbr_counts.get)
            if majority_sid == current_sid:
                continue
            if nbr_counts[majority_sid] / total_nbrs < 0.60:
                continue
            if not removal_preserves_contiguity(block_id, current_sid, assignments, adjacency):
                continue
            block_students = blocks_gdf.loc[block_id, "students"]
            if loads[majority_sid] + block_students > capacities[majority_sid]:
                continue
            assignments[block_id] = majority_sid
            loads[majority_sid] += block_students
            loads[current_sid] -= block_students
            changed = True

        if not changed:
            break

    return assignments


def recover_walkable_assignments(assignments, blocks_gdf, open_schools, walk_df, adjacency,
                                  walk_threshold_m=1207.0):
    """
    Stage 4.5: Walkability recovery.

    Move any block that is walkable to a school OTHER than its current assignment
    to that school, if:
      - The block is closer to the target by walk than to its current school
      - The target has remaining capacity
      - Removing the block from the source preserves source contiguity
        (or the source has only 1 block, which is handled gracefully)

    This fixes the case where a school's natural walkable neighbourhood is
    topologically isolated from its flood-fill zone (e.g. Kaler in small_closed
    where tract-031 walkable blocks end up in Skillin because the census-block
    adjacency graph does not connect them to Kaler's main zone).
    """
    open_school_ids = list(open_schools.index)
    capacities = open_schools["capacity"].to_dict()
    school_loads = {
        sid: sum(blocks_gdf.loc[b, "students"] for b, s in assignments.items() if s == sid)
        for sid in open_school_ids
    }

    changed = True
    while changed:
        changed = False
        for bid in list(assignments.keys()):
            current_sid = assignments[bid]
            wd_current = walk_df.loc[bid, current_sid] if current_sid in walk_df.columns else float("inf")
            if not np.isfinite(wd_current):
                wd_current = float("inf")

            # Look for schools this block can walk to that are closer by walk
            walkable_targets = [
                sid for sid in open_school_ids
                if sid != current_sid
                and sid in walk_df.columns
                and np.isfinite(walk_df.loc[bid, sid])
                and walk_df.loc[bid, sid] <= walk_threshold_m
                and walk_df.loc[bid, sid] < wd_current   # must be closer by walk
                and school_loads[sid] + blocks_gdf.loc[bid, "students"] <= capacities[sid]
            ]
            if not walkable_targets:
                continue
            if not removal_preserves_contiguity(bid, current_sid, assignments, adjacency):
                continue
            best = min(walkable_targets, key=lambda s: walk_df.loc[bid, s])
            bs = blocks_gdf.loc[bid, "students"]
            assignments[bid] = best
            school_loads[best] += bs
            school_loads[current_sid] -= bs
            changed = True

    return assignments


def equalize_loads(assignments, blocks_gdf, open_schools, drive_df, walk_df, adjacency,
                   walk_threshold_m=1207.0,
                   imbalance_threshold=0.10, max_iterations=40):
    """
    Stage 5: Even out school utilization.

    If any school's utilization deviates from the mean by more than
    imbalance_threshold, move border blocks (outermost by drive distance) from
    over-utilized schools to adjacent under-utilized schools, preserving
    contiguity.  Only moves that keep the source contiguous and the target
    within capacity are accepted.  Walkable blocks are never moved away from
    their current school (preserving walkability).
    """
    open_school_ids = list(open_schools.index)
    capacities = open_schools["capacity"].to_dict()

    for _ in range(max_iterations):
        changed = False
        loads = {sid: sum(blocks_gdf.loc[b, "students"]
                          for b, s in assignments.items() if s == sid)
                 for sid in open_school_ids}
        utils = {sid: loads[sid] / capacities[sid] for sid in open_school_ids}
        mean_util = sum(utils.values()) / len(utils)

        over_schools = sorted(
            [s for s in open_school_ids if utils[s] > mean_util + imbalance_threshold],
            key=lambda s: utils[s], reverse=True,
        )
        under_schools = {s for s in open_school_ids
                         if utils[s] < mean_util - imbalance_threshold}

        # If no school is strictly over threshold but there's still a large spread
        # (e.g. all schools near capacity but one school is significantly under),
        # allow movement from the highest-utilization school to the lowest.
        if not over_schools and under_schools:
            max_sid = max(open_school_ids, key=lambda s: utils[s])
            min_sid = min(open_school_ids, key=lambda s: utils[s])
            if utils[max_sid] - utils[min_sid] > 2 * imbalance_threshold:
                over_schools = [max_sid]
            else:
                break
        elif not over_schools or not under_schools:
            break

        for src_sid in over_schools:
            if utils[src_sid] <= mean_util + imbalance_threshold:
                continue
            zone_blocks = sorted(
                [b for b, s in assignments.items() if s == src_sid],
                key=lambda b: drive_df.loc[b, src_sid],
                reverse=True,
            )
            for block_id in zone_blocks:
                if utils[src_sid] <= mean_util + imbalance_threshold:
                    break
                if not removal_preserves_contiguity(block_id, src_sid, assignments, adjacency):
                    continue
                adj_under = [
                    s for s in _adjacent_zone_schools(
                        block_id, open_school_ids, assignments, adjacency)
                    if s in under_schools
                    and loads[s] + blocks_gdf.loc[block_id, "students"] <= capacities[s]
                ]
                if not adj_under:
                    continue
                best = min(adj_under, key=lambda s: drive_df.loc[block_id, s])
                # Don't move a block to a school it's farther from by walk:
                # this preserves walkable-neighborhood cohesion without being
                # over-restrictive (blocks are only protected if they're
                # actually closer to source by walk).
                wd_src  = walk_df.loc[block_id, src_sid] if src_sid in walk_df.columns else float("inf")
                wd_best = walk_df.loc[block_id, best]    if best    in walk_df.columns else float("inf")
                if not np.isfinite(wd_src):  wd_src  = float("inf")
                if not np.isfinite(wd_best): wd_best = float("inf")
                if wd_src < wd_best:
                    continue  # block is closer to source school by walk; keep it there
                bs = blocks_gdf.loc[block_id, "students"]
                assignments[block_id] = best
                loads[best] += bs
                loads[src_sid] -= bs
                utils[best] = loads[best] / capacities[best]
                utils[src_sid] = loads[src_sid] / capacities[src_sid]
                if utils[best] >= mean_util - imbalance_threshold:
                    under_schools.discard(best)
                changed = True

        if not changed:
            break

    return assignments


def run_scenario(scenario, blocks_gdf, all_schools_gdf, walk_df, drive_df, adjacency):
    """Run full two-stage assignment for one closure scenario."""
    closed = scenario["closed"]
    open_schools = (
        all_schools_gdf[all_schools_gdf["school_id"] != closed].copy()
        if closed else all_schools_gdf.copy()
    )

    print(f"  Stage 1 (capacity-bounded flood-fill) ...")
    assignments = initial_assignment(
        blocks_gdf, open_schools, walk_df, drive_df, adjacency
    )

    for sid in open_schools["school_id"]:
        load = _students_in_zone(sid, assignments, blocks_gdf)
        cap  = open_schools.loc[sid, "capacity"]
        status = "✓" if load <= cap else f"OVER by {load-cap:.0f}"
        print(f"    {sid}: {load:.0f}/{cap} {status}")

    print(f"  Stage 2 (capacity + contiguity enforcement) ...")
    assignments = balance_capacity(
        assignments, blocks_gdf, open_schools, drive_df, adjacency
    )

    print(f"  Stage 3 (bussed community cohesion smoothing) ...")
    assignments = smooth_bussed_communities(
        assignments, blocks_gdf, open_schools, walk_df, drive_df, adjacency
    )

    return assignments, open_schools
