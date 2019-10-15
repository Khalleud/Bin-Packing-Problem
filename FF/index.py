from Constants import Weights,C

def firstFit():
  bins = []
  bins.append(C)
  Configuration = []

  for j in range(len(Weights)):
        i = 0
        while i < len(bins):
            if bins[i] >=Weights[j]:
                bins[i] -= Weights[j]
                Configuration.append(i+1)
                break
            i+=1
        if i == len(bins):
            bins.append(C-Weights[j])
            Configuration.append(i+1)

  return max(Configuration)

print(firstFit())
