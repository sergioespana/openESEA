import numpy as np

def categorical(integer_value: int, num_categories: int):
    # Initialize zero-valued array for all categories
    array = np.zeros(num_categories, dtype = int)
    # Set category corresponding to given integer to 1
    array[integer_value] = 1
    # Return one hot array
    return array

def boolean(boolean_value: bool):
    # Convert to integer value
    value = int(boolean_value)
    # Return array with value
    return np.array([value])

def integer_and_normalise(integer_value: int, max_value: int):
    # Normalise value
    value = integer_value / max_value
    # Ensure that value is between 0 and 1
    value = max(0, min(1, value))
    # Return array with value
    return np.array([value])
