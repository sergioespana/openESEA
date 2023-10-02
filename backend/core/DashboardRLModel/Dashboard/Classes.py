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
    PROGRESS_BAR = 5
    RADIAL_PROGRESS_BAR = 6

@dataclass
class Visualisation:
    visualisationType: VisualisationType

    itemLimitEnabled: bool

    itemLimitLarge: bool
    itemLimit: int

    manyDataItems: bool
    dataItems: int

    displayArea: float

@dataclass
class Dashboard:
    visualisations: List[Visualisation]
    displayArea: float
