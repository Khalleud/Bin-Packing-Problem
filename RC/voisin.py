from Fitness import Fitness,Allowed,createBin
from random import randint,choice,random
from Constants import Weights
import pandas as pd

def voisin1(Conf): #the voisin of a configuration consist of selecting a objet and ndiro fun bin
    Configuration=Conf.copy()
    i=randint(0,len(Configuration)-1) #je selectionne un objet au hasard
    currentBin = Configuration[i]
    RemainingWeights = createBin(Configuration)  #je créer les bins correspondants à la configuration
    RemainingWeights[Configuration[i] - 1] += Weights[i] #j'enleve l'objet choisis précedement du bin correspondant
    choices = list(range(0,len(RemainingWeights))) #je créer un array qui contient la liste de choix des bin
    choices.remove(currentBin-1)
    j=choice(choices)   # je choisis au hasard
    for k in range(len(RemainingWeights)-2):
      if RemainingWeights[j] < Weights[i]:  #TQ il n'ya pas de la place pour l'objet i dans le bin choisis au hasard j
        choices.remove(j)
        j=choice(choices)
      else:
        break
    #if k == len(RemainingWeights)-2: j=currentBin-1
    if k == len(RemainingWeights)-3 : j = currentBin-1
    Configuration[i] = j+1
    return truncConf(Configuration)


def voisin2(Conf): #swap(1,1)
        Configuration=Conf.copy()
        i=randint(0,len(Configuration)-1) #je selectionne un objet au hasard
        j=randint(0,len(Configuration)-1)
        RemainingWeights = createBin(Configuration)  #je créer les bins correspondants à la configuration
        RemainingWeights[Configuration[i] - 1] += Weights[i]
        RemainingWeights[Configuration[j] - 1] += Weights[j]
        if RemainingWeights[Configuration[i] - 1] >= Weights[j] and RemainingWeights[Configuration[j] - 1] >= Weights[i]:
            a = Configuration[i]
            Configuration[i] = Configuration[j]
            Configuration[j] = a
        return Configuration

def voisin(Conf):
    return voisin1(Conf) if random() < 0.8 else voisin2(Conf)
def truncConf(Configuration):  #this function will trunc a conf exemple : [2,3,4] will becam [1,2,3] or [1,22,4,4] will becam [1,2,3,3]
   s = pd.Series(Configuration)
   uniques = s.unique()
   return s.map({c:v for c,v in zip(uniques,range(1,len(uniques)+1))}).values
