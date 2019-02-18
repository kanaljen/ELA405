import numpy as np
import matplotlib.pyplot as plt
import sympy
import os
#import time


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

    run1z = data['run'][0][:,2]
    walk1z = data['walk'][0][:,2]

    from scipy.fftpack import fft

    # Number of sample points
    N = 100
    # sample spacing
    T = 1.0 / 800.0
    x = np.linspace(0.0, N * T, N)
    runy = run1z
    walky = walk1z
    runf = fft(runy)
    walkf = fft(walky)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    import matplotlib.pyplot as plt
    plt.subplot(1,2,1)
    plt.plot(xf, 2.0 / N * np.abs(runf[0:N // 2]))
    plt.subplot(1, 2, 2)
    plt.plot(xf, 2.0 / N * np.abs(walkf[0:N // 2]))
    plt.grid()
    plt.show()