from .Classes import Visualisation, VisualisationType, Dashboard
from .Information import MAX_ITEM_LIMIT, MAX_DATA_ITEMS, NUM_VISUALISATION_TYPES

from ..Encoding import Encode
from ..Encoding import Decode

import numpy as np

def visualisationToArray(dashboard: Dashboard, visualisation: Visualisation):
    # For each class member encode the value and append to the array
    total_array = np.array([])
    
    visualisationTypeInteger = int(visualisation.visualisationType)
    array = Encode.categorical(visualisationTypeInteger, NUM_VISUALISATION_TYPES)
    total_array = np.append(total_array, array) 
    
    array = Encode.boolean(visualisation.itemLimitEnabled)
    total_array = np.append(total_array, array) 

    array = Encode.boolean(visualisation.itemLimitLarge)
    total_array = np.append(total_array, array) 

    array = Encode.integer_and_normalise(visualisation.itemLimit, MAX_ITEM_LIMIT)
    total_array = np.append(total_array, array) 

    array = Encode.boolean(visualisation.manyDataItems)
    total_array = np.append(total_array, array) 

    array = Encode.integer_and_normalise(visualisation.dataItems, MAX_DATA_ITEMS)
    total_array = np.append(total_array, array) 

    array = Encode.integer_and_normalise(visualisation.displayArea, dashboard.displayArea)
    total_array = np.append(total_array, array) 
    
    return total_array

def dashboardToArray(dashboard: Dashboard):
    array = np.array([])

    for visualisation in dashboard.visualisations:
        array = np.append(array, visualisationToArray(dashboard, visualisation))

    return array

def visualisationFromArray(array) -> Visualisation:
    # For each class member decode the assigned part of the array
    offset = 0

    visualisationTypeInteger = Decode.categorical(array, offset, NUM_VISUALISATION_TYPES)
    visualisationType = VisualisationType(visualisationTypeInteger)
    offset += NUM_VISUALISATION_TYPES

    itemLimitEnabled = Decode.boolean(array, offset)
    offset += 1

    itemLimitLarge = Decode.boolean(array, offset)
    offset += 1

    itemLimit = Decode.integer_normalised(array, offset, MAX_ITEM_LIMIT)
    offset += 1

    manyDataItems = Decode.boolean(array, offset)
    offset += 1

    dataItems = Decode.integer_normalised(array, offset, MAX_DATA_ITEMS)
    offset += 1

    # Currently this function is not used, but we would times this by the dashboard display area
    dashboardDisplayArea = 10000
    dataItems = Decode.integer_normalised(array, offset, dashboardDisplayArea)
    offset += 1

    # Wrap into Visualisation class
    return Visualisation(visualisationType, itemLimitEnabled, itemLimitLarge, itemLimit, manyDataItems, dataItems)

def dashboardFromArray(array) -> Dashboard:
    # Length of a single visualisation: length of one-hot visualisation type + 3 times boolean of length 1 + 2 times of single integer value normalised between [0,1]
    visualisationSize = NUM_VISUALISATION_TYPES + 3 * 1 + 2 * 1
    # Lenght of given array
    arraySize = len(array)
    # This means this many visualisations:
    nr_of_visualisations = arraySize // visualisationSize

    # For each visualisation decode from array and append to list
    visualisations = []
    for i in range(0, nr_of_visualisations):
        visualisationArray = array[i * visualisationSize : (i + 1) * visualisationSize]
        visualisation = visualisationFromArray(visualisationArray)
        visualisations.append(visualisation)

    # Wrap into Dashboard class
    return Dashboard(visualisations)
