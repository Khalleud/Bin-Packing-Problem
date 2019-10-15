import pandas as pd
import numpy as np

df = pd.read_csv('../NF/csv/Parameters.csv',index_col=0,squeeze=True,header=None)#because this file will be executed from the HH directory
C=int(df['C'])
Weights = np.array(eval(df['Weights']))
