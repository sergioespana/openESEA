from dataclasses import dataclass

from enum import IntEnum

from typing import List

# Classes for visualisation(s)

# Integer enumeration for visualisation types
class VisualisationType(IntEnum):
    SINGLE = 0
    FRACTIONAL = 1
    PROGRESS_BAR = 2
    RADIAL_PROGRESS_BAR = 3
    PIE  = 4
    BAR  = 5
    GROUPED_BAR = 6
    STACKED_BAR = 7
    LINE = 8
    MULTI_SERIES_LINE = 9
    TABLE = 10

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
