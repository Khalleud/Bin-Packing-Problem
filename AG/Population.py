from Constants import n,C,Weights
from random import randint,random,choice
from Fitness import Allowed,Fitness
import numpy as np
from firstFit import firstFit,nextfit,maxfit,bestfit
import pandas as pd

"""def GenerateConfiguration(): #permet de generer un individus
     Configuration = []
     Bin = [C]*n
     Configuration.append(1) # le premiere objet est mis dans une boite
     Bin[0] -= Weights[0]  #jenleve le ppoid du premiere element du premier bin
     for i in range(1,n): # pour tout les autre objets
        choices = list(range(Fitness(Configuration)+1)) #je genere les numero des bins déja créer sous forme darray
        choix = choice(choices)  #je tire un bin au hasard
        j=0
        while j < (Fitness(Configuration)//2 + 1) and Bin[choix] < Weights[i]: #TQ g pas trouvé de place et que j'ai pas atteins la limite du nombre d'itération que g moi mm fixé
           choices.remove(choix) # j'enleve le choix du tableau des choix car je peux pas y mettre lobjet
           choix = choice(choices) # je prend un nouveau choix au hasard
           j+=1
        if j == (Fitness(Configuration)//2 + 1): # si j'ai atteind le nombre max d'iteration alors je met l'objet dans un nouveau bin
          Configuration.append(Fitness(Configuration)+1)
          Bin[Fitness(Configuration)-1] -= Weights[i]
        else:  # sinon je met l'objet dans le bin trouvé
          Configuration.append(choix+1)
          Bin[choix] -= Weights[i]
     return Configuration"""

def GenerateConfigurationFF():
    bins = Weights.copy()
    np.random.shuffle(bins)
    return firstFit(bins)

def GenerateConfigurationNF():
    bins = Weights.copy()
    np.random.shuffle(bins)
    return nextfit(bins)

def GenerateConfigurationBF():
    bins = Weights.copy()
    np.random.shuffle(bins)
    return bestfit(bins)

def GenerateConfigurations(nb):
    j=0
    Configurations = []
    while j<nb:
        rand = random()
        Configuration = GenerateConfigurationFF() if rand < 0.5 else GenerateConfigurationBF()
        #Configuration = GenerateConfigurationMF() if rand < 0.5 else GenerateConfigurationFF()
        #Configuration = GenerateConfigurationFF()
        if Allowed(Configuration):
            Configurations.append(Configuration)
            j+=1
    return Configurations

def Fitness2(Configuration):
  s=pd.Series(Configuration)
  w=pd.Series(Weights)
  return (w.groupby(s).sum()**2).sum()

def calculFitnessForConfigurations(Configurations):
    FitnessArray=[]
    for Configuration in Configurations:
        FitnessArray.append(Fitness2(Configuration)**2)
    return FitnessArray

def CalculCumulProbas(Fitness):
    FitnessTotal = sum(Fitness)
    Probas = np.array(Fitness)/FitnessTotal
    CumulProbas = []
    CumulProbas.append(Probas[0])
    for proba in Probas[1:]:
        CumulProbas.append(CumulProbas[-1] + proba)
    return CumulProbas

def SelectionParent(Fitness):
      SelectedParents=[]
      for i in range(len(Fitness)//2):
          CumulProbas=CalculCumulProbas(Fitness)
          Random = random()
          j=0
          while Random > CumulProbas[j]:
              j+=1
          SelectedParents.append(j)
          Fitness[j] = 0 #on met à 0 pour ne pas reselectionner le même elements
      return SelectedParents

def SelectionParent2(Fitness):
      SelectedParents=[]
      for i in range(len(Fitness)//2):
          max = 0
          for j in range(len(Fitness)):
              if Fitness[j]>max:
                  max = Fitness[j]
                  indice = j
          SelectedParents.append(indice)
          Fitness[indice] = 0 #on met à 0 pour ne pas reselectionner le même elements
      return SelectedParents

def SelectBestConfiguration(Configurations):
      minConf = Configurations[0]
      minFitness = Fitness(minConf)
      for Configuration in Configurations[1:]:
          if Fitness(Configuration) < minFitness:
              minConf=Configuration
              minFitness=Fitness(minConf)
      return minConf

def SelectBestConfiguration2(Configurations):
      minConf = Configurations[0]
      maxFitness = Fitness2(minConf)
      for Configuration in Configurations[1:]:
          if Fitness2(Configuration) > maxFitness:
              minConf=Configuration
              maxFitness=Fitness2(minConf)
      return minConf
