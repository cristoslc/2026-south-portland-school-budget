import { useState } from 'react'
import { computeMetrics } from '../utils/metrics.js'

const GRADE_LABELS = { k: 'K', g1: '1', g2: '2', g3: '3', g4: '4' };

export default function StatsPanel({
  scenarioData, assignments, editedBlocks,
  onReset, modeKey, studentKey, visibleSchools,
}) {
  const { schools } = scenarioData;
  const prekAllocations = scenarioData.prekAllocations[modeKey] || {};
  const metrics = computeMetrics(
    scenarioData.blocks, assignments, visibleSchools, schools, studentKey, prekAllocations
  );
  const hasEdits = editedBlocks.size > 0;
  const [expanded, setExpanded] = useState({});

  return (
    <>
      <div className="sidebar-scroll">
        <div className="sidebar-section">
          <div className="sidebar-section-title">School Enrollment</div>
          {visibleSchools.map(sid => {
            const m = metrics[sid];
            if (!m) return null;
            const pct    = Math.min(m.utilization * 100, 100);
            const isOver = m.overCapacity;
            const isExp  = !!expanded[sid];
            return (
              <div className="school-card" key={sid}>
                <div
                  className="school-card-header school-card-toggle"
                  onClick={() => setExpanded(e => ({ ...e, [sid]: !e[sid] }))}
                >
                  <span className="school-dot" style={{ background: schools[sid].color }} />
                  <span className="school-name">{sid}</span>
                  {isOver && <span className="over-badge">OVER</span>}
                  <svg className="expand-chevron" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    {isExp
                      ? <path d="M7 14l5-5 5 5z"/>
                      : <path d="M7 10l5 5 5-5z"/>}
                  </svg>
                </div>
                <div className="util-bar-bg">
                  <div className="util-bar-fill"
                    style={{ width: pct + '%', background: isOver ? '#e74c3c' : schools[sid].color }} />
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
                {isExp && (
                  <div className="grade-breakdown">
                    {['k', 'g1', 'g2', 'g3', 'g4'].map(g => (
                      <div key={g} className="grade-item">
                        <span className="grade-label">{GRADE_LABELS[g]}</span>
                        <span className="grade-count">{Math.round(m.gradeTotals[g] || 0)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <div className="sidebar-actions">
        <button className="btn btn-secondary" onClick={onReset}
          disabled={!hasEdits} style={{ opacity: hasEdits ? 1 : 0.45 }}>
          Reset to Base
        </button>
      </div>
    </>
  );
}
