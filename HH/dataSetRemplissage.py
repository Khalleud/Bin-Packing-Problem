import numpy as np
import pandas as pd
from time import time
import subprocess
from multiprocessing import Pool

df_len = 20 #number of problem instance to solve
exacts = []
Heuristics = ['FF','BF','MF','NF']
MetaHeuristics = ['RC','AG2']

features = ['n','poid_max','mean','dist_mean_poidMax','division_mean_poidMax','division_mean_std_poidMax','kurtosis','skewness','dist_max_poidMax']
sorties = ['exec_time','solution']
addtional_variable = {'AG2':['pm','populationBegin','nbIteration'],'RC':['T','nbIteration']}
timeout={'AG':120,'RC':60,'FF':30,'BF':30,'NF':30,'MF':30,'AG2':120}
#addtional_variable = ['pm','nbIteration']

for df in exacts+Heuristics+MetaHeuristics:
    exec(df+'_df=pd.DataFrame({feature:[] for feature in features})')
    if df in MetaHeuristics:
        exec(df+'_df'+'=pd.concat(['+df+'_df,pd.DataFrame([],columns=addtional_variable[df])],axis=1)')


def generer_n(): #generate a random value of n
    random = np.random.random()
    if random < 0.4:
        n = np.random.randint(10,200)
    else:
        n = np.int(np.random.normal(800,10))
    return n

def generer_problem(poid_max,n): #generate an instance of problem
    random = np.random.random()
    if n%2 == 0 :
        p = n//2
        q = n//2
    else :
        p = (n+1)// 2
        q= (n-1)//2

    if random < 0.4:
        distrib =["normal","exponential"]
        weights = np.concatenate([np.random.normal(poid_max/3,10,p),np.random.exponential(poid_max/4,q)])

    elif random <0.7:
        distrib = "uniform"
        weights = np.random.randint(poid_max//5,poid_max,n)

    else:
        distrib = ["normal","uniform"]
        weights = np.concatenate([np.random.normal(poid_max/3,10,p),np.random.randint(poid_max//5,poid_max,q)])

    return pd.Series(weights.astype(int)),distrib


def correct_problem(tab,poid_max): #correcte problem mean if one of the object have weight greater than poid max than transform it to poid max of if weight have value lower than 0 than transform it to 0
     return tab.apply(lambda x:x if (x<=poid_max and x>0) else (poid_max//5 if x<=0 else poid_max))

def get_problem_feature(tab,poid_max): #get problem feature which will be used in the training
    mean = tab.mean()
    std = tab.std()
    dist_mean_poidMax = np.abs(mean - poid_max)
    division_mean_poidMax = mean / poid_max
    division_mean_std_poidMax = mean*std/poid_max
    dist_max_poidMax = np.abs(tab.max() - poid_max)
    kurtosis = tab.kurtosis()
    skewness = tab.skew()
    return {'mean':mean,'std':std,'division_mean_std_poidMax':division_mean_std_poidMax,'dist_max_poidMax':dist_max_poidMax,'dist_mean_poidMax':dist_mean_poidMax,'division_mean_poidMax':division_mean_poidMax,'poid_max':poid_max,'n':len(tab),'kurtosis':kurtosis,'skewness':skewness}

def tunning_parametre(algorithm): #get the tunning parameters for meta Heuristics
    if algorithm == 'AG2':
     pm = np.random.uniform(0,0.4)
     populationBegin = np.int(np.random.uniform(4,24))
     nbIteration = np.int(np.random.uniform(0,100))
     return pm,nbIteration,populationBegin
    elif algorithm == 'RC':
      nbIteration = np.int(np.random.uniform(1000,6000))
      T = np.random.randint(10000,50000)
      return nbIteration,T

def run_algorithm(df):#run a algorithm
    return int(str(subprocess.check_output('python3 ../'+df+'/index.py', shell=True)).split('\\')[0].split("'")[1])

def run_processes(df,timeout): #run a processes, i used this method to stop the algorithm if it time execution is greater than timeout

    pool = Pool(processes=1)
    res = pool.apply_async(run_algorithm,(df,))
    try:
        return res.get(timeout=timeout)
    except:
        return None


for i in range(df_len):
    print('nous somme dans le probleme numero %d'%(i+1))
    n = generer_n()
    poid_max = np.random.randint(10,1000)
    tab,dist= generer_problem(poid_max,n)
    tab = correct_problem(tab,poid_max)
    features = get_problem_feature(tab,poid_max)
    for df in exacts+Heuristics+MetaHeuristics:
        if df in MetaHeuristics:
           if df == 'AG2':
             pm,nbIteration,populationBegin = tunning_parametre(df)
             features.update({'pm':pm,'nbIteration':nbIteration,'populationBegin':populationBegin})
             pd.Series([poid_max,tab.values.tolist(),populationBegin,pm,nbIteration],index=['C','Weights','PopulationBegin','Pm','nb_iteration']).to_csv('../'+df+'/csv/Parameters.csv')
           elif df == 'RC':
             nbIteration,T = tunning_parametre(df)
             features.update({'nbIteration':nbIteration,'T':T})
             pd.Series([poid_max,tab.values.tolist(),nbIteration,T],index=['C','Weights','nb_iteration','T']).to_csv('../'+df+'/csv/Parameters.csv')
        else:
             pd.Series([poid_max,tab.values.tolist()],index=['C','Weights']).to_csv('../'+df+'/csv/Parameters.csv')
        start_time=time()
        minBoites = run_processes(df,timeout[df])
        features.update({'exec_time':time() - start_time,'solution':minBoites})
        exec(df+'_df='+df+"_df.append(features,ignore_index=True)")

for df in exacts+Heuristics+MetaHeuristics:
    #exec('print('+df+'_df)')
    #exec(df+'_df.to_csv("csv/'+df+'.csv",index=False)')
    with open('csv/'+df+'.csv','a') as f:
      exec(df+'_df.to_csv(f,index=False,header=None)')
