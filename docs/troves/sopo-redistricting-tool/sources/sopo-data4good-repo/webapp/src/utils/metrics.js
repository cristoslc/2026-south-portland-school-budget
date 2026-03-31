const WALK_THRESHOLD = 1207.0; // 0.75 miles

/**
 * Compute % of students who would change schools under the proposed assignment.
 *
 * Community mode: compare K-4 assignment to current school.
 * Grade-center mode: K+1 students → compare prek1 assignment; 2+3+4 → compare g24 assignment.
 * PreK excluded (citywide draw, no address data).
 *
 * Returns { pctChange, totalStudents, changedStudents }
 */
export function computeChangeRate(blocks, gcMode, assignments, prek1Assignments, g24Assignments) {
  let totalStudents   = 0;
  let changedStudents = 0;

  for (const block of blocks) {
    if (!gcMode) {
      const assignedSchool = assignments[block.id];
      const cs    = block.currentSchoolsK4 || {};
      const total = Object.values(cs).reduce((s, v) => s + v, 0);
      const stays = assignedSchool ? (cs[assignedSchool] || 0) : 0;
      totalStudents   += total;
      changedStudents += total - stays;
    } else {
      const prek1School = prek1Assignments?.[block.id];
      const g24School   = g24Assignments?.[block.id];
      const csK1  = block.currentSchoolsK1  || {};
      const csG24 = block.currentSchoolsG24 || {};
      const totalK1  = Object.values(csK1).reduce((s, v) => s + v, 0);
      const totalG24 = Object.values(csG24).reduce((s, v) => s + v, 0);
      totalStudents   += totalK1 + totalG24;
      changedStudents += (totalK1  - (prek1School ? (csK1[prek1School]   || 0) : 0))
                       + (totalG24 - (g24School   ? (csG24[g24School]    || 0) : 0));
    }
  }

  const pctChange = totalStudents > 0 ? (changedStudents / totalStudents) * 100 : 0;
  return {
    pctChange:      Math.round(pctChange),
    totalStudents:  Math.round(totalStudents * 10) / 10,
    changedStudents: Math.round(changedStudents * 10) / 10,
  };
}

/**
 * Compute per-school metrics for one mode.
 *
 * studentKey: "studentsK4" | "studentsK1" | "studentsG24"
 * prekAllocations: {schoolId: prekCount}
 */
export function computeMetrics(blocks, assignments, openSchools, schools, studentKey, prekAllocations = {}) {
  const metrics = {};

  for (const sid of openSchools) {
    const zoneBlocks = blocks.filter(b => assignments[b.id] === sid);
    const zoneStudents = zoneBlocks.reduce((s, b) => s + (b[studentKey] || 0), 0);
    const prekCount    = prekAllocations[sid] || 0;
    const totalEnrolled = zoneStudents + prekCount;
    const capacity = schools[sid].capacity;

    // Walkable = pedestrian route exists via OSM AND distance ≤ 0.75-mile policy threshold
    const walkableBlocks    = zoneBlocks.filter(b => b.walkDists[sid] !== null && b.walkDists[sid] <= WALK_THRESHOLD);
    const nonWalkableBlocks = zoneBlocks.filter(b => b.walkDists[sid] === null  || b.walkDists[sid] >  WALK_THRESHOLD);

    const walkableStudents    = walkableBlocks.reduce((s, b) => s + (b[studentKey] || 0), 0);
    const nonWalkableStudents = nonWalkableBlocks.reduce((s, b) => s + (b[studentKey] || 0), 0);
    const pctWalkable         = zoneStudents > 0 ? (walkableStudents / zoneStudents) * 100 : 0;

    // Population-weighted avg drive for non-walkable blocks
    let avgDriveNonWalkMi = null;
    const nwPop = nonWalkableBlocks.reduce((s, b) => s + b.population, 0);
    if (nwPop > 0) {
      const weighted = nonWalkableBlocks.reduce((s, b) => {
        const dd = b.driveDists[sid];
        return dd !== null ? s + dd * b.population : s;
      }, 0);
      avgDriveNonWalkMi = weighted / nwPop / 1609.34;
    }

    // Max drive distance across all zone blocks
    let maxDriveMi = null;
    for (const b of zoneBlocks) {
      const dd = b.driveDists[sid];
      if (dd !== null && (maxDriveMi === null || dd > maxDriveMi * 1609.34))
        maxDriveMi = dd / 1609.34;
    }

    const gradeTotals = {};
    for (const g of ['k', 'g1', 'g2', 'g3', 'g4']) {
      gradeTotals[g] = Math.round(zoneBlocks.reduce((s, b) => s + ((b.studentsPerGrade || {})[g] || 0), 0) * 10) / 10;
    }

    metrics[sid] = {
      zoneStudents:         Math.round(zoneStudents * 10) / 10,
      walkableStudents:     Math.round(walkableStudents * 10) / 10,
      nonWalkableStudents:  Math.round(nonWalkableStudents * 10) / 10,
      prekCount,
      totalEnrolled:        Math.round(totalEnrolled * 10) / 10,
      capacity,
      utilization:          capacity > 0 ? totalEnrolled / capacity : 0,
      overCapacity:         totalEnrolled > capacity,
      pctWalkable:          Math.round(pctWalkable * 10) / 10,
      avgDriveNonWalkMi:    avgDriveNonWalkMi !== null ? Math.round(avgDriveNonWalkMi * 100) / 100 : null,
      maxDriveMi:           maxDriveMi !== null ? Math.round(maxDriveMi * 100) / 100 : null,
      gradeTotals,
    };
  }
  return metrics;
}
