from random import randint
from Fitness import createBin,Allowed,truncConf
from Constants import Weights,C
from Population import SelectBestConfiguration2

def CrossOverPopulation(Configurations):
    Childs = []
    ConfigurationsCopy = Configurations.copy()
    for i in range(len(ConfigurationsCopy)//2):
      Parent1 = SelectBestConfiguration2(ConfigurationsCopy)
      ConfigurationsCopy.remove(Parent1)
      Parent2 = SelectBestConfiguration2(ConfigurationsCopy)
      ConfigurationsCopy.remove(Parent2)
      """Parent1 = ConfigurationsCopy[randint(0,len(ConfigurationsCopy)-1)]
      ConfigurationsCopy.remove(Parent1)
      Parent2 = ConfigurationsCopy[randint(0,len(ConfigurationsCopy)-1)]
      ConfigurationsCopy.remove(Parent2)"""

      (child1,child2) = CrossOver(Parent1,Parent2)
      Childs.append(child1)
      Childs.append(child2)
    return Childs



def CrossOver(parent1,parent2):
    limiter = len(parent1)//2
    parent1 = truncConf(parent1)
    parent2 = truncConf(parent2)
    chrom11=parent1[:limiter]
    chrom12=parent1[limiter:]
    chrom21=parent2[:limiter]
    chrom22=parent2[limiter:]
    child1=fusion2(chrom11,chrom22,limiter)
    child2=fusion(chrom21,chrom12,limiter)
    return (child1,child2)

def fusion(chrom1,chrom2,limiter):
    chrom1= chrom1.tolist()
    chrom2= chrom2.tolist()
    child=[0]*(len(chrom1)+len(chrom2))  #initalisé l'enfant ac des 0 partout pour l'instant
    RemainingWeights= [C]*(len(chrom1)+len(chrom2))
    for i in range(len(chrom1)): #recopier le premier chromosome dans l'enfant
        child[i]=chrom1[i]
        RemainingWeights[chrom1[i]-1] -= Weights[i]
    for i in range(len(chrom2)): # mettre les objets du chromosome2 qu'on peut insérer dans les bin créer avec les objet du chromosome 1
                            #suivant les bin du chromosome2
        if chrom2[i] <= len(RemainingWeights) and Weights[i+limiter] <= RemainingWeights[chrom2[i] - 1]:
            child[i+limiter]=chrom2[i]
            RemainingWeights[chrom2[i] - 1] -= Weights[i+limiter]
            chrom2[i]=None  #on ne supprime pas l'objet car sinon le array chrom2 va diminuer de sa taille et les position des objets vont devenir fausse

        elif chrom2[i] > len(RemainingWeights):
            child[i+limiter] = chrom2[i]
            RemainingWeights[chrom2[i] - 1] -= Weights[i+limiter]
            chrom2[i] = None
    for i in range(len(chrom2)): #les objet du chromosomes2 qu'on a pas pu insérer dans leur place dans les bin créer par le chromosome1 vont être insérer séquentiellement lorsuqi'l y'a de la place
        if(chrom2[i] != None): #si l'objet na pas été pris précedement
            j=0
            while j<len(RemainingWeights) and Weights[i+limiter] > RemainingWeights[j] : #dés qu'il ya de la place dans un bin je le met
                j+=1
            if j < len(RemainingWeights): # si j'ai trouvé de la place je le met
                child[i+limiter] = j+1
                RemainingWeights[j]-= Weights[i+limiter]
            else: # sinon je dois créer un nouveau bin et l'insérer
                child[i+limiter] = j+1
                RemainingWeights[j]-= Weights[i+limiter]
    return truncConf(child)


def fusion2(chrom1,chrom2,limiter):
    chrom1,chrom2 = chrom1.tolist(),chrom2.tolist()
    child=[0]*(len(chrom1)+len(chrom2))  #initalisé l'enfant ac des 0 partout pour l'instant
    RemainingWeights= [C]*(len(chrom1)+len(chrom2))
    for i in range(len(chrom1)):
        if Weights[i] <= RemainingWeights[chrom1[i] - 1]:
            child[i] = chrom1[i]
            RemainingWeights[chrom1[i]-1]-= Weights[i]
        else:
            child[i]=None

        if  Weights[i+limiter] <= RemainingWeights[chrom2[i] - 1]:
            child[i+limiter] = chrom2[i]
            RemainingWeights[chrom2[i]-1]-= Weights[i+limiter]
        else:
            child[i+limiter]=None

    if (len(chrom1)+len(chrom2))%2==1:
          if  Weights[-1] <= RemainingWeights[chrom2[-1] - 1]:
            child[-1] = chrom2[-1]
            RemainingWeights[chrom2[-1] - 1]-= Weights[-1]
          else:
            child[-1]=None

    maxi = 0
    for h in range(len(child)):
        if child[h] != None and child[h]>maxi:maxi = child[h]

    for j in range(len(chrom1)+len(chrom2)):
        if child[j] == None:
            for k in range(maxi):
                if Weights[j] <= RemainingWeights[k]:
                    child[j] = k+1
                    RemainingWeights[k]-= Weights[j]
                    break
            if k ==  maxi-1:
                child[j] = maxi+1
                RemainingWeights[k+1]-= Weights[j]
                maxi+=1
    return child
