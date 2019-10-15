from Constants import Weights,C

def nextFit():
    bin = 1
    rest = C
    Configuration=[]
    for x in Weights:
        if x >= rest:
            bin+=1
            rest = C -x
        else:
            rest -= x
        Configuration.append(bin)
    return max(Configuration)


print(nextFit())
