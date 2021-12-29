import pandas as pd
from pandas import read_csv
import numpy as np

def outlier_detection(organisation, indicator, data):
    # data = for one indicator the answer from all esea accounts

    # for indicator in esea method:
    # for indicators with integers/floats without range
    
    # Function to Detection Outlier on one-dimentional datasets.



    # get indicator_audit object (with the specificed lowerlimit & upperlimit) if it exists

    
    #define a list to accumlate anomalies
    anomalies = []
    # Set upper and lower limit to 3 standard deviation
    
    data_mean = np.mean(data)
    print(data, data_mean)
    
    data_std = np.std(data)
    anomaly_cut_off = data_std * 3
    print('------', anomaly_cut_off)

    if indicator.cut_off_lower_limit:
        lower_limit = indicator.cut_off_lower_limit
    else:
        lower_limit  = data_mean - anomaly_cut_off 

    if indicator.cut_off_upper_limit:
        upper_limit = indicator.cut_off_upper_limit
    else:
        upper_limit = data_mean + anomaly_cut_off

    # Generate outliers
    #for index, value in data.iteritems():
    value = data[organisation]
    
    print('value:', value, 'upper_limit:', upper_limit, 'lower_limit:', lower_limit)

    if value > upper_limit or value < lower_limit:
        return True
    return False