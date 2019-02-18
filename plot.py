import numpy as np
import matplotlib.pyplot as plt
import sympy
import os
import time


def loadData():
    data = dict()
    data["run"] = list()
    data["walk"] = list()

    for filename in os.listdir('data'):
        if filename.endswith(".csv"):
            csv = np.genfromtxt('data/'+filename, delimiter=',')
            if "run" in filename:
                data["run"].append(csv)
            elif "walk" in filename:
                data["walk"].append(csv)
    return data

def plotData(data, savepng=""):
    """ Plots the signals from the data fead"""
    # walk0 walk1 walk2
    # run0  run1  run2
    count = 1
    for sig in data["walk"]:
        print(sig)
        plt.subplot(2,3,count)
        plt.ylim([-20,30])
        plt.title("Walk {}".format(count - 1))
        plt.plot(sig)
        count += 1
    temp = count
    for sig in data["run"]:
        plt.subplot(2,3,count)
        plt.ylim([-20,30])
        plt.title("Run {}".format(count - temp))
        plt.plot(sig)
        count += 1
    plt.savefig(savepng, dpi=300, frameon=True, pad_inches=1)
    plt.show()




if __name__ == '__main__':
    data = loadData()
    print("Show run")
    print(data["run"])
    print("Show walk")
    print(data["walk"])
    plotData(data, savepng="walk_and_run.png")

# Showing the signal.
# walk0 walk1 walk2
# run0  run1  run2

# plt.subplot(211)
# for file in data:
#     x = file[:,0]
#     y = file[:,1]
#     z = file[:,2]
#     plt.plot(x + y + z)
# plt.subplot(212)


# plt.show()
