import json
import os
import sys

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')

import django  # noqa: E402
django.setup()

from core.models import Dashboard, DirectIndicator, QuestionResponse, EseaAccount, Organisation  # noqa: E402

dashboards = list(Dashboard.objects.all())
print('Total dashboards in DB:', len(dashboards))
for d in dashboards:
    print('-', d.id, d.specification.get('Name'))

print()
print('=== First dashboard raw structure (truncated) ===')
first = dashboards[0].specification
print(json.dumps(first, indent=2)[:3000])

print()
print('=== Orgs / years available ===')
for org in Organisation.objects.all():
    years = list(EseaAccount.objects.filter(organisation=org).values_list('year', flat=True))
    print(org.id, org.name, 'years:', sorted(years))

print()
print('=== Sample DirectIndicator ===')
di = DirectIndicator.objects.first()
print(di.id, di.method_id, di.key, di.name, di.datatype)
print('QuestionResponse count for this indicator:', QuestionResponse.objects.filter(direct_indicator_id=di.id).count())
