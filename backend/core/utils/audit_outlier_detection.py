import pandas as pd
from pandas import read_csv
import numpy as np

def outlier_detection(data):
    # data = for one indicator the answer from all esea accounts

    # for indicator in esea method:
    # for indicators with integers/floats without range
    
    # Function to Detection Outlier on one-dimentional datasets.



    # get indicator_audit object (with the specificed lowerlimit & upperlimit) if it exists

    
    #define a list to accumlate anomalies
    anomalies = []
    # Set upper and lower limit to 3 standard deviation
    
    data_mean = np.mean(data)

    # if indicator_audit object:
    #     lower_limit = indicator_audit.cut_offLowerLimit
    #     upper_limit = indicator_audit.cut_offUpperLimit
    # else:
    if True:
        data_std = np.std(data)
        anomaly_cut_off = data_std * 3
        lower_limit  = data_mean - anomaly_cut_off 
        upper_limit = data_mean + anomaly_cut_off

    # Generate outliers
    #for index, value in data.iteritems():
    value = data[company_index]
    if value > upper_limit or value < lower_limit:
        return anomaly
    

    anomalies.append({ 'indicator': indicator, 'value': anomaly })

    return True