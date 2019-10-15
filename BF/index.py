from Constants import C,Weights
def bestFit():

    bins = [] #il va stocker le volume restant de chaque bin
    bins.append(C)
    Configuration = []
    bin = 1

    for x in Weights:
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


    return max(Configuration)

print(bestFit())
