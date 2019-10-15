from Constants import C,Weights
import pandas as pd

def Fitness(Configuration): # renvoit le nombre de boites utilisé pour une solution
  return max(Configuration)

def Allowed(Configuration): # renvoit True si la solution est acceptable
    RemainingWeights = [C]*Fitness(Configuration)
    for i in range(len(Configuration)):
        if RemainingWeights[Configuration[i]-1] >= Weights[i]:
            RemainingWeights[Configuration[i]-1] -= Weights[i]
        else :
            return False
    return True

def createBin(Configuration): #crée l'ensemble des bin ac les poids suivant la configuration
    RemainingWeights = [C]*max(Configuration)
    for i in range(len(Configuration)):
        if RemainingWeights[Configuration[i]-1] >= Weights[i]:
            RemainingWeights[Configuration[i]-1] -= Weights[i]
        else :
            return False
    return RemainingWeights

def truncConf(Configuration):  #this function will trunc a conf exemple : [2,3,4] will becam [1,2,3] or [1,22,4,4] will becam [1,2,3,3]
   s = pd.Series(Configuration)
   uniques = s.unique()
   return s.map({c:v for c,v in zip(uniques,range(1,len(uniques)+1))}).values
