# Succes
# ..from models import specificmodel

# import pandas as pd


def audit_data(eseaaccount, indicators):
    for indicator in indicators.values():
        print(indicator.name, indicator.value)

        # DirectIndicator.objects.filter(datatype=)