import numpy as np
from Constants import Weights, C, T, nb_iteration
from firstfit import firstFit
from Fitness import Fitness, Allowed
from random import random
from voisin import voisin


def RC():
    Configuration = firstFit()
    e = Fitness(Configuration)
    bestFitness = max(Configuration)
    bestConf = Configuration
    T_ = T
    Configurations = []
    proba_acceptation = []
    for k in range(nb_iteration):
        voisinConfiguration = voisin(Configuration)
        en = Fitness(voisinConfiguration)
        # Configurations.append(max(voisinConfiguration))
        # if( np.exp((en-e)/T_) < 1) : proba_acceptation.append( np.exp((en-e)/T_))
        if (en > e) or random() < np.exp((en - e) / T_):
            Configuration = voisinConfiguration
            e = en
            if (max(Configuration) < bestFitness):
                bestFitness = max(Configuration)
                bestConf = Configuration
        T_ *= 0.99

    """plt.plot(range(nb_iteration),Configurations,'b')
    plt.savefig('fig/evolution.png')
    plt.close()
    plt.plot(range(len(proba_acceptation)),proba_acceptation)
    plt.xlabel('iterations')
    plt.ylabel('probabilité')
    plt.title('évolution de la probabilité d\'acceptation')
    plt.savefig('fig/acceptation.png')
    plt.close()"""
    return max(bestConf)


if __name__ == "__main__":
    print(RC())
