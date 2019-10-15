from Constants import C,Weights

def firstFit(poids):
  bins = []
  bins.append(C)
  Configuration = []

  for j in range(len(poids)):
        i = 0
        while i < len(bins):
            if bins[i] >=poids[j]:
                bins[i] -= poids[j]
                Configuration.append(i+1)
                break
            i+=1
        if i == len(bins):
            bins.append(C-poids[j])
            Configuration.append(i+1)

  result = []
  for j in range(len(Weights)):
      result.append(Configuration[poids.index(Weights[j])])
      Configuration.pop(poids.index(Weights[j]))
      poids.remove(Weights[j])
  return result

def nextfit(poids):
        bin = 1
        rest = C
        Configuration=[]
        for x in poids:
            if x >= rest:
                bin+=1
                rest = C -x
            else:
                rest -= x
            Configuration.append(bin)
        result = []
        for j in range(len(Weights)):
           result.append(Configuration[poids.index(Weights[j])])
           Configuration.pop(poids.index(Weights[j]))
           poids.remove(Weights[j])
        return result

def maxfit(poids):
    bins = [] #il va stocker le volume restant de chaque bin
    bins.append(C)
    Configuration = []
    bin = 1

    for x in poids:
        bi = 0
        maximum = 0

        for i in range(0,bin):
            if bins[i] >= x and bins[i] > maximum:
                bi = i
                maximum = bins[i]
        if maximum == 0:
            bins.append(C - x)
            Configuration.append(len(bins))
            bin+=1
        else:
            bins[bi] = bins[bi] - x
            Configuration.append(bi+1)

    return Configuration

def bestfit(poids):

    bins = [] #il va stocker le volume restant de chaque bin
    bins.append(C)
    Configuration = []
    bin = 1

    for x in poids:
        bi = 0
        min = C + 1

        for i in range(0,bin):
            if bins[i] >= x and bins[i] - x < min:
                bi = i
                min = bins[i] - x
        if min == C +1:
            bins.append(C - x)
            Configuration.append(len(bins))
            bin+=1
        else:
            bins[bi] = bins[bi] - x
            Configuration.append(bi+1)


    return Configuration
