const ROWS = [
  {
    key: 'split_families',
    label: 'Split families',
    sourceSlug: 'split-family-model',
  },
  {
    key: 'mv_exposure_annual',
    label: 'McKinney-Vento exposure',
    sourceSlug: 'mckinney-vento-exposure',
  },
  {
    key: 'sea_staffing_gap',
    label: 'SEA staffing gap',
    sourceSlug: 'sea-staffing-assessment',
  },
  {
    key: 'bus_tiers',
    label: 'Bus tiers needed',
    sourceSlug: 'bell-schedule-analysis',
  },
  {
    key: 'care_gap_annual_cost',
    label: 'Family care cost',
    sourceSlug: 'before-after-care-gap',
  },
  {
    key: 'total_annual_fiscal_exposure',
    label: 'Total fiscal exposure',
    sourceSlug: 'transport-configuration-comparison',
  },
  {
    key: 'as_pct_of_claimed_savings',
    label: 'As % of claimed savings',
    sourceSlug: 'transport-configuration-comparison',
  },
];

function formatPercentRange(value) {
  if (!value) return '—';
  return `${value.low.toFixed(1)}%-${value.high.toFixed(1)}%`;
}

function formatCareGapRange(config) {
  const cost = config.care_gap_annual_cost;
  const families = config.care_gap_families;

  if (!cost) return '—';
  if (!families) return cost;
  if (families === '0-0' || families === '0') return `${cost} (0 families)`;

  return `${cost} (${families} families)`;
}

export function getConfigurationNames(comparison) {
  return comparison.configurations
    .filter((config) => config.configuration !== 'Variant C')
    .map((config) => config.configuration);
}

export function getComparisonRows(comparison) {
  const visibleConfigurations = comparison.configurations.filter((config) => config.configuration !== 'Variant C');
  return ROWS.map((row) => {
    const values = {};
    for (const config of visibleConfigurations) {
      values[config.configuration] =
        row.key === 'as_pct_of_claimed_savings'
          ? formatPercentRange(config[row.key])
          : row.key === 'care_gap_annual_cost'
            ? formatCareGapRange(config)
          : config[row.key] ?? '—';
    }

    return {
      ...row,
      values,
    };
  });
}
