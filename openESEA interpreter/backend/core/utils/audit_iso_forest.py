# from sklearn.ensemble import IsolationForest
import pandas as pd

def calculate_iso_forest():
    #Creating the model
    model=IsolationForest(n_estimators=50, 
                        max_samples='auto', 
                        contamination=float(0.1),
                        max_features=1.0)

    #fitting the model on one feature for unsupervised learning
    model.fit(df[['column']])

    df['scores']=model.decision_function(df[['column']])
    df['anomaly']=model.predict(df[['column']])
    df2.tail()


    anomaly=df.loc[df['anomaly']==-1]

    anomaly_index=list(anomaly.index)

    print(anomaly)
    return True