import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


exacts = []
Heuristics = ['FF','BF','MF','NF']
MetaHeuristics = ['RC','AG']

for df in exacts+Heuristics+MetaHeuristics:
    df_ = pd.read_csv('csv/'+df+'.csv')

    for feature in ['n','poid_max','mean','dist_mean_poidMax','division_mean_poidMax','dist_max_poidMax','division_mean_std_poidMax','kurtosis','skewness']:
      if df in MetaHeuristics:
        sns.relplot(x=feature,y='exec_time',hue='nbIteration',data=df_)
        plt.title(feature+' x exec time')
        plt.xlabel(feature)
        plt.ylabel('time')
        plt.savefig('fig/'+df+'/'+feature+'_exec_time.png')
        plt.close()

        sns.relplot(x=feature,y='solution',hue='nbIteration',data=df_)
        plt.title(feature+' x solution')
        plt.xlabel(feature)
        plt.ylabel('solution')
        plt.savefig('fig/'+df+'/'+feature+'_solution.png')
        plt.close()

      else:
        plt.scatter(df_[feature],df_['exec_time'])
        plt.title(feature+' x exec time')
        plt.xlabel(feature)
        plt.ylabel('time')
        plt.savefig('fig/'+df+'/'+feature+'_exec_time.png')
        plt.close()

        plt.scatter(df_[feature],df_['solution'])
        plt.title(feature+' x solution')
        plt.xlabel(feature)
        plt.ylabel('solution')
        plt.savefig('fig/'+df+'/'+feature+'_solution.png')
        plt.close()

      sns.barplot(x='selected',y=feature,data=df_)
      plt.savefig('fig/'+df+'/'+feature+'_barplot_selected')
      plt.close()



training = pd.read_csv('csv/training.csv')
sns.catplot(x="target",kind="count",data=training)
plt.savefig('fig/training/count.png')
