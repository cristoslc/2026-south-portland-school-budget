import { useEffect, useRef } from 'react'
import L from 'leaflet'

const MAP_CENTER   = [43.632, -70.270];
const MAP_ZOOM     = 13;
const WALK_RADIUS  = 1207.0; // 0.75 miles

function blockStyle(color, isEdited, isSelected) {
  return {
    fillColor:   color,
    fillOpacity: 0.65,
    color:       '#555',
    weight:      isSelected ? 2.5 : isEdited ? 2 : 0.6,
    dashArray:   isEdited && !isSelected ? '5,3' : null,
  };
}

export default function MapView({
  scenarioData, assignments, editedBlocks,
  selectedBlockId, onBlockClick, visibleSchools, studentKey,
}) {
  const mapElRef        = useRef(null);
  const mapRef          = useRef(null);
  const layersRef       = useRef({});
  const schoolLayersRef = useRef([]);   // circles + markers, rebuilt on visibleSchools change
  const clickCbRef      = useRef(onBlockClick);
  const asgnRef         = useRef(assignments);
  const studKeyRef      = useRef(studentKey);

  useEffect(() => { clickCbRef.current = onBlockClick; });
  useEffect(() => { asgnRef.current    = assignments;  });
  useEffect(() => { studKeyRef.current = studentKey;   });

  // ── Initialize map and block polygons once ──────────────────────────────
  useEffect(() => {
    const { schools, blocks } = scenarioData;

    const map = L.map(mapElRef.current, { center: MAP_CENTER, zoom: MAP_ZOOM });
    mapRef.current = map;

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap contributors © CARTO', maxZoom: 19,
    }).addTo(map);

    blocks.forEach(block => {
      const sid   = assignments[block.id];
      const color = sid && schools[sid] ? schools[sid].color : '#ccc';
      const layer = L.geoJSON(block.geometry, { style: blockStyle(color, false, false) });

      layer.on('click', e => { L.DomEvent.stopPropagation(e); clickCbRef.current(block, e.containerPoint); });
      layer.on('mouseover', e => {
        const curSid = asgnRef.current[block.id];
        const sk     = studKeyRef.current;
        const wd     = curSid ? block.walkDists[curSid] : null;
        const walkable = wd !== null && wd <= WALK_RADIUS;
        const status = curSid ? (walkable ? 'Walkable' : 'Bussed') : '—';
        const stud = (block[sk] || 0).toFixed(1);
        layer.bindTooltip(
          `<b>${block.id}</b><br>` +
          `Pop: ${block.population} · Students: ${stud}<br>` +
          `Assigned: ${curSid || '—'} · ${status}`,
          { sticky: true }
        ).openTooltip(e.latlng);
      });
      layer.on('mouseout', () => layer.unbindTooltip());

      layer.addTo(map);
      layersRef.current[block.id] = layer;
    });

    map.on('click', () => clickCbRef.current(null, null));

    return () => { map.remove(); mapRef.current = null; layersRef.current = {}; schoolLayersRef.current = []; };
  }, []); // eslint-disable-line

  // ── School markers + walk circles — rebuilt whenever visibleSchools changes ──
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    const { schools } = scenarioData;

    // Remove previous school layers
    schoolLayersRef.current.forEach(l => l.remove());
    schoolLayersRef.current = [];

    visibleSchools.forEach(sid => {
      const s = schools[sid];
      if (!s) return;
      const circle = L.circle([s.lat, s.lng], {
        radius: WALK_RADIUS, color: s.color, weight: 1.5, dashArray: '6', fill: false,
      }).addTo(map);
      const marker = L.circleMarker([s.lat, s.lng], {
        radius: 9, color: '#fff', weight: 2, fillColor: s.color, fillOpacity: 1,
      }).bindTooltip(sid, { permanent: false }).addTo(map);
      schoolLayersRef.current.push(circle, marker);
    });
  }, [visibleSchools]); // eslint-disable-line

  // ── Update block styles when assignments / selection change ──
  useEffect(() => {
    const { schools } = scenarioData;
    scenarioData.blocks.forEach(block => {
      const layer = layersRef.current[block.id];
      if (!layer) return;
      const sid    = assignments[block.id];
      const color  = sid && schools[sid] ? schools[sid].color : '#ccc';
      const edited = editedBlocks.has(block.id);
      const sel    = block.id === selectedBlockId;
      layer.setStyle(blockStyle(color, edited, sel));
      if (sel) layer.bringToFront();
    });
  }, [assignments, editedBlocks, selectedBlockId]); // eslint-disable-line

  return <div ref={mapElRef} className="map-el" />;
}
