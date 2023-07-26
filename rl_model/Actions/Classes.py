from dataclasses import dataclass

from Dashboard.Classes import VisualisationType, Dashboard

@dataclass
class ChangeVisualisationType:
    visualisationIndex: int
    visualisationType: int

    def act(self, dashboard: Dashboard):
        dashboard.visualisations[self.visualisationIndex].visualisationType = VisualisationType(self.visualisationType)

@dataclass
class AddItemLimit:
    visualisationIndex: int
    itemLimit: int

    def act(self, dashboard: Dashboard):
        dashboard.visualisations[self.visualisationIndex].itemLimitEnabled = True
        dashboard.visualisations[self.visualisationIndex].itemLimit = self.itemLimit
        
@dataclass
class RemoveItemLimit:
    visualisationIndex: int

    def act(self, dashboard: Dashboard):
        dashboard.visualisations[self.visualisationIndex].itemLimitEnabled = False
        dashboard.visualisations[self.visualisationIndex].itemLimit = 0
