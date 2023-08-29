from .Classes import VisualisationType, Visualisation, Dashboard

from .Information import MAX_ITEM_LIMIT, MAX_DATA_ITEMS

from typing import Dict

VISUALISATION_TYPE_MAPPING: Dict[str, VisualisationType] = {
    'Pie': VisualisationType.PIE,
    'Bar': VisualisationType.BAR,
    'Line': VisualisationType.LINE
}

def parseVisualisation(visualisation) -> Visualisation:
    # Get visualisation type and lookup enum value
    visualisationTypeString = visualisation['Visualisation Type']
    visualisationType = VISUALISATION_TYPE_MAPPING[visualisationTypeString]

    # Get config -> if item limit is enabled
    itemLimitEnabled = visualisation['Item Limit Enabled']

    # Get item limit
    itemLimit = visualisation.get('Item Limit', 0)
    itemLimitLarge = itemLimit >= MAX_ITEM_LIMIT
    if itemLimitLarge: itemLimit = MAX_ITEM_LIMIT

    # Get amount of data items
    dataItems = visualisation['Data Items']
    manyDataItems = dataItems >= MAX_DATA_ITEMS 
    if manyDataItems: dataItems = MAX_DATA_ITEMS

    return Visualisation(visualisationType, itemLimitEnabled, itemLimitLarge, itemLimit, manyDataItems, dataItems)

def parseDashboard(dashboard) -> Dashboard:
    return Dashboard([parseVisualisation(visualisation) for visualisation in dashboard])
