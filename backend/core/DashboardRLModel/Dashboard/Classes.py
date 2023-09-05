from dataclasses import dataclass

from enum import IntEnum

from typing import List

# Classes for visualisation(s)

# Integer enumeration for visualisation types
class VisualisationType(IntEnum):
    PIE  = 0
    BAR  = 1
    LINE = 2
    SINGLE = 3
    FRACTIONAL = 4
    PROGRESS = 5

@dataclass
class Visualisation:
    visualisationType: VisualisationType

    itemLimitEnabled: bool

    itemLimitLarge: bool
    itemLimit: int

    manyDataItems: bool
    dataItems: int

@dataclass
class Dashboard:
    visualisations: List[Visualisation]
