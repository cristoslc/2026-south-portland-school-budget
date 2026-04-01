import test from 'node:test';
import assert from 'node:assert/strict';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

const DIST_ROOT = new URL('../dist/transportation-analysis/', import.meta.url);
const BRIEFINGS_DIR = new URL('./briefings/', DIST_ROOT);

const FORBIDDEN_PATTERNS = [
  /INITIATIVE-\d+/,
  /EPIC-\d+/,
  /SPEC-\d+/,
  /Variant C/,
  /attendance boundary/i,
  /attendance boundaries/i,
  /Transportation Claims Catalog/,
  /source_specs/,
  /Machine-Readable Data/,
  /Source Data/,
  /Sources of Error/,
  /How to Improve This Analysis/,
  /Detailed analysis supporting the transportation comparison and transport briefing pages/,
  /translate the transport model into stakeholder-specific language/i,
  /critical path item/i,
  /did not exist when the board voted/i,
  /the city has to make work/i,
];

test('built transport pages do not expose internal project framing', async () => {
  const briefingEntries = await readdir(BRIEFINGS_DIR, { withFileTypes: true });
  const pages = [
    new URL('./index.html', DIST_ROOT),
    ...briefingEntries.map((entry) =>
      entry.isDirectory() ? new URL(`./${entry.name}/index.html`, BRIEFINGS_DIR) : new URL(`./${entry.name}`, BRIEFINGS_DIR),
    ),
  ];

  for (const page of pages) {
    const html = await readFile(page, 'utf8');

    for (const pattern of FORBIDDEN_PATTERNS) {
      assert.equal(
        pattern.test(html),
        false,
        `${path.basename(path.dirname(page.pathname)) || path.basename(page.pathname)} leaked ${pattern}`,
      );
    }
  }
});

test('post-decision brief explains the modeled family-care cost range with affected-family range', async () => {
  const html = await readFile(new URL('./post-decision-brief/index.html', DIST_ROOT), 'utf8');

  assert.match(html, /\$143,640-\$803,520/);
  assert.match(html, /42-144 families/);
});

test('landing page comparison contextualizes family-care cost range with affected-family range', async () => {
  const html = await readFile(new URL('./index.html', DIST_ROOT), 'utf8');

  assert.match(html, /Family care cost/);
  assert.match(html, /\$143,640-\$803,520 \(42-144 families\)/);
});
