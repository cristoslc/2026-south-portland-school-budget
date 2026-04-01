import test from 'node:test';
import assert from 'node:assert/strict';

import {
  getConfigurationNames,
  getComparisonRows,
} from '../src/lib/transport-comparison.js';

import comparison from '../../dist/transportation-analysis/transport-comparison.json' with { type: 'json' };

test('getConfigurationNames preserves the transport comparison order', () => {
  assert.deepEqual(getConfigurationNames(comparison), ['Option A', 'Option B', 'Variant C']);
});

test('getComparisonRows exposes key metric rows with source slugs', () => {
  const rows = getComparisonRows(comparison);

  assert.deepEqual(
    rows.map((row) => row.key),
    [
      'split_families',
      'mv_exposure_annual',
      'sea_staffing_gap',
      'bus_tiers',
      'care_gap_annual_cost',
      'total_annual_fiscal_exposure',
      'as_pct_of_claimed_savings',
    ],
  );

  assert.equal(rows[0].sourceSlug, 'split-family-model');
  assert.equal(rows[1].sourceSlug, 'mckinney-vento-exposure');
  assert.equal(rows[2].sourceSlug, 'sea-staffing-assessment');
  assert.equal(rows[3].sourceSlug, 'bell-schedule-analysis');
  assert.equal(rows[4].sourceSlug, 'before-after-care-gap');
  assert.equal(rows[5].sourceSlug, 'transport-configuration-comparison');
  assert.equal(rows[6].values['Option A'], '47.9%-119.1%');
});
