import sys
import numpy as np
from Population import *
from Fitness import Fitness,Allowed,truncConf
from CrossOver import CrossOverPopulation
from random import randint
from Mutation import MutatePopulation
import numpy as np
from Constants import nb_iteration,PopulationBegin,Weights
from branch import binPacking
#import matplotlib.pyplot as plt


def AG():
 Population=np.array(GenerateConfigurations(PopulationBegin))
 BestConf = SelectBestConfiguration(Population)
 BestFitness = Fitness(BestConf)
 Configurations=[]
 #print([Fitness(c) for c in Population])
 for i in range(nb_iteration):
  fitness=calculFitnessForConfigurations(Population)
  index = SelectionParent(fitness)
  parents = Population[index].tolist()
  childs = CrossOverPopulation(parents)
  #print([Fitness(c) for c in childs])
  Population = parents + childs
  Population = np.array(MutatePopulation(Population)) # il faut transformé en np array pour pouvoir faire Parents = Populaiton[index]
  BestConfItration = SelectBestConfiguration2(Population)
  #Configurations.append(Fitness(BestConfItration))
  if(Fitness(BestConfItration) < BestFitness):
      BestConf = BestConfItration.copy()
      BestFitness = Fitness(BestConf)
 #plt.plot(range(nb_iteration),Configurations,'b')
 #plt.savefig('fig/evolution.png')
 return BestFitness

print(AG())
