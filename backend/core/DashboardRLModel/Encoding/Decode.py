import numpy as np

def categorical(array, offset, num_categories: int) -> int:
    # Get index where one hot array is one for the amount of categories
    return np.argmax(array[offset : offset + num_categories])

def boolean(array, offset) -> bool:
    # Get integer value from array
    integer_value = array[offset : offset + 1]
    # Cast back to boolean value
    boolean_value = bool(integer_value)
    # Return boolean value
    return boolean_value

def integer_normalised(array, offset, max_value: int) -> int:
    # Get normalised value from array
    value = array[offset : offset + 1]
    # Multiply and round back to original value
    original_value = round(max_value * value)
    # Return original value
    return original_value
