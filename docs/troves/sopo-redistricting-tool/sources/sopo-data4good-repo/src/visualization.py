"""
Generate interactive folium maps with census-block-level colored overlays.

Each scenario map includes:
  - Census blocks colored by assigned school
  - Legend with utilization (X% full, YYY/ZZZ) + walkable % + avg drive for non-walkable
  - School point markers with popups
  - 1-mile walkability radius circles
  - Per-block tooltip with full metrics
"""
import folium
import geopandas as gpd
import numpy as np
import json
import os

from src.config import SCHOOL_COLORS, WALK_THRESHOLD_METERS, OUTPUT_DIR, SCHOOLS

MAP_CENTER = [43.632, -70.270]
MAP_ZOOM   = 13


def _school_icon_color(school_id):
    return {
        "Brown":   "red",
        "Dyer":    "blue",
        "Small":   "green",
        "Skillin": "orange",
        "Kaler":   "purple",
    }.get(school_id, "gray")


def make_scenario_map(
    scenario_name: str,
    assignments: dict,
    blocks_gdf: gpd.GeoDataFrame,
    open_schools: gpd.GeoDataFrame,
    school_metrics: dict,
    walk_df,
    drive_df,
) -> folium.Map:

    # Ensure blocks are in WGS84 for folium
    blocks_4326 = blocks_gdf.copy()
    blocks_4326["geometry"] = blocks_4326["geometry_4326"]
    blocks_4326 = (blocks_4326
                   .set_geometry("geometry")
                   .set_crs("EPSG:4326", allow_override=True))

    m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM, tiles="CartoDB positron")

    open_school_ids = list(open_schools["school_id"])

    # --- Walkability radius circles ---
    for sid in open_school_ids:
        cfg   = SCHOOLS[sid]
        color = SCHOOL_COLORS.get(sid, "#999999")
        folium.Circle(
            location=[cfg["lat"], cfg["lng"]],
            radius=WALK_THRESHOLD_METERS,
            color=color, fill=False, weight=1.5, dash_array="6",
            tooltip=f"{sid} — 1-mile walk radius",
        ).add_to(m)

    # --- Block polygons ---
    for bid, sid in assignments.items():
        if bid not in blocks_4326.index:
            continue
        row  = blocks_4326.loc[bid]
        geom = row["geometry"]
        if geom is None or geom.is_empty:
            continue

        pop  = int(row["population"])
        stud = round(float(row["students"]), 1)
        color = SCHOOL_COLORS.get(sid, SCHOOL_COLORS["UNASSIGNED"])

        wd = walk_df.loc[bid, sid] if sid in walk_df.columns else np.inf
        dd = drive_df.loc[bid, sid] if sid in drive_df.columns else np.inf
        walkable = wd <= WALK_THRESHOLD_METERS

        wd_str = f"{wd/1609.34:.2f} mi" if np.isfinite(wd) else "N/A"
        dd_str = f"{dd/1609.34:.2f} mi" if np.isfinite(dd) else "N/A"
        dd_min = f"{dd/26.8:.0f} min" if np.isfinite(dd) else "N/A"  # ~20 mph avg urban

        tooltip_html = (
            f"<b>Block:</b> {bid}<br>"
            f"<b>Assigned:</b> {sid}<br>"
            f"<b>Population:</b> {pop}<br>"
            f"<b>Est. Students:</b> {stud}<br>"
            f"<b>Mode:</b> {'🚶 Walk' if walkable else '🚗 Drive'}<br>"
            f"<b>Walk dist:</b> {wd_str}<br>"
            f"<b>Drive dist:</b> {dd_str} (~{dd_min})"
        )

        geo_json = json.loads(gpd.GeoSeries([geom]).to_json())
        folium.GeoJson(
            geo_json,
            style_function=lambda f, c=color: {
                "fillColor": c,
                "color": "#333333",
                "weight": 0.6,
                "fillOpacity": 0.65,
            },
            tooltip=folium.Tooltip(tooltip_html, sticky=True),
        ).add_to(m)

    # --- School markers ---
    for sid in open_school_ids:
        cfg = SCHOOLS[sid]
        sm  = school_metrics.get(sid, {})

        stud     = sm.get("assigned_students", 0)
        cap      = sm.get("capacity", 0)
        util     = sm.get("utilization_rate", 0) or 0
        pct_walk = sm.get("pct_walkable", 0)
        nw_mi    = sm.get("avg_drive_non_walkable_mi")
        overflow = sm.get("capacity_overflow", 0)

        nw_str = f"{nw_mi:.2f} mi avg" if nw_mi else "—"
        ovf_str = f"<br>⚠️ Overflow: {overflow:.0f}" if overflow > 0 else ""

        popup_html = (
            f"<b>{sid} Elementary</b><br>"
            f"<b>{util*100:.0f}% full</b> ({stud:.0f}/{cap})<br>"
            f"🚶 Walkable: {pct_walk:.0f}%<br>"
            f"🚗 Non-walkable avg: {nw_str}"
            f"{ovf_str}"
        )

        folium.Marker(
            location=[cfg["lat"], cfg["lng"]],
            popup=folium.Popup(popup_html, max_width=210),
            tooltip=f"{sid}: {util*100:.0f}% full",
            icon=folium.Icon(color=_school_icon_color(sid), icon="home", prefix="fa"),
        ).add_to(m)

    # --- Legend (with utilization + walkable % + non-walkable avg drive) ---
    legend_rows = ""
    for sid in open_school_ids:
        sm      = school_metrics.get(sid, {})
        color   = SCHOOL_COLORS.get(sid, "#ccc")
        stud    = sm.get("assigned_students", 0)
        cap     = sm.get("capacity", 0)
        util    = (sm.get("utilization_rate") or 0) * 100
        pct_w   = sm.get("pct_walkable", 0)
        nw_mi   = sm.get("avg_drive_non_walkable_mi")
        nw_str  = f"{nw_mi:.2f} mi" if nw_mi else "—"

        legend_rows += (
            f'<div style="margin-bottom:8px;">'
            f'  <span style="background:{color};width:14px;height:14px;display:inline-block;'
            f'margin-right:6px;border-radius:2px;vertical-align:middle;"></span>'
            f'  <b>{sid}</b><br>'
            f'  <span style="margin-left:20px;font-size:11px;color:#333;">'
            f'    {util:.0f}% full &nbsp;({stud:.0f}/{cap})<br>'
            f'    <span style="margin-left:0px;">🚶 {pct_w:.0f}% walkable &nbsp;'
            f'    🚗 {nw_str} avg (non-walk)</span>'
            f'  </span>'
            f'</div>'
        )

    scenario_label = (scenario_name
                      .replace("_closed", " Closed")
                      .replace("no_closure", "No Closure")
                      .replace("_", " ")
                      .title())

    legend_html = f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
                padding:14px 18px;border-radius:8px;
                box-shadow:0 2px 10px rgba(0,0,0,0.25);
                font-family:Arial,sans-serif;font-size:13px;line-height:1.6;
                min-width:230px;">
      <b style="font-size:14px;">School Zones</b><br>
      <div style="margin:6px 0 8px 0;border-bottom:1px solid #eee;"></div>
      {legend_rows}
      <div style="margin-top:8px;border-top:1px solid #eee;padding-top:6px;
                  font-size:11px;color:#888;">
        Dashed circle = 1-mile walk radius<br>
        Hover blocks for detail
      </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # --- Title ---
    title_html = (
        f'<div style="position:fixed;top:10px;left:50%;transform:translateX(-50%);'
        f'z-index:1000;background:white;padding:8px 20px;border-radius:5px;'
        f'box-shadow:0 2px 6px rgba(0,0,0,0.2);font-family:Arial,sans-serif;'
        f'font-size:15px;font-weight:bold;">'
        f'South Portland Elementary — {scenario_label}</div>'
    )
    m.get_root().html.add_child(folium.Element(title_html))

    return m


def save_map(m: folium.Map, scenario_name: str):
    path = os.path.join(OUTPUT_DIR, f"{scenario_name}_map.html")
    m.save(path)
    print(f"  Map saved: {path}")
    return path
