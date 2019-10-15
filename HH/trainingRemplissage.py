import pandas as pd
import numpy as np

exacts = []
Heuristics = ['FF','BF','MF','NF']
MetaHeuristics = ['AG','RC']
def score(solution,time):
    time = time.apply(lambda x: 0 if x<10 else x-10)
    return solution + 0.1*time

def verifyIntegrity():
    tab = []
    for df in exacts+Heuristics+MetaHeuristics:
        exec('tab.append('+df+'_df[["n","poid_max"]].values.tolist())')
    for i in range(len(tab)-1):
        if tab[i] != tab[i+1]:
            return False
    return True


for df in exacts+Heuristics+MetaHeuristics:
    exec(df+'_df=pd.read_csv("csv/'+df+'.csv")')
    exec(df+'_df["score"]=0')
    exec(df+'_df.loc['+df+'_df["solution"].isna(),"score"]=np.inf')
    exec(df+'_df.loc['+df+'_df["score"].isna()==False,"score"]=score('+df+'_df["solution"],'+df+'_df["exec_time"])')
    exec(df+'_df["selected"]=0')
print('creation du training dataset done :D')

if verifyIntegrity():
    print('lintegrité des dataset est valide')
else:
    print('lintegrite des dataset nest pas valide')

print('creation du training dataset ...')


training = pd.DataFrame([],columns=FF_df.columns.drop(['score','solution','exec_time']))
training['target'] = []

for i in range(len(FF_df)):
    min = np.inf
    features = FF_df.iloc[i][FF_df.columns.drop(['score','solution','exec_time'])].values.tolist()
    for df in exacts+Heuristics+MetaHeuristics:
      exec('score='+df+'_df.iloc[i]["score"]')
      if score<min : min,target = score,df
    exec(target+'_df.ix[i,"selected"]=1')
    training=training.append({c:v for c,v in zip(training.columns,features+[target])},ignore_index=True)

training.to_csv('csv/training.csv',index=False)

for df in exacts+Heuristics+MetaHeuristics:
    exec(df+'_df.to_csv("csv/'+df+'.csv",index=False)')
