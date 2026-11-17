"""
One-off export of the Python dashboard fixtures into RL_Evaluation/dashboards/
as JSON, so Goal 4 scripts can treat "a folder of dashboard specifications"
as the uniform input format (existing fixtures + later, real dashboards
pulled from the database, dropped into the same folder).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from dashboard_fixture import TRAINING_DASHBOARD, TRAINING_DASHBOARD_LARGE  # noqa: E402

OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'dashboards'))

EXPORTS = {
    'small': TRAINING_DASHBOARD,
    'large': TRAINING_DASHBOARD_LARGE,
}

if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, dashboard in EXPORTS.items():
        path = os.path.join(OUT_DIR, name + '.json')
        with open(path, 'w') as f:
            json.dump(dashboard, f, indent=2)
        print('Wrote', path)
