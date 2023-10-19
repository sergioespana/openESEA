from .Classes import VisualisationType, Visualisation, Dashboard

from .Information import MAX_ITEM_LIMIT, MAX_DATA_ITEMS

from typing import Dict

VISUALISATION_TYPE_MAPPING: Dict[str, VisualisationType] = {
    'Single Value Display': VisualisationType.SINGLE,
    'Fractional Value Display': VisualisationType.FRACTIONAL,
    'Radial Progress Bar': VisualisationType.RADIAL_PROGRESS_BAR,
    'Progress Bar': VisualisationType.PROGRESS_BAR,
    'Pie Chart': VisualisationType.PIE,
    'Bar Chart': VisualisationType.BAR,
    'Grouped Bar Chart': VisualisationType.GROUPED_BAR,
    'Stacked Bar Chart': VisualisationType.STACKED_BAR,
    'Line Chart': VisualisationType.LINE,
    'Multi-Series Line Chart': VisualisationType.MULTI_SERIES_LINE,
    'Table': VisualisationType.TABLE
}

# Reverse mapping
VISUALISATION_NAME_MAPPING: Dict[VisualisationType, str] = {
    VISUALISATION_TYPE_MAPPING[name]: name for name in VISUALISATION_TYPE_MAPPING
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

    # Display area
    displayArea = visualisation['Display Area']

    return Visualisation(visualisationType, itemLimitEnabled, itemLimitLarge, itemLimit, manyDataItems, dataItems, displayArea)

def parseDashboard(dashboard) -> Dashboard:
    displayArea = dashboard['Display Area']
    visualisations = dashboard['Visualisations']
    return Dashboard([parseVisualisation(visualisation) for visualisation in visualisations], displayArea)
