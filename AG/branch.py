import random
import numpy as np
from copy import copy
from collections import namedtuple


def binPacking(n,tab,Poid_Max,minBoites) :

    Node = namedtuple("Node","level conf poidRest")
    Nodes = []

    u=Node(1,[1],[Poid_Max - tab[0]]) #le premier noeud on met le premier objet
    Nodes.append(u)
    while len(Nodes) > 0:
      u=Nodes.pop()
      if u.level == n and max(u.conf) < minBoites: #si il s'agit d'un noeud feuille et que cette configuration contient moins de boites que les configurations trouvé jusqu'à à present alors je sauvegarde
        minBoites = max(u.conf)
        minConf = u.conf.copy()
      if u.level < n and max(u.conf) < minBoites: #sinon si ce n'est pas un noeud feuille et que cette configuration est suscéptible de contenir la solution optimal
         nbFils=max(u.conf)   #ce noeud en réalité va créer nbFils+1 , mais le dernier fils étant un cas particulier(car dans ce fils l'element va se mettre dans un nouveau bin) alors je traiterais ce cas en dehors de la boucle
         element=u.level      #le niveau courant represente l'index de l'element(l'objet) courant
         for j in range(nbFils):
            if tab[element] <= u.poidRest[j]:  #si il ya assez de place pour l'element dans le bin je le met et je crée un nouveau noeud
             a=u.conf.copy()
             a.append(j+1)
             if max(a)< minBoites:
              poidRest = u.poidRest.copy()
              poidRest[j]-= tab[element]
              v=Node(u.level + 1 ,a,poidRest)
              Nodes.append(v)

         if max(u.conf)+1 < minBoites:
           u.conf.append(max(u.conf)+1)
           u.poidRest.append(Poid_Max-tab[element])
           v=Node(u.level+1,u.conf,u.poidRest) # dans ce noeud je met l'element ( objet ) dans un nouveau bin d'ou le (u.conf.append(max(u.conf)+1))
           Nodes.append(v)
    print(minBoites)








































"""Node = namedtuple("Node","level conf poidRest nbBoites")
tab=[8,6,8,5,12,10,3,4,5,9,17,6,7,8,13,14,2,16]
Poid_Max=20
n=len(tab)

def binPacking(n,tab,Poid_Max) :
    Nodes=[]
    minBoites=n+1
    minConf=np.zeros((n,n))

    u=Node(0,np.zeros((n,n)),[Poid_Max]*n,0)
    Nodes.append(u)

    while len(Nodes) > 0:
      u=Nodes.pop()

      if u.level == n and u.nbBoites < minBoites:
        minBoites = u.nbBoites
        minConf = copy(u.conf)
      if u.level < n and u.nbBoites < minBoites:
         nbFils=u.nbBoites + 1
         element=u.level - 1
         for j in range(0,nbFils):
            if tab[element] <= u.poidRest[j]:
             a=copy(u.conf)
             a[element,j]=1
             poidRest=u.poidRest.copy()
             poidRest[j]-= tab[element]
             v=Node(u.level + 1 , a ,poidRest,nbBoites(poidRest,Poid_Max) )
             Nodes.append(v)
    print(minConf)
    print(minBoites)"""






#binPacking(n,tab,Poid_Max)
