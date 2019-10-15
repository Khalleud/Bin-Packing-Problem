from Constants import Weights
from random import randint,choice,random
from Fitness import createBin,truncConf
from Constants import Pm
def MutatePopulation(Configurations):

     return [Mutation(Configuration) if random()<Pm else Configuration for Configuration in Configurations ]


def Mutation(Conf):
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
