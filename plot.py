import numpy as np
import matplotlib.pyplot as plt
import os

data = []

for filename in os.listdir('data'):
    if filename.endswith(".csv"):
        print(filename)
        csv = np.genfromtxt('data/'+filename, delimiter=',')
        data.append(csv)
        continue
    else:
        continue

for file in data:
    x = file[:,0]
    y = file[:,1]
    z = file[:,2]
    plt.plot(x)

plt.show()
