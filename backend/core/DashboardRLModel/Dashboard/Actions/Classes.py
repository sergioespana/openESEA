from ..Classes import VisualisationType, Dashboard

from dataclasses import dataclass

@dataclass
class ChangeVisualisationType:
    visualisationIndex: int
    visualisationType: int

    def act(self, dashboard: Dashboard):
        dashboard.visualisations[self.visualisationIndex].visualisationType = VisualisationType(self.visualisationType)

    def to_dict(self):
        action_dict = {
            'Type': 'Change Visualisation Type',
            'Visualisation Index': self.visualisationIndex,
            'Visualisation Type': VisualisationType(self.visualisationType).name
        }
        return action_dict

@dataclass
class AddItemLimit:
    visualisationIndex: int
    itemLimit: int

    def act(self, dashboard: Dashboard):
        dashboard.visualisations[self.visualisationIndex].itemLimitEnabled = True
        dashboard.visualisations[self.visualisationIndex].itemLimit = self.itemLimit

    def to_dict(self):
        action_dict = {
            'Type': 'Add Item Limit',
            'Visualisation Index': self.visualisationIndex,
            'Item Limit': self.itemLimit
        }
        return action_dict
        
@dataclass
class RemoveItemLimit:
    visualisationIndex: int

    def act(self, dashboard: Dashboard):
        dashboard.visualisations[self.visualisationIndex].itemLimitEnabled = False
        dashboard.visualisations[self.visualisationIndex].itemLimit = 0

    def to_dict(self):
        action_dict = {
            'Type': 'Remove Item Limit',
            'Visualisation Index': self.visualisationIndex
        }
        return action_dict
