import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';

import {
  normalizeTransportMarkdown,
  parseMarkdownEntry,
  getTransportAnalysisEntries,
  sanitizePublicMarkdown,
} from '../src/lib/transport-content.js';

const BRIEFINGS_DIR = new URL('../../dist/transportation-analysis/briefings/', import.meta.url);
const BOARD_LETTER_FILE = new URL('../../dist/transportation-analysis/BOARD-LETTER-DRAFT.md', import.meta.url);

const EXPECTED_BRIEFING_IDS = [
  'transport-city-school-leadership',
  'transport-elementary-families',
  'transport-families',
  'transport-general',
  'transport-older-students',
  'transport-staff',
  'transport-taxpayers',
];

const BRIEFINGS_WITH_MODELED_DRIVER_COUNT = new Set([
  'transport-city-school-leadership',
  'transport-families',
  'transport-staff',
  'transport-taxpayers',
]);

test('normalizeTransportMarkdown unwraps fenced frontmatter blocks', () => {
  const input = [
    '```markdown',
    '---',
    'persona_id: "general"',
    'topic: "transportation"',
    '---',
    '```',
    '',
    '# Heading',
    '',
    'Body text.',
  ].join('\n');

  const output = normalizeTransportMarkdown(input);

  assert.equal(
    output,
    ['---', 'persona_id: "general"', 'topic: "transportation"', '---', '', '# Heading', '', 'Body text.'].join('\n'),
  );
});

test('normalizeTransportMarkdown unwraps yaml-fenced frontmatter blocks', () => {
  const input = [
    '```yaml',
    '---',
    'persona_id: "PERSONA-015"',
    'topic: "transportation"',
    '---',
    '```',
    '',
    '# Heading',
    '',
    'Body text.',
  ].join('\n');

  const output = normalizeTransportMarkdown(input);

  assert.equal(
    output,
    ['---', 'persona_id: "PERSONA-015"', 'topic: "transportation"', '---', '', '# Heading', '', 'Body text.'].join(
      '\n',
    ),
  );
});

test('parseMarkdownEntry extracts frontmatter data and markdown body', () => {
  const source = [
    '```',
    '---',
    'persona_id: "PERSONA-001"',
    'persona_name: "Maria"',
    'topic: "transportation"',
    'source_specs: ["SPEC-060", "SPEC-065"]',
    'generated_date: "2026-03-31"',
    '---',
    '```',
    '',
    '# Transportation Impact Brief',
    '',
    'Hello world.',
  ].join('\n');

  const entry = parseMarkdownEntry({
    id: 'transport-persona-001-maria',
    source,
    filePath: 'dist/transportation-analysis/briefings/transport-persona-001-maria.md',
  });

  assert.equal(entry.id, 'transport-persona-001-maria');
  assert.equal(entry.data.persona_id, 'PERSONA-001');
  assert.equal(entry.data.persona_name, 'Maria');
  assert.equal(entry.data.topic, 'transportation');
  assert.deepEqual(entry.data.source_specs, ['SPEC-060', 'SPEC-065']);
  assert.match(entry.body, /^# Transportation Impact Brief/m);
});

test('parseMarkdownEntry removes the transport wrapper divider before markdown content', () => {
  const source = [
    '```',
    '---',
    'persona_id: "PERSONA-001"',
    '---',
    '```',
    '',
    '---',
    '',
    '# Transport Title',
    '',
    'Body text.',
  ].join('\n');

  const entry = parseMarkdownEntry({
    id: 'transport-persona-001-maria',
    source,
    filePath: 'dist/transportation-analysis/briefings/transport-persona-001-maria.md',
  });

  assert.equal(entry.body, ['# Transport Title', '', 'Body text.'].join('\n'));
});

test('getTransportAnalysisEntries only includes public transport analysis docs', () => {
  const entries = getTransportAnalysisEntries();
  const ids = entries.map((entry) => entry.id);

  assert.deepEqual(ids, [
    'readme',
    'post-decision-brief',
    'board-letter',
    'methodology',
    'transport-configuration-comparison',
    'split-family-model',
    'mckinney-vento-exposure',
    'sea-staffing-assessment',
    'bell-schedule-analysis',
    'before-after-care-gap',
  ]);
});

test('board letter source is post-decision and problem-solving', async () => {
  const source = await readFile(BOARD_LETTER_FILE, 'utf8');
  const entry = parseMarkdownEntry({
    id: 'board-letter',
    source,
    filePath: 'dist/transportation-analysis/BOARD-LETTER-DRAFT.md',
  });

  assert.doesNotMatch(entry.body, /scheduled to vote/i);
  assert.doesNotMatch(entry.body, /before the vote/i);
  assert.doesNotMatch(entry.body, /if the district adopts/i);
  assert.match(entry.body, /What has already been decided/i);
  assert.match(entry.body, /What now needs public clarity/i);
  assert.match(entry.body, /Specific requests for the board and district/i);
});

test('transport briefing corpus contains only the seven post-decision community lenses', async () => {
  const files = (await readdir(BRIEFINGS_DIR)).filter((file) => file.endsWith('.md')).sort();
  const ids = files.map((file) => file.replace(/\.md$/, ''));

  assert.deepEqual(ids, EXPECTED_BRIEFING_IDS);
  assert.equal(ids.some((id) => id.includes('transport-persona-')), false);
});

test('transport briefing corpus has the expected post-decision frontmatter and modeled driver wording', async () => {
  for (const id of EXPECTED_BRIEFING_IDS) {
    const filePath = new URL(`../../dist/transportation-analysis/briefings/${id}.md`, import.meta.url);
    const source = await readFile(filePath, 'utf8');
    const entry = parseMarkdownEntry({
      id,
      source,
      filePath: `dist/transportation-analysis/briefings/${id}.md`,
    });

    assert.ok(entry.data.title, `${id} is missing title frontmatter`);
    assert.ok(entry.data.audience, `${id} is missing audience frontmatter`);
    assert.equal(entry.data.decision_phase, 'post-decision', `${id} must be post-decision`);
    assert.equal(entry.data.topic, 'transportation', `${id} must be transportation content`);
    assert.match(entry.body, /Post-Decision Transportation Brief/i, `${id} must link to the canonical overview`);

    if (BRIEFINGS_WITH_MODELED_DRIVER_COUNT.has(id)) {
      assert.match(
        entry.body,
        /(Estimated|Modeled):.*about 30 drivers/i,
        `${id} must present the 30-driver count as estimated or modeled`,
      );
    }
  }
});

test('sanitizePublicMarkdown removes internal artifact jargon from public transport content', () => {
  const source = [
    '**Spec:** SPEC-065 | **Epic:** EPIC-031 | **Initiative:** INITIATIVE-006',
    '',
    'As documented in SPEC-062, the district is short drivers. (TC-009, SPEC-064)',
    '',
    '*Sources: SPEC-060 through SPEC-065; Transportation Claims Catalog (TC-001 through TC-011).*',
  ].join('\n');

  const output = sanitizePublicMarkdown(source);

  assert.equal(output.includes('SPEC-065'), false);
  assert.equal(output.includes('EPIC-031'), false);
  assert.equal(output.includes('INITIATIVE-006'), false);
  assert.equal(output.includes('TC-009'), false);
  assert.match(output, /staffing analysis/);
  assert.match(output, /care-gap analysis/);
});

test('sanitizePublicMarkdown removes internal source references from public briefing prose', () => {
  const source = [
    'The district has not provided analysis on the following (sourced from the Transportation Claims Catalog and linked SPECs):',
    '',
    '**PERSONA-015 | FY27 Budget Analysis | 2026-03-31**',
    '',
    '*Sources: SPEC-060 through SPEC-065; Transportation Claims Catalog (TC-001 through TC-011).*',
  ].join('\n');

  const output = sanitizePublicMarkdown(source);

  assert.equal(output.includes('Transportation Claims Catalog'), false);
  assert.equal(output.includes('PERSONA-015'), false);
  assert.equal(output.includes('SPEC-060'), false);
  assert.equal(output.includes('TC-001'), false);
});

test('sanitizePublicMarkdown removes Variant C and replaces attendance-boundary jargon', () => {
  const source = [
    '| Metric | Option A | Option B | Variant C |',
    '|---|---|---|---|',
    '| Drivers needed | 30 | 24 | 29 |',
    '',
    'No attendance boundaries have been drawn. Families need attendance boundary proposals before route planning starts.',
  ].join('\n');

  const output = sanitizePublicMarkdown(source);

  assert.equal(output.includes('Variant C'), false);
  assert.match(output, /\| Metric \| Option A \| Option B \|/);
  assert.match(output, /school assignment lines/i);
});
