import pandas as pd
from pandas import read_csv
import numpy as np


def outlier_detection(organisation, indicator, data, verbose=False):    
    anomalies = []
    
    data_mean = np.mean(data)    
    data_std = np.std(data)
    anomaly_cut_off = data_std * 3

    lower_limit = indicator.cut_off_lower_limit if indicator.cut_off_lower_limit else (data_mean - anomaly_cut_off)
    upper_limit = indicator.cut_off_upper_limit if indicator.cut_off_upper_limit else (data_mean + anomaly_cut_off)

    # Generate outliers
    value = data[organisation]
    
    if verbose:
        print('\n','indicator:', indicator.key, 'value:', 'lower_limit:', lower_limit, value, 'upper_limit:', upper_limit, 'mean:', data_mean, 'std*3', anomaly_cut_off)

    if value > upper_limit or value < lower_limit:
        return True

    return False



    '''
    data = for one indicator the answer from all esea accounts

    for indicator in esea method:
    for indicators with integers/floats without range
    Function to Detection Outlier on one-dimentional datasets.
    get indicator_audit object (with the specificed lowerlimit & upperlimit) if it exists
    '''