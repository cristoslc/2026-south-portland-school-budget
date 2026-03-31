import { useState, useEffect, useRef } from 'react'
import L from 'leaflet'
import html2canvas from 'html2canvas'
import { computeMetrics, computeChangeRate } from '../utils/metrics.js'

const WALK_THRESHOLD = 1207.0; // 0.75 miles
const MAP_CENTER     = [43.632, -70.270];
const MAP_ZOOM       = 13;

// ── Parsing ──────────────────────────────────────────────────────────────────

function parseGeoJSON(geojson) {
  const { metadata, features } = geojson;
  const { isGradeCenter, openSchools, schools } = metadata;

  const blocks = features.map(f => ({
    id:          f.properties.block_id,
    geometry:    f.geometry,
    population:  f.properties.population,
    studentsK4:  f.properties.students_k4,
    studentsK1:  f.properties.students_k1,
    studentsG24: f.properties.students_g24,
    walkDists:   f.properties.all_walk_dists  || {},
    driveDists:  f.properties.all_drive_dists || {},
    // base assignments for reset / labeling
    basePrek1:  f.properties.assigned_prek1,
    baseG24:    f.properties.assigned_g24,
    baseSchool: f.properties.assigned_school,
  }));

  if (isGradeCenter) {
    const { modeOption, prek1Schools, g24Schools, prekAllocations } = metadata;
    const initPrek1 = {}, initG24 = {};
    features.forEach(f => {
      initPrek1[f.properties.block_id] = f.properties.assigned_prek1;
      initG24[f.properties.block_id]   = f.properties.assigned_g24;
    });
    return {
      isGradeCenter: true,
      blocks, openSchools, schools,
      modeOption, prek1Schools, g24Schools,
      prekAllocations: prekAllocations || {},
      initPrek1, initG24, metadata,
    };
  } else {
    const { modeKey, prekAllocations } = metadata;
    const studentKey = modeKey.startsWith('prek1') ? 'studentsK1'
                     : modeKey === 'g24'            ? 'studentsG24'
                     : 'studentsK4';
    const initAssignments = {};
    features.forEach(f => { initAssignments[f.properties.block_id] = f.properties.assigned_school; });
    return {
      isGradeCenter: false,
      blocks, openSchools, schools,
      modeKey, studentKey,
      prekAllocations: prekAllocations || {},
      initAssignments, metadata,
    };
  }
}

// ── Shared map component ──────────────────────────────────────────────────────

function blockStyle(color, isSelected) {
  return { fillColor: color, fillOpacity: 0.65, color: '#555', weight: isSelected ? 2.5 : 0.6 };
}

function UploadMap({ parsed, assignments, visibleSchools, selectedBlockId, onBlockClick }) {
  const mapElRef  = useRef(null);
  const mapRef    = useRef(null);
  const layersRef = useRef({});
  const cbRef     = useRef(onBlockClick);
  const asgnRef   = useRef(assignments);
  const vsRef     = useRef(visibleSchools);

  useEffect(() => { cbRef.current  = onBlockClick;   });
  useEffect(() => { asgnRef.current = assignments;    });
  useEffect(() => { vsRef.current   = visibleSchools; });

  useEffect(() => {
    const { blocks, schools } = parsed;
    const activeSchools = visibleSchools;

    const map = L.map(mapElRef.current, { center: MAP_CENTER, zoom: MAP_ZOOM });
    mapRef.current = map;

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap contributors © CARTO', maxZoom: 19,
    }).addTo(map);

    blocks.forEach(block => {
      const sid   = assignments[block.id];
      const color = sid && schools[sid] ? schools[sid].color : '#ccc';
      const layer = L.geoJSON(block.geometry, { style: blockStyle(color, false) });

      layer.on('click', e => { L.DomEvent.stopPropagation(e); cbRef.current(block, e.containerPoint); });
      layer.on('mouseover', e => {
        const curSid  = asgnRef.current[block.id];
        const wd      = curSid ? (block.walkDists[curSid] ?? null) : null;
        const walkable = wd !== null && wd <= WALK_THRESHOLD;
        const status  = curSid ? (walkable ? 'Walkable' : 'Bussed') : '—';
        layer.bindTooltip(
          `<b>${block.id}</b><br>Pop: ${block.population}<br>` +
          `Assigned: ${curSid || '—'} · ${status}`,
          { sticky: true }
        ).openTooltip(e.latlng);
      });
      layer.on('mouseout', () => layer.unbindTooltip());
      layer.addTo(map);
      layersRef.current[block.id] = layer;
    });

    activeSchools.forEach(sid => {
      const s = schools[sid];
      if (!s) return;
      L.circle([s.lat, s.lng], {
        radius: WALK_THRESHOLD, color: s.color, weight: 1.5, dashArray: '6', fill: false,
      }).addTo(map);
      L.circleMarker([s.lat, s.lng], {
        radius: 9, color: '#fff', weight: 2, fillColor: s.color, fillOpacity: 1,
      }).bindTooltip(sid).addTo(map);
    });

    map.on('click', () => cbRef.current(null, null));

    return () => { map.remove(); mapRef.current = null; layersRef.current = {}; };
  }, []); // eslint-disable-line

  useEffect(() => {
    const { blocks, schools } = parsed;
    blocks.forEach(block => {
      const layer = layersRef.current[block.id];
      if (!layer) return;
      const sid   = assignments[block.id];
      const color = sid && schools[sid] ? schools[sid].color : '#ccc';
      layer.setStyle(blockStyle(color, block.id === selectedBlockId));
      if (block.id === selectedBlockId) layer.bringToFront();
    });
  }, [assignments, selectedBlockId]); // eslint-disable-line

  return <div ref={mapElRef} className="map-el" />;
}

// ── Stats sidebar ─────────────────────────────────────────────────────────────

function UploadStats({ parsed, assignments, visibleSchools, studentKey, onClear }) {
  const { schools, prekAllocations, metadata, modeOption, modeKey } = parsed;
  const metrics = computeMetrics(parsed.blocks, assignments, visibleSchools, schools, studentKey, prekAllocations);

  const scenarioLabel = metadata.scenario
    ? metadata.scenario.replace(/_closed$/, ' Closed').replace(/_/g, ' ')
    : 'Uploaded';
  const modeLabel = parsed.isGradeCenter
    ? `Grade Centers · ${(modeOption || '').replace('prek1_', '')} PreK`
    : (modeKey || '').replace(/_/g, ' ');

  return (
    <>
      <div className="sidebar-scroll">
        <div className="sidebar-section">
          <div className="sidebar-section-title">{scenarioLabel}</div>
          <div className="school-stat" style={{ marginBottom: 4 }}>
            Mode: <strong>{modeLabel}</strong>
          </div>
        </div>

        <div className="sidebar-section">
          <div className="sidebar-section-title">School Enrollment</div>
          {visibleSchools.map(sid => {
            const m = metrics[sid];
            if (!m) return null;
            const pct    = Math.min(m.utilization * 100, 100);
            const isOver = m.overCapacity;
            return (
              <div className="school-card" key={sid}>
                <div className="school-card-header">
                  <span className="school-dot" style={{ background: schools[sid]?.color }} />
                  <span className="school-name">{sid}</span>
                  {isOver && <span className="over-badge">OVER</span>}
                </div>
                <div className="util-bar-bg">
                  <div className="util-bar-fill"
                    style={{ width: pct + '%', background: isOver ? '#e74c3c' : schools[sid]?.color }} />
                </div>
                <div className={`school-stat${isOver ? ' stat-over' : ''}`}>
                  {m.totalEnrolled.toFixed(0)} / {m.capacity} enrolled
                  {m.prekCount > 0 && <span className="prek-note"> (incl. {m.prekCount} PreK)</span>}
                </div>
                <div className="school-stat">
                  {m.pctWalkable.toFixed(0)}% walkable
                  <span className="stat-muted"> ({m.walkableStudents.toFixed(0)} students within 0.75 mi)</span>
                </div>
                <div className="school-stat">
                  {m.avgDriveNonWalkMi !== null ? m.avgDriveNonWalkMi.toFixed(2) + ' mi avg drive' : '—'}
                  {m.maxDriveMi !== null && <span className="stat-muted"> · max {m.maxDriveMi.toFixed(2)} mi</span>}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="sidebar-actions">
        <button className="btn btn-secondary" onClick={onClear}>Clear Upload</button>
      </div>
    </>
  );
}

// ── Main UploadTab ────────────────────────────────────────────────────────────

export default function UploadTab({ active }) {
  const [parsed,        setParsed]        = useState(null);
  const [assignments,   setAssignments]   = useState(null);   // community mode
  const [prek1Asgn,     setPrek1Asgn]     = useState(null);   // grade-center prek1 band
  const [g24Asgn,       setG24Asgn]       = useState(null);   // grade-center g24 band
  const [gradeLevel,    setGradeLevel]    = useState('prek1');
  const [selectedBlock, setSelectedBlock] = useState(null);
  const [popupPos,      setPopupPos]      = useState(null);
  const [dragOver,      setDragOver]      = useState(false);
  const [error,         setError]         = useState(null);
  const viewRef = useRef(null);

  function handleExportPNG() {
    if (!viewRef.current) return;
    const label = parsed?.metadata?.scenario || 'uploaded';
    html2canvas(viewRef.current, { useCORS: true, scale: 2 }).then(canvas => {
      const link = document.createElement('a');
      link.download = `${label}_zones.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    });
  }

  function handleFile(file) {
    setError(null);
    const reader = new FileReader();
    reader.onload = e => {
      try {
        const geojson = JSON.parse(e.target.result);
        if (geojson.metadata?.source !== 'sopo-redistricting-tool') {
          setError('This file was not exported from the South Portland redistricting tool.');
          return;
        }
        if (!geojson.features?.length) {
          setError('No features found in this file.');
          return;
        }
        const p = parseGeoJSON(geojson);
        setParsed(p);
        setSelectedBlock(null);
        setGradeLevel('prek1');
        if (p.isGradeCenter) {
          setPrek1Asgn({ ...p.initPrek1 });
          setG24Asgn({ ...p.initG24 });
          setAssignments(null);
        } else {
          setAssignments({ ...p.initAssignments });
          setPrek1Asgn(null);
          setG24Asgn(null);
        }
      } catch {
        setError('Could not parse file. Please upload a valid GeoJSON file.');
      }
    };
    reader.readAsText(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }

  function handleClear() {
    setParsed(null); setAssignments(null);
    setPrek1Asgn(null); setG24Asgn(null);
    setSelectedBlock(null); setError(null);
  }

  function handleReassign(blockId, newSchool) {
    if (!parsed) return;
    if (parsed.isGradeCenter) {
      if (gradeLevel === 'prek1') setPrek1Asgn(prev => ({ ...prev, [blockId]: newSchool }));
      else                        setG24Asgn(prev   => ({ ...prev, [blockId]: newSchool }));
    } else {
      setAssignments(prev => ({ ...prev, [blockId]: newSchool }));
    }
  }

  if (!active) return <div className="scenario-view hidden" />;

  if (!parsed) {
    return (
      <div className="scenario-view upload-view">
        <div
          className={`upload-drop-area${dragOver ? ' drag-over' : ''}`}
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
        >
          <div className="upload-icon">&#128193;</div>
          <div className="upload-title">Drop a zone file here</div>
          <div className="upload-subtitle">
            Upload a GeoJSON file exported from this tool to visualize and compare shared zone plans.
          </div>
          <label className="btn btn-secondary upload-browse">
            Browse file
            <input type="file" accept=".geojson,.json" style={{ display: 'none' }}
              onChange={e => { if (e.target.files[0]) handleFile(e.target.files[0]); }} />
          </label>
          {error && <div className="upload-error">{error}</div>}
        </div>
      </div>
    );
  }

  // Derive active view for grade-center vs community
  const gcMode      = parsed.isGradeCenter;
  const activeAsgn  = gcMode
    ? (gradeLevel === 'prek1' ? prek1Asgn : g24Asgn)
    : assignments;
  const visSchools  = gcMode
    ? (gradeLevel === 'prek1' ? parsed.prek1Schools : parsed.g24Schools)
    : parsed.openSchools;
  const studKey     = gcMode
    ? (gradeLevel === 'prek1' ? 'studentsK1' : 'studentsG24')
    : parsed.studentKey;

  // % change
  const changeInfo = computeChangeRate(
    parsed.blocks, gcMode, activeAsgn,
    gcMode ? prek1Asgn : null,
    gcMode ? g24Asgn   : null,
  );

  return (
    <div ref={viewRef} className="scenario-view">
      <div className="map-container">
        <UploadMap
          parsed={parsed}
          assignments={activeAsgn}
          visibleSchools={visSchools}
          selectedBlockId={selectedBlock?.id ?? null}
          onBlockClick={(block, pos) => { setSelectedBlock(block); setPopupPos(pos || null); }}
        />
        {selectedBlock && popupPos && activeAsgn && (() => {
          const sid    = activeAsgn[selectedBlock.id];
          const wd     = sid ? (selectedBlock.walkDists[sid] ?? null) : null;
          const walkable = wd !== null && wd <= WALK_THRESHOLD;
          const baseSchool = parsed.isGradeCenter
            ? (studKey === 'studentsK1' ? selectedBlock.basePrek1 : selectedBlock.baseG24)
            : selectedBlock.baseSchool;
          return (
            <div className="block-popup" style={{ left: popupPos.x, top: popupPos.y }}>
              <div className="block-popup-header">
                <span className="block-popup-id">···{selectedBlock.id.slice(-6)}</span>
                <button className="block-popup-close" onClick={() => setSelectedBlock(null)}>✕</button>
              </div>
              <div className="block-popup-row">{(selectedBlock[studKey] || 0).toFixed(1)} est. students</div>
              <div className="block-popup-row">
                <span className={walkable ? 'tag-walkable' : 'tag-bussed'}>{walkable ? 'Walkable' : 'Bussed'}</span>
              </div>
              <select className="reassign-select" value={sid || ''}
                onChange={e => handleReassign(selectedBlock.id, e.target.value)}>
                {visSchools.map(s => (
                  <option key={s} value={s}>{s}{s === baseSchool ? ' (original)' : ''}</option>
                ))}
              </select>
            </div>
          );
        })()}
        {gcMode && (
          <div className="grade-band-overlay">
            <button
              className={`band-btn${gradeLevel === 'prek1' ? ' active' : ''}`}
              onClick={() => { setGradeLevel('prek1'); setSelectedBlock(null); }}
            >PreK–1</button>
            <button
              className={`band-btn${gradeLevel === 'g24' ? ' active' : ''}`}
              onClick={() => { setGradeLevel('g24'); setSelectedBlock(null); }}
            >2–4</button>
          </div>
        )}
        <div className="change-overlay">
          <span className="change-pill">
            {changeInfo.pctChange}% Change Schools
          </span>
        </div>
      </div>
      <div className="sidebar">
        <UploadStats
          parsed={parsed}
          assignments={activeAsgn}
          visibleSchools={visSchools}
          studentKey={studKey}
          onClear={handleClear}
        />
        <div className="sidebar-actions">
          <button className="btn btn-secondary btn-export" onClick={handleExportPNG}>
            <svg xmlns="http://www.w3.org/2000/svg" height="13" width="13" viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
            PNG
          </button>
        </div>
      </div>
    </div>
  );
}
