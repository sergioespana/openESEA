import pandas as pd
from pandas import read_csv
import numpy as np
from numpy.core import numeric
# import matplotlib.pyplot as plt
# import seaborn as sns

import benford as bf

def calculate_benfords_law(indicator_array):
    # Calculate benfords law for all Integer/Float values that don't have a defined range
    for value in indicator_array:
        print('--->', type(value))
    first_digit = bf.first_digits(indicator_array, digs=1, decimals=8, MAD=True, confidence=95,
                     chi_square=True, KS=True) # save_plot=True
    
    second_digit = bf.second_digit(indicator_array, decimals=8, MAD=True, confidence=95,
                     chi_square=True, KS=True) # save_plot=True   

    first_two_digits = bf.first_digits(indicator_array, digs=2, decimals=8,MAD=True, confidence=95, 
                    chi_square=True, KS=True) # save_plot=True

    # Create and return 3 images()
    return()