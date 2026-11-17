import json
import os
import sys

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')

import django  # noqa: E402
django.setup()

from core.models import Dashboard  # noqa: E402

seen_types = {}

for d in Dashboard.objects.all():
    spec = d.specification
    name = spec.get('Name')
    for overview in spec.get('Overviews', []):
        containers = overview.get('BodySection', {}).get('Containers', [])
        for container in containers:
            for vis in container.get('Visualisations', []):
                dd = vis.get('DataDisplay', {})
                vtype = dd.get('Type')
                dc = dd.get('DataConfiguration', {})
                keys = tuple(sorted(dc.keys()))
                seen_types.setdefault(vtype, {})
                seen_types[vtype].setdefault(keys, [])
                if len(seen_types[vtype][keys]) < 1:
                    seen_types[vtype][keys].append((name, vis.get('Title'), dc))

print('=== Distinct visualisation types + DataConfiguration key shapes ===')
for vtype, shapes in seen_types.items():
    print('\n---', vtype, '---')
    for keys, examples in shapes.items():
        print('  keys:', keys)
        for dashboard_name, title, dc in examples:
            print('   e.g.', dashboard_name, '|', title, '|', json.dumps(dc))
