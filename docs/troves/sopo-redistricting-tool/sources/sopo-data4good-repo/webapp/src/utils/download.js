const WALK_THRESHOLD = 1207.0; // 0.75 miles

export function downloadGeoJSON({
  scenarioData,
  isGradeCenter,
  modeOption,
  modeKey,
  studentKey,
  prekAllocations,
  assignments,
  editedBlocks,
  // grade-center only:
  prek1Assignments,
  g24Assignments,
  prek1EditedBlocks,
  g24EditedBlocks,
}) {
  const { scenario, closedSchool, openSchools, schools, reconfig } = scenarioData;

  const features = scenarioData.blocks.map(block => {
    // Embed distances to all open schools so uploaded files are fully self-contained
    const allWalkDists  = {};
    const allDriveDists = {};
    for (const sid of openSchools) {
      allWalkDists[sid]  = block.walkDists[sid];
      allDriveDists[sid] = block.driveDists[sid];
    }

    const baseProps = {
      block_id:        block.id,
      population:      block.population,
      students_k4:     block.studentsK4,
      students_k1:     block.studentsK1,
      students_g24:    block.studentsG24,
      all_walk_dists:  allWalkDists,
      all_drive_dists: allDriveDists,
    };

    if (isGradeCenter) {
      const assignedPrek1 = (prek1Assignments || {})[block.id];
      const assignedG24   = (g24Assignments   || {})[block.id];
      return {
        type: 'Feature',
        geometry: block.geometry,
        properties: {
          ...baseProps,
          assigned_prek1:    assignedPrek1,
          assigned_g24:      assignedG24,
          was_edited_prek1:  (prek1EditedBlocks || new Set()).has(block.id),
          was_edited_g24:    (g24EditedBlocks   || new Set()).has(block.id),
        },
      };
    } else {
      const assignedSchool = assignments[block.id];
      const walkDist  = assignedSchool ? block.walkDists[assignedSchool]  : null;
      const driveDist = assignedSchool ? block.driveDists[assignedSchool] : null;
      return {
        type: 'Feature',
        geometry: block.geometry,
        properties: {
          ...baseProps,
          assigned_school:  assignedSchool,
          base_assignment:  block.baseAssignments[modeKey],
          was_edited:       editedBlocks.has(block.id),
          walk_dist_m:      walkDist,
          walk_dist_mi:     walkDist  !== null ? Math.round(walkDist  / 1609.34 * 100) / 100 : null,
          drive_dist_m:     driveDist,
          drive_dist_mi:    driveDist !== null ? Math.round(driveDist / 1609.34 * 100) / 100 : null,
          walkable:         walkDist !== null && walkDist <= WALK_THRESHOLD,
        },
      };
    }
  });

  const metadata = isGradeCenter
    ? {
        source:        'sopo-redistricting-tool',
        isGradeCenter: true,
        scenario,
        closedSchool,
        openSchools,
        schools,
        modeOption,
        prek1Schools:  reconfig.prek1Schools,
        g24Schools:    reconfig.g24Schools,
        prekAllocations,
        exportedAt:    new Date().toISOString(),
      }
    : {
        source:        'sopo-redistricting-tool',
        isGradeCenter: false,
        scenario,
        closedSchool,
        openSchools,
        schools,
        modeKey,
        prekAllocations,
        exportedAt:    new Date().toISOString(),
      };

  const suffix   = isGradeCenter
    ? `grade_centers_${modeOption.replace('prek1_', '')}`
    : modeKey;
  const filename = `${scenario}_${suffix}_zones.geojson`;

  const geojson = { type: 'FeatureCollection', metadata, features };
  const blob = new Blob([JSON.stringify(geojson, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}
