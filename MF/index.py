from Constants import C,Weights

def maxFit():
    bins = [] #il va stocker le volume restant de chaque bin
    bins.append(C)
    Configuration = []
    bin = 1

    for x in Weights:
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

    return max(Configuration)

print(maxFit())
