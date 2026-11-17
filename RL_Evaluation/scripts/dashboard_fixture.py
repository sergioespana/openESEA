"""
Representative dashboard states used for the RL evaluation brief.

NOTE ON PROVENANCE: the repository/logs do not retain a serialized copy of
the exact dashboard used for the thesis's original 100-episode training run,
so `TRAINING_DASHBOARD` below is a reconstruction that is representative of
a typical openESEA dashboard (mixed chart types, mixed data-item counts,
some in need of decluttering / retyping, some already fine) rather than a
byte-for-byte replay of the original. `SENSITIVITY_STATE_BAR_5` reuses the
exact worked example from the thesis's Action Space subsection (bar chart,
5 data points, state vector [5, 1, 0.06, 0, 0.02, 0]).
"""


def _vis(title, vis_type, data_items, item_limit_enabled, item_limit, display_area):
    return {
        'Visualisation Title': title,
        'Selection Configuration': {},
        'Visualisation Type': vis_type,
        'Data Items': data_items,
        'Item Limit Enabled': item_limit_enabled,
        'Item Limit': item_limit,
        'Display Area': display_area,
    }


# Representative multi-visualisation dashboard for Goal 1 training run.
TRAINING_DASHBOARD = {
    'Display Area': 2000,
    'Visualisations': [
        _vis('Revenue by Quarter', 'Bar Chart', 5, False, 0, 400),
        _vis('Cost Breakdown', 'Pie Chart', 8, False, 0, 300),
        _vis('Daily Active Users', 'Line Chart', 20, False, 0, 500),
        _vis('Total Headcount', 'Single Value Display', 1, False, 0, 200),
        _vis('Onboarding Completion', 'Progress Bar', 2, False, 0, 200),
        _vis('Regional Sales Table', 'Table', 12, False, 0, 400),
    ],
}

# Larger, more varied dashboard: 15 visualisations spanning every
# visualisation type, a wide spread of data-item counts (1-50), and a mix of
# already-appropriate configurations, already-decluttered ones, and clearly
# problematic ones (oversized tables/charts, wrong type for the data size).
# Used as a second Goal 1 training run to compare against the smaller
# 6-visualisation TRAINING_DASHBOARD baseline.
TRAINING_DASHBOARD_LARGE = {
    'Display Area': 1500,
    'Visualisations': [
        _vis('Quarterly Revenue', 'Bar Chart', 5, False, 0, 100),
        _vis('Product Sales (All SKUs)', 'Bar Chart', 25, False, 0, 100),
        _vis('Emissions by Scope', 'Pie Chart', 4, False, 0, 100),
        _vis('Supplier Breakdown', 'Pie Chart', 12, False, 0, 100),
        _vis('Short-Term Trend', 'Line Chart', 3, False, 0, 100),
        _vis('Daily Active Users (Full History)', 'Line Chart', 50, True, 20, 100),
        _vis('Total Employees', 'Single Value Display', 1, False, 0, 100),
        _vis('Malformed KPI Card', 'Single Value Display', 3, False, 0, 100),
        _vis('Onboarding Completion', 'Progress Bar', 2, False, 0, 100),
        _vis('Target Attainment', 'Radial Progress Bar', 1, False, 0, 100),
        _vis('Water Usage Fraction', 'Fractional Value Display', 2, False, 0, 100),
        _vis('Headcount by Department', 'Grouped Bar Chart', 10, False, 0, 100),
        _vis('Revenue by Region (Stacked)', 'Stacked Bar Chart', 8, False, 0, 100),
        _vis('Raw Transactions Table', 'Table', 30, False, 0, 100),
        _vis('Multi-Region Sales Trend', 'Multi-Series Line Chart', 15, True, 10, 100),
    ],
}

# Thesis worked example: bar chart, 5 data points, item limit enabled at 6
# (i.e. the limit does not currently trim anything), state vector
# [5, 1, 0.06, 0, 0.02, 0] -> [VisualisationType.BAR, itemLimitEnabled=True,
# itemLimit/MAX_ITEM_LIMIT=6/100, itemLimitLarge=False,
# dataItems/MAX_DATA_ITEMS=5/250, manyDataItems=False].
SENSITIVITY_STATE_BAR_5 = {
    'Display Area': 100,
    'Visualisations': [
        _vis('Bar Chart Example', 'Bar Chart', 5, True, 6, 100),
    ],
}

# Second, more complex test case for Goal 2 robustness check: a multi-item
# pie chart that is over the recommended slice count and could plausibly be
# retyped to a bar chart or have a limit added.
SENSITIVITY_STATE_PIE_9 = {
    'Display Area': 100,
    'Visualisations': [
        _vis('Pie Chart Example', 'Pie Chart', 9, False, 0, 100),
    ],
}
