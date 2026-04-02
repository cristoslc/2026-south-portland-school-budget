import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';

import {
  TRANSPORT_COMMUNITY_LENSES,
  getTransportCommunityLens,
  getTransportCommunityLensEntries,
} from '../src/lib/transport-content.js';

const INDEX_SOURCE = new URL('../src/pages/transportation-analysis/briefings/index.astro', import.meta.url);
const SLUG_SOURCE = new URL('../src/pages/transportation-analysis/briefings/[slug].astro', import.meta.url);
const TRANSPORT_LANDING_SOURCE = new URL('../src/pages/transportation-analysis/index.astro', import.meta.url);
const BUILT_HOME_INDEX = new URL('../dist/index.html', import.meta.url);
const BUILT_TRANSPORT_LANDING = new URL('../dist/transportation-analysis/index.html', import.meta.url);
const BUILT_BRIEFINGS_INDEX = new URL('../dist/transportation-analysis/briefings/index.html', import.meta.url);
const BUILT_BRIEFINGS_DIR = new URL('../dist/transportation-analysis/briefings/', import.meta.url);

const EXPECTED_LENS_IDS = [
  'transport-general',
  'transport-families',
  'transport-elementary-families',
  'transport-staff',
  'transport-taxpayers',
  'transport-older-students',
  'transport-city-school-leadership',
];

const EXPECTED_LENS_LABELS = [
  'General Community',
  'Families',
  'Elementary Families',
  'Staff',
  'Taxpayers',
  'Older Students',
  'City and School Leadership',
];

const FORBIDDEN_PATTERNS = [/persona_id/i, /persona_name/i, /PERSONA-\d+/, /Transport Persona/i, /View persona profile/i];
const PUBLIC_PHRASES = ['being asked to vote', 'before the vote', 'scheduled to vote'];

const MOCK_TRANSPORT_BRIEFINGS = [
  { id: 'transport-elementary-families' },
  { id: 'transport-ignored-draft' },
  { id: 'transport-general' },
  { id: 'transport-staff' },
  { id: 'transport-city-school-leadership' },
  { id: 'transport-families' },
  { id: 'transport-taxpayers' },
  { id: 'transport-older-students' },
];

test('transport community lens metadata lists the seven public briefing pages', () => {
  assert.deepEqual(
    TRANSPORT_COMMUNITY_LENSES.map((lens) => lens.id),
    EXPECTED_LENS_IDS,
  );

  assert.deepEqual(
    TRANSPORT_COMMUNITY_LENSES.map((lens) => lens.label),
    EXPECTED_LENS_LABELS,
  );
});

test('getTransportCommunityLensEntries returns the seven public lens pages in public order', () => {
  const ids = getTransportCommunityLensEntries(MOCK_TRANSPORT_BRIEFINGS).map(({ entry }) => entry.id);

  assert.deepEqual(ids, EXPECTED_LENS_IDS);
});

test('getTransportCommunityLens resolves valid public lens ids and rejects unknown ids', () => {
  for (const lensId of EXPECTED_LENS_IDS) {
    assert.equal(getTransportCommunityLens(lensId)?.id, lensId);
  }

  assert.equal(getTransportCommunityLens('transport-ignored-draft'), null);
  assert.equal(getTransportCommunityLens('missing-lens-id'), null);
});

test('transport briefing index and slug pages derive from the public lens source and lens summary copy', async () => {
  const [indexSource, slugSource, landingSource] = await Promise.all([
    readFile(INDEX_SOURCE, 'utf8'),
    readFile(SLUG_SOURCE, 'utf8'),
    readFile(TRANSPORT_LANDING_SOURCE, 'utf8'),
  ]);

  assert.match(indexSource, /getTransportCommunityLensEntries\(transportBriefings\)/);
  assert.match(indexSource, /Community Lenses/);
  assert.match(slugSource, /getTransportCommunityLensEntries\(transportBriefings\)/);
  assert.match(slugSource, /const lensSummary = lens\?\.summary \?\? ['"]Transportation briefing\.['"];?/);
  assert.match(slugSource, /description=\{lensSummary\}/);
  assert.match(slugSource, /<p>\{lensSummary\}<\/p>/);
  assert.doesNotMatch(slugSource, /transportation community lens/i);
  assert.match(landingSource, /seven community lenses/i);
  assert.doesNotMatch(landingSource, /persona-specific explainers/i);

  for (const source of [indexSource, slugSource, landingSource]) {
    for (const pattern of FORBIDDEN_PATTERNS) {
      assert.equal(pattern.test(source), false, `leaked ${pattern}`);
    }
  }
});

test('built transport output exposes only the seven public lens pages and no persona framing', async () => {
  const [homeIndex, transportLanding, briefingIndex, briefingDirs] = await Promise.all([
    readFile(BUILT_HOME_INDEX, 'utf8'),
    readFile(BUILT_TRANSPORT_LANDING, 'utf8'),
    readFile(BUILT_BRIEFINGS_INDEX, 'utf8'),
    readdir(BUILT_BRIEFINGS_DIR, { withFileTypes: true }),
  ]);

  const briefingDirNames = briefingDirs
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();

  assert.deepEqual(briefingDirNames, [...EXPECTED_LENS_IDS].sort());
  assert.equal(briefingDirNames.some((name) => name.includes('transport-persona-')), false);

  assert.match(homeIndex, /community lens briefings/i);
  assert.equal(/PERSONA-\d+/.test(homeIndex), false);
  assert.equal(/transport-persona-/i.test(homeIndex), false);

  assert.match(transportLanding, /seven community lenses/i);
  assert.doesNotMatch(transportLanding, /persona-specific explainers/i);
  assert.equal(/transport-persona-/i.test(briefingIndex), false);

  for (const lensId of EXPECTED_LENS_IDS) {
    const page = await readFile(new URL(`../dist/transportation-analysis/briefings/${lensId}/index.html`, import.meta.url), 'utf8');
    assert.equal(/PERSONA-\d+/.test(page), false, `${lensId} leaked persona IDs`);
    for (const phrase of PUBLIC_PHRASES) {
      assert.equal(page.includes(phrase), false, `${lensId} leaked phrase: ${phrase}`);
    }
  }

  for (const phrase of PUBLIC_PHRASES) {
    assert.equal(transportLanding.includes(phrase), false, `transport landing leaked phrase: ${phrase}`);
  }
});
