import { useState, useEffect } from 'react'
import ScenarioView from './components/ScenarioView'
import UploadTab    from './components/UploadTab'
import AboutModal   from './components/AboutModal'

const BOUNDARIES_URL = 'https://www.arcgis.com/apps/instant/basic/index.html?appid=185441c7918f4681b4653653fc30a27c';

// Alphabetical by school name
const SCENARIO_KEYS = ['brown_closed', 'dyer_closed', 'kaler_closed', 'small_closed'];
const SCENARIO_LABELS = {
  brown_closed: 'Close Brown',
  dyer_closed:  'Close Dyer',
  kaler_closed: 'Close Kaler',
  small_closed: 'Close Small',
};

const MODE_OPTIONS = [
  { key: 'community_current', label: 'Community – Current PreK' },
  { key: 'community_full',    label: 'Community – Full PreK'    },
  { key: 'prek1_current',     label: 'Grade Centers – Current PreK' },
  { key: 'prek1_full',        label: 'Grade Centers – Full PreK'    },
];

const ALL_MODE_KEYS = ['community_current', 'community_full', 'prek1_current', 'prek1_full', 'g24'];

function isGradeCenter(modeOption) {
  return modeOption.startsWith('prek1');
}

function resolveModeKey(modeOption, gradeLevel) {
  if (!isGradeCenter(modeOption)) return modeOption;
  return gradeLevel === 'g24' ? 'g24' : modeOption;
}

function getStudentKey(modeKey) {
  if (modeKey.startsWith('prek1')) return 'studentsK1';
  if (modeKey === 'g24')           return 'studentsG24';
  return 'studentsK4';
}

function getVisibleSchools(modeKey, scenarioData) {
  if (modeKey.startsWith('prek1')) return scenarioData.reconfig.prek1Schools;
  if (modeKey === 'g24')           return scenarioData.reconfig.g24Schools;
  return scenarioData.openSchools;
}

function initScenarioStates(data) {
  const states = {};
  for (const modeKey of ALL_MODE_KEYS) {
    const assignments = {};
    data.blocks.forEach(b => { assignments[b.id] = b.baseAssignments[modeKey]; });
    states[modeKey] = { assignments, editedBlocks: new Set() };
  }
  return states;
}

export default function App() {
  const [activeTab,        setActiveTab]        = useState('brown_closed');
  const [modeOption,       setModeOption]       = useState('community_current');
  const [gradeLevel,       setGradeLevel]       = useState('prek1');
  const [showAbout,        setShowAbout]        = useState(false);
  const [scenarioData,     setScenarioData]     = useState(null);
  const [scenarioStates,   setScenarioStates]   = useState(null);


  useEffect(() => {
    Promise.all(SCENARIO_KEYS.map(k => fetch(`/data/${k}.json`).then(r => r.json())))
      .then(results => {
        const data   = {};
        const states = {};
        SCENARIO_KEYS.forEach((k, i) => {
          data[k]   = results[i];
          states[k] = initScenarioStates(results[i]);
        });
        setScenarioData(data);
        setScenarioStates(states);
      });
  }, []);

  function reassignBlock(scenarioKey, modeKey, blockId, newSchool) {
    setScenarioStates(prev => {
      const modeState = prev[scenarioKey][modeKey];
      const newAssignments = { ...modeState.assignments, [blockId]: newSchool };
      const newEdited = new Set(modeState.editedBlocks);
      const base = scenarioData[scenarioKey].blocks.find(b => b.id === blockId)?.baseAssignments[modeKey];
      if (newSchool === base) newEdited.delete(blockId);
      else                    newEdited.add(blockId);
      return {
        ...prev,
        [scenarioKey]: {
          ...prev[scenarioKey],
          [modeKey]: { assignments: newAssignments, editedBlocks: newEdited },
        },
      };
    });
  }

  function resetMode(scenarioKey, modeKey) {
    setScenarioStates(prev => {
      const newAssignments = {};
      scenarioData[scenarioKey].blocks.forEach(b => {
        newAssignments[b.id] = b.baseAssignments[modeKey];
      });
      return {
        ...prev,
        [scenarioKey]: {
          ...prev[scenarioKey],
          [modeKey]: { assignments: newAssignments, editedBlocks: new Set() },
        },
      };
    });
  }

  if (!scenarioData || !scenarioStates) {
    return <div className="app"><div className="loading">Loading scenario data…</div></div>;
  }

  const gcMode     = isGradeCenter(modeOption);
  const modeKey    = resolveModeKey(modeOption, gradeLevel);
  const studentKey = getStudentKey(modeKey);

  return (
    <div className="app">
      <header className="header">
        <h1>South Portland Elementary School Redistricting</h1>
        <div className="header-right">
          <select
            className="mode-select"
            value={modeOption}
            onChange={e => { setModeOption(e.target.value); setGradeLevel('prek1'); }}
          >
            {MODE_OPTIONS.map(o => (
              <option key={o.key} value={o.key}>{o.label}</option>
            ))}
          </select>
          <button className="btn-about" onClick={() => setShowAbout(true)}>About</button>
        </div>
      </header>

      <div className="tabs">
        {SCENARIO_KEYS.map(key => {
          const hasEdits = scenarioStates[key][modeKey].editedBlocks.size > 0;
          return (
            <button
              key={key}
              className={`tab${activeTab === key ? ' active' : ''}`}
              onClick={() => setActiveTab(key)}
            >
              {SCENARIO_LABELS[key]}
              {hasEdits && <span className="tab-dot" title="Has unsaved edits" />}
            </button>
          );
        })}
        <button
          className={`tab${activeTab === 'upload' ? ' active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          Upload Zones
        </button>

        {/* Right-side tab bar actions */}
        <div className="tabs-right">
          <a
            className="tab-action-btn"
            href={BOUNDARIES_URL}
            target="_blank"
            rel="noopener noreferrer"
          >
            Current Boundaries ↗
          </a>
        </div>
      </div>

      <div className="main">
        {SCENARIO_KEYS.map(key => (
          <ScenarioView
            key={key}
            scenarioData={scenarioData[key]}
            states={scenarioStates[key]}
            active={activeTab === key}
            modeKey={modeKey}
            modeOption={modeOption}
            studentKey={studentKey}
            visibleSchools={getVisibleSchools(modeKey, scenarioData[key])}
            gcMode={gcMode}
            gradeLevel={gradeLevel}
            onGradeLevelChange={setGradeLevel}
            onReassign={(mk, blockId, school) => reassignBlock(key, mk, blockId, school)}
            onReset={(mk) => resetMode(key, mk)}
          />
        ))}
        <UploadTab
          active={activeTab === 'upload'}
        />
      </div>

      {showAbout && <AboutModal onClose={() => setShowAbout(false)} />}

      <footer className="disclaimer">
        <strong>Unofficial tool.</strong> Zone assignments shown here are computer-generated
        estimates based on straight-line and road distances from school addresses — they are
        not official school district boundaries and should not be treated as such.
        This site was created independently by a South Portland parent and has no affiliation
        with South Portland School Department or the School Board.
      </footer>
    </div>
  );
}
