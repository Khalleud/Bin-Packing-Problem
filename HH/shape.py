import shap
import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import plot_importance
exacts = []
Heuristics = ['FF','MF','BF','NF']
MetaHeuristics = ['RC','AG']

training = pd.read_csv('csv/training.csv')

def shape(model,df):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)
    shap.summary_plot(shap_values,df)


for df in ['FF','BF','RC']:
   training["shap"] = training["target"].apply(lambda x:1 if x ==df else 0)
   model = xgb.XGBRegressor(n_estimators=100,max_depth=3)
   target = training.pop("shap")
   model.fit(training.drop('target',axis=1),target)
  # shape(model,training.drop('target',axis=1))
   plot_importance(model,title=df)
   plt.show()
   plt.title('shap values for '+df)
  # plt.close()
