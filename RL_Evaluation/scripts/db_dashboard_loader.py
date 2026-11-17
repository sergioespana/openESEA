"""
Pulls the 16 tool-inspired dashboards seeded by seed_dummy_data.py out of the
local Postgres DB (esea_db) and converts each into the RL model's input
format (matching dashboard_fixture.py's schema), writing one JSON file per
dashboard into RL_Evaluation/dashboards/.

Conversion rules (derived directly from
openESEA_interpreter/frontend/src/views/organisation/OrganisationDashboard.vue,
lines ~244-260, the code that builds this exact payload for the live RL
endpoint):
  - Data Items = numberOfDataPoints * amountOfValueFields, where:
    - amountOfValueFields = count of DataConfiguration keys containing
      "Value Field" (1 for Single/Bar/Pie/Line's "Value Field"; 2 for
      Radial/Progress's "Current Value Field" + "Target Value Field").
    - numberOfDataPoints = number of fetched data rows. For visualisations
      with a "Category Field" (Bar/Pie/Line, categorised by Year in this
      seed data), that's the number of years the organisation has reported
      for (confirmed via DB query: every seeded organisation has exactly one
      QuestionResponse per indicator per year across 2022-2025 -> 4 years).
      For visualisations with no "Category Field" (Single/Radial/Progress),
      the display shows one current snapshot -> numberOfDataPoints = 1.
  - Item Limit Enabled = Category Limit > 0; Item Limit = Category Limit.
    All 16 seeded dashboards have Category Limit = 0 everywhere (no limits
    configured on template dashboards prior to any user edits), so every
    visualisation starts with no item limit - the RL model's job in this
    context is entirely about whether it recommends adding one.
  - Display Area per visualisation = its Position box area (X End - X
    Start) * (Y End - Y Start), in percentage-of-canvas units; dashboard
    Display Area = 100 * 100 (a 0-100% x 0-100% canvas).

Excluded: dashboard #26 "ESEA Standard" - this is the platform's own default
dashboard (not modelled after an external ESG tool) and uses a different,
incompatible DataConfiguration schema (plural "Indicators"/"Values" lists
instead of a single Indicator + Category Field), so it doesn't fit the
conversion rule above without a separate special case. All 16 tool-inspired
dashboards use only 6 of the model's 11 supported visualisation types:
Single Value Display, Radial Progress Bar, Progress Bar, Bar Chart, Pie
Chart, Line Chart - worth noting in the thesis writeup.
"""
import json
import os
import re
import sys

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')

import django  # noqa: E402
django.setup()

from core.models import Dashboard  # noqa: E402

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'dashboards'))
YEARS_PER_ORGANISATION = 4  # confirmed via DB: every seeded org has 2022-2025 data for every indicator
EXCLUDED_DASHBOARD_NAMES = {'ESEA Standard'}


def slugify(name):
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')


def convert_visualisation(vis):
    dd = vis.get('DataDisplay', {})
    vtype = dd.get('Type')
    dc = dd.get('DataConfiguration', {})

    value_field_count = sum(1 for key in dc if 'Value Field' in key)
    has_category_field = 'Category Field' in dc
    number_of_data_points = YEARS_PER_ORGANISATION if has_category_field else 1
    data_items = number_of_data_points * max(value_field_count, 1)

    category_limit = dc.get('Category Limit') or 0
    item_limit_enabled = category_limit > 0

    position = vis.get('Position', {})
    width = position.get('X End', 100) - position.get('X Start', 0)
    height = position.get('Y End', 100) - position.get('Y Start', 0)
    display_area = max(width * height, 1)

    return {
        'Visualisation Title': vis.get('Title', ''),
        'Selection Configuration': {},
        'Visualisation Type': vtype,
        'Data Items': data_items,
        'Item Limit Enabled': item_limit_enabled,
        'Item Limit': category_limit,
        'Display Area': display_area,
    }


def convert_dashboard(specification):
    visualisations = []
    for overview in specification.get('Overviews', []):
        for container in overview.get('BodySection', {}).get('Containers', []):
            for vis in container.get('Visualisations', []):
                visualisations.append(convert_visualisation(vis))
    return {
        'Display Area': 100 * 100,
        'Visualisations': visualisations,
    }


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)

    manifest = []
    for d in Dashboard.objects.all().order_by('id'):
        name = d.specification.get('Name')
        if name in EXCLUDED_DASHBOARD_NAMES:
            print('Skipping (excluded):', name)
            continue

        converted = convert_dashboard(d.specification)
        num_overviews = len(d.specification.get('Overviews', []))
        slug = 'real_' + slugify(name)
        path = os.path.join(OUT_DIR, slug + '.json')
        with open(path, 'w') as f:
            json.dump(converted, f, indent=2)

        type_counts = {}
        for v in converted['Visualisations']:
            type_counts[v['Visualisation Type']] = type_counts.get(v['Visualisation Type'], 0) + 1

        manifest.append({
            'slug': slug,
            'name': name,
            'num_overviews': num_overviews,
            'num_visualisations': len(converted['Visualisations']),
            'type_counts': type_counts,
        })
        print('Wrote {} - {} visualisations across {} overview(s) - {}'.format(
            path, len(converted['Visualisations']), num_overviews, type_counts))

    manifest_path = os.path.join(OUT_DIR, '_real_dashboards_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print('\nWrote manifest to', manifest_path)
