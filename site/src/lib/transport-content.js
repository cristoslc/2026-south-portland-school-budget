import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

import { parse as parseYaml } from 'yaml';

const TRANSPORT_ROOT_URL = new URL('../../../dist/transportation-analysis/', import.meta.url);
const TRANSPORT_BRIEFINGS_URL = new URL('./briefings/', TRANSPORT_ROOT_URL);

const TRANSPORT_ANALYSIS_FILES = [
  { id: 'readme', fileName: 'README.md', kind: 'landing' },
  { id: 'post-decision-brief', fileName: 'POST-DECISION-BRIEF.md', kind: 'analysis' },
  { id: 'board-letter', fileName: 'BOARD-LETTER-DRAFT.md', kind: 'resource' },
  { id: 'methodology', fileName: 'METHODOLOGY.md', kind: 'methodology' },
  {
    id: 'transport-configuration-comparison',
    fileName: 'transport-configuration-comparison.md',
    kind: 'analysis',
  },
  { id: 'split-family-model', fileName: 'split-family-model.md', kind: 'analysis' },
  { id: 'mckinney-vento-exposure', fileName: 'mckinney-vento-exposure.md', kind: 'analysis' },
  { id: 'sea-staffing-assessment', fileName: 'sea-staffing-assessment.md', kind: 'analysis' },
  { id: 'bell-schedule-analysis', fileName: 'bell-schedule-analysis.md', kind: 'analysis' },
  { id: 'before-after-care-gap', fileName: 'before-after-care-gap.md', kind: 'analysis' },
];

export const TRANSPORT_COMMUNITY_LENSES = [
  {
    id: 'transport-general',
    label: 'General Community',
    summary: 'Start with the whole-community transportation overview.',
  },
  {
    id: 'transport-families',
    label: 'Families',
    summary: 'For families planning daily pickup, drop-off, and care.',
  },
  {
    id: 'transport-elementary-families',
    label: 'Elementary Families',
    summary: 'For elementary households adjusting to the new transportation plan.',
  },
  {
    id: 'transport-staff',
    label: 'Staff',
    summary: 'For staff members coordinating schedules, routes, and daily routines.',
  },
  {
    id: 'transport-taxpayers',
    label: 'Taxpayers',
    summary: 'For residents tracking the cost and public follow-through.',
  },
  {
    id: 'transport-older-students',
    label: 'Older Students',
    summary: 'For older students and the households that support them.',
  },
  {
    id: 'transport-city-school-leadership',
    label: 'City and School Leadership',
    summary: 'For leaders responsible for implementation and coordination.',
  },
];

const TRANSPORT_COMMUNITY_LENS_BY_ID = new Map(
  TRANSPORT_COMMUNITY_LENSES.map((lens, order) => [lens.id, { ...lens, order }]),
);

export function getTransportCommunityLens(id) {
  return TRANSPORT_COMMUNITY_LENS_BY_ID.get(id) ?? null;
}

export function getTransportCommunityLensEntries(entries) {
  return entries
    .map((entry) => {
      const lens = getTransportCommunityLens(entry.id);
      return lens ? { entry, lens } : null;
    })
    .filter(Boolean)
    .sort((a, b) => a.lens.order - b.lens.order);
}

const PUBLIC_TERM_REPLACEMENTS = new Map([
  ['SPEC-060 through SPEC-065', 'the transport analysis set'],
  ['SPEC-060', 'split-family analysis'],
  ['SPEC-061', 'McKinney-Vento analysis'],
  ['SPEC-062', 'staffing analysis'],
  ['SPEC-063', 'bell schedule analysis'],
  ['SPEC-064', 'care-gap analysis'],
  ['SPEC-065', 'configuration comparison'],
]);

function trimFenceLine(line = '') {
  return line.trim().toLowerCase();
}

export function normalizeTransportMarkdown(source) {
  const normalized = source.replace(/\r\n/g, '\n');
  const lines = normalized.split('\n');
  const firstLine = trimFenceLine(lines[0]);
  const closingFenceIndex = lines.findIndex((line, index) => index > 0 && trimFenceLine(line) === '```');

  if ((firstLine === '```' || firstLine.startsWith('```')) && closingFenceIndex > 0 && lines[1] === '---') {
    return [...lines.slice(1, closingFenceIndex), ...lines.slice(closingFenceIndex + 1)].join('\n').trim();
  }

  return normalized.trim();
}

function extractFrontmatter(source) {
  if (!source.startsWith('---\n')) {
    return { data: {}, body: source.trim() };
  }

  const closingIndex = source.indexOf('\n---\n', 4);
  if (closingIndex === -1) {
    return { data: {}, body: source.trim() };
  }

  const rawFrontmatter = source.slice(4, closingIndex);
  const body = source.slice(closingIndex + 5).trim();
  return { data: parseYaml(rawFrontmatter) ?? {}, body };
}

function stripLeadingDivider(body) {
  return body.replace(/^---\n+/, '').trim();
}

function parseTableCells(line) {
  const trimmed = line.trim();
  if (!trimmed.startsWith('|')) return null;

  const rawCells = trimmed.split('|');
  if (rawCells[0] === '') rawCells.shift();
  if (rawCells.at(-1) === '') rawCells.pop();
  return rawCells.map((cell) => cell.trim());
}

function formatTableCells(cells) {
  return `| ${cells.join(' | ')} |`;
}

function removeVariantCFromTables(body) {
  const lines = body.split('\n');
  const output = [];

  for (let i = 0; i < lines.length; i += 1) {
    const headerCells = parseTableCells(lines[i]);
    const separatorCells = parseTableCells(lines[i + 1] ?? '');

    const isTable =
      headerCells &&
      separatorCells &&
      headerCells.length === separatorCells.length &&
      separatorCells.every((cell) => /^:?-{3,}:?$/.test(cell));

    if (!isTable) {
      output.push(lines[i]);
      continue;
    }

    const variantIndex = headerCells.findIndex((cell) => /Variant C/i.test(cell));
    if (variantIndex === -1) {
      output.push(lines[i], lines[i + 1]);
      i += 1;
      continue;
    }

    output.push(formatTableCells(headerCells.filter((_, index) => index !== variantIndex)));
    output.push(formatTableCells(separatorCells.filter((_, index) => index !== variantIndex)));

    let j = i + 2;
    while (j < lines.length) {
      const rowCells = parseTableCells(lines[j]);
      if (!rowCells || rowCells.length !== headerCells.length) break;
      output.push(formatTableCells(rowCells.filter((_, index) => index !== variantIndex)));
      j += 1;
    }

    i = j - 1;
  }

  return output.join('\n');
}

export function sanitizePublicMarkdown(body) {
  let output = removeVariantCFromTables(body);

  output = output.replace(/^\*\*(Spec|Epic|Initiative|Status|Date):.*$\n?/gim, '');
  output = output.replace(/^\*\*PERSONA-\d+\s*\|.*$\n?/gim, '');
  output = output.replace(/^All calculation scripts:.*$\n?/gim, '');
  output = output.replace(/^Machine-readable comparison:.*$\n?/gim, '');
  output = output.replace(/^\*?(Sources?|Source specifications?):.*$\n?/gim, '');
  output = output.replace(/^The district has not provided analysis on the following \(sourced from the Transportation Claims Catalog and linked SPECs\):\s*$/gim, 'The district has not provided analysis on the following:');
  output = output.replace(/^The district has not produced the analysis that would confirm or contradict the numbers above\. Specific gaps from the Transportation Claims Catalog:\s*$/gim, 'The district has not produced the analysis that would confirm or contradict the numbers above. Key gaps include:');
  output = output.replace(/^The district has not produced the following analyses, despite direct parent requests at the February 4 and March 2 forums \(documented in the Transportation Claims Catalog\):\s*$/gim, 'The district has not produced the following analyses, despite direct parent requests at the February 4 and March 2 forums:');
  output = output.replace(/\(Source:\s*Transportation Claims Catalog[^)]*\)/gim, '');
  output = output.replace(/\battendance boundaries\b/gi, 'school assignment lines');
  output = output.replace(/\battendance boundary proposals\b/gi, 'school assignment proposals');
  output = output.replace(/\battendance boundary interaction\b/gi, 'school assignment interaction');
  output = output.replace(/\battendance boundary\b/gi, 'school assignment line');

  output = output.replace(/\bOption A or Variant C\b/gi, 'Option A');
  output = output.replace(/\bOption A and Variant C\b/gi, 'Option A');
  output = output.replace(/\bVariant C and Option B\b/gi, 'Option B');
  output = output.replace(/\bOption A, Option B, and Variant C\b/gi, 'Option A and Option B');
  output = output.replace(/\bOption A, Option B and Variant C\b/gi, 'Option A and Option B');
  output = output.replace(/\bOption A, Option B, or Variant C\b/gi, 'Option A or Option B');
  output = output.replace(/\bOptions A and Variant C\b/gi, 'Option A');
  output = output.replace(/\bVariant C — the middle option —[^.]*\.\s*/gi, '');
  output = output.replace(/\bUnder Variant C,[^.]*\.\s*/gi, '');
  output = output.replace(/\bEven Variant C[^.]*\.\s*/gi, '');
  output = output.replace(/;\s*Variant C[^.;\n]*/gi, '');
  output = output.replace(/^.*Variant C.*$\n?/gim, '');
  output = output.replace(/Detailed analysis supporting the transportation comparison and transport briefing pages\./gi, 'Use this page to look more closely at one part of the transportation plan and the choices still ahead.');
  output = output.replace(/These briefs translate the transport model into stakeholder-specific language without changing the underlying evidence\./gi, 'These briefs explain the same transportation questions in plain language for different community audiences.');
  output = output.replace(/This document assembles the independent analysis that did not exist when the board voted\./gi, 'This page brings together the transportation analysis that residents may want in one place after the vote.');
  output = output.replace(/The goal is to surface the transportation analysis that did not exist when the board voted -- and to identify what needs to happen before fall 2026\./gi, 'The goal is to help residents understand the transportation questions that still need to be worked through before fall 2026.');
  output = output.replace(/Option A is now the plan the city has to make work\./gi, 'Option A is now the approved plan, and the city, district, staff, and families all need a workable path to September.');
  output = output.replace(/Recruiting 10\+ bus drivers by September 2026 is the critical path item\./gi, 'Recruiting enough bus drivers by September 2026 is one of the biggest near-term tasks.');
  output = output.replace(/This analysis documents what is known; the district has not yet produced the disaggregated analysis required to evaluate equity impact\./gi, 'This analysis summarizes what is publicly available so far and highlights where more detailed local data would help.');
  output = output.replace(/\bThe district has not yet produced\b/gi, 'The district has not yet published');
  output = output.replace(/\bThe district has not announced\b/gi, 'The district has not yet announced');
  output = output.replace(/\bnot optional\b/gi, 'required');

  for (const [needle, replacement] of PUBLIC_TERM_REPLACEMENTS.entries()) {
    output = output.replaceAll(needle, replacement);
  }

  output = output.replace(/\bEPIC-\d+\b/g, '');
  output = output.replace(/\bINITIATIVE-\d+\b/g, '');
  output = output.replace(/\bPERSONA-\d+\b/g, '');
  output = output.replace(/\bTC-\d+\b(?:\s+through\s+TC-\d+\b)?/g, '');
  output = output.replace(/Transportation Claims Catalog/g, '');
  output = output.replace(/\(\s*,\s*/g, '(');
  output = output.replace(/\(\s*\)/g, '');
  output = output.replace(/\s+\./g, '.');
  output = output.replace(/[ \t]{2,}/g, ' ');
  output = output.replace(/\n{3,}/g, '\n\n');

  return output.trim();
}

function deriveTitle(body, fallbackId) {
  const headingMatch = body.match(/^#\s+(.+)$/m);
  if (headingMatch) {
    return headingMatch[1].trim();
  }

  return fallbackId
    .split('-')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

export function parseMarkdownEntry({ id, source, filePath, extraData = {} }) {
  const normalized = normalizeTransportMarkdown(source);
  const { data, body } = extractFrontmatter(normalized);
  const cleanedBody = sanitizePublicMarkdown(stripLeadingDivider(body));
  return {
    id,
    filePath,
    body: cleanedBody,
    data: {
      title: deriveTitle(cleanedBody, id),
      ...data,
      ...extraData,
    },
  };
}

export function getTransportAnalysisEntries() {
  return [...TRANSPORT_ANALYSIS_FILES];
}

async function storeMarkdownEntries(context, entries) {
  context.store.clear();

  for (const entry of entries) {
    const parsedData = await context.parseData({
      id: entry.id,
      data: entry.data,
      filePath: entry.filePath,
    });
    const rendered = await context.renderMarkdown(entry.body, {
      fileURL: pathToFileURL(path.resolve(context.config.root.pathname, entry.filePath)),
    });

    context.store.set({
      id: entry.id,
      data: parsedData,
      body: entry.body,
      filePath: entry.filePath,
      digest: context.generateDigest(`${entry.filePath}\n${entry.body}`),
      rendered,
      assetImports: rendered?.metadata?.imagePaths,
    });
  }
}

export function transportBriefingsLoader() {
  return {
    name: 'transport-briefings-loader',
    load: async (context) => {
      const briefingDir = fileURLToPath(TRANSPORT_BRIEFINGS_URL);
      const files = (await readdir(briefingDir)).filter((file) => file.endsWith('.md')).sort();
      const entries = [];

      for (const fileName of files) {
        const source = await readFile(new URL(fileName, TRANSPORT_BRIEFINGS_URL), 'utf8');
        const id = fileName.replace(/\.md$/, '');
        entries.push(
          parseMarkdownEntry({
            id,
            source,
            filePath: `../dist/transportation-analysis/briefings/${fileName}`,
            extraData: {
              topic: 'transportation',
            },
          }),
        );
      }

      await storeMarkdownEntries(context, entries);
    },
  };
}

export function transportAnalysisLoader() {
  return {
    name: 'transport-analysis-loader',
    load: async (context) => {
      const entries = [];

      for (const config of TRANSPORT_ANALYSIS_FILES) {
        const source = await readFile(new URL(config.fileName, TRANSPORT_ROOT_URL), 'utf8');
        entries.push(
          parseMarkdownEntry({
            id: config.id,
            source,
            filePath: `../dist/transportation-analysis/${config.fileName}`,
            extraData: {
              kind: config.kind,
            },
          }),
        );
      }

      await storeMarkdownEntries(context, entries);
    },
  };
}
