from abc import ABC, abstractmethod

from dataclasses import dataclass

from Dashboard.Classes import Visualisation, Dashboard

@dataclass
class Action(ABC):
    visualisationIndex: int

    def getVisualisation(self, dashboard: Dashboard):
        return dashboard.visualisations[self.visualisationIndex]
        
    def execute(self, dashboard: Dashboard):
        visualisation = self.getVisualisation(dashboard)
        return self.act(visualisation)

    @abstractmethod
    def act(self, visualisation: Visualisation):
        return None
