from Constants import C,Weights
import pandas as pd




def Fitness(Configuration): # renvoit le nombre de boites utilisé pour une solution
  s=pd.Series(Configuration)
  w=pd.Series(Weights)
  return (w.groupby(s).sum()**2).sum()
  
def Allowed(Configuration): # renvoit True si la solution est acceptable
    RemainingWeights = [C]*max(Configuration)
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
