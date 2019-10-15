import pandas as pd
import tensorflow as tf
import numpy as np
import sys

tab = []
for arg in range(2, len(sys.argv)):
    tab.append(int(arg))
poid_max = int(sys.argv[1])

def restore_model(filename):
    return tf.keras.models.load_model(filename)


def get_problem_feature(tab, poid_max):  # get problem feature which will be used in the training
    tab=pd.Series(tab)
    mean = tab.mean()
    std = tab.std()
    dist_mean_poidMax = np.abs(mean - poid_max)
    division_mean_poidMax = mean / poid_max
    division_mean_std_poidMax = mean * std / poid_max
    dist_max_poidMax = np.abs(tab.max() - poid_max)
    kurtosis = tab.kurtosis()
    skewness = tab.skew()
    return np.array(
        [[len(tab), poid_max, mean, dist_mean_poidMax, division_mean_poidMax, division_mean_std_poidMax, kurtosis,
         skewness, dist_max_poidMax, std]])


encode = {'FF': 0, 'BF': 1, 'MF': 2, 'NF': 3, 'RC': 4, 'AG2': 5}
decode = {0: 'FF', 1: 'BF', 2: 'MF', 3: 'NF', 4: 'RC', 5: 'AG'}

model = restore_model('HH/models/RNN.pk')
# features = ['n','poid_max','mean','dist_mean_poidMax','division_mean_poidMax','division_mean_std_poidMax','kurtosis','skewness','dist_max_poidMax','std']

problem_features = get_problem_feature(tab, poid_max)
# 'le meilleur algorithme a utilisÃ© est :' +
print(decode[np.argmax(model.predict(problem_features))])