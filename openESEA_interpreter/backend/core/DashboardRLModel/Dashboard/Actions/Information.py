from ..Actions.Classes import ChangeVisualisationType, AddItemLimit, RemoveItemLimit

from ..Information import NUM_VISUALISATION_TYPES, MAX_ITEM_LIMIT, MAX_DATA_ITEMS

ACTIONS_INFORMATION = [
    {
        'Action': ChangeVisualisationType,
        'Name': 'Change Visualisation Type',
        'Parameters': [{ 'Values': NUM_VISUALISATION_TYPES, 'Type': 'categorical' }]
    },
    {
        'Action': AddItemLimit,
        'Name': 'Add Item Limit',
        'Parameters': [{ 'Values': MAX_ITEM_LIMIT, 'Type': 'numerical' }]
    },
    {
        'Action': RemoveItemLimit,
        'Name': 'Remove Item Limit',
        'Parameters': []
    }
]

ACTIONS            = [ACTION_INFORMATION['Action']     for ACTION_INFORMATION in ACTIONS_INFORMATION]
ACTIONS_PARAMETERS = [ACTION_INFORMATION['Parameters'] for ACTION_INFORMATION in ACTIONS_INFORMATION]

NUM_ACTIONS = len(ACTIONS)
