import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import os


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

def gen_frequesyresponse(signal):
    """ Generates the frequensy response of the signal
        in: signal 1d vector
        out: tf a vector for the carry vector.
        out: fr is the response.
    """
    T = 1/100 # Hz is our sampling speed.
    fr = fft(signal)
    N = len(signal)
    t = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    fr =  2.0 / N * np.abs(fr[0:N // 2])
    ft  = np.linspace(0,1/(2 * T ), N//2 )
    return ft,fr



if __name__ == '__main__':
    data = loadData()

    run1z = data['run'][0][:,2]
    walk1z = data['walk'][0][:,2]

    nrof_runs = len(data['run'])
    nrof_walks = len(data['walk'])
    rows = max(nrof_runs, nrof_walks)
    print("runs={r}, walks={w}".format(r=nrof_runs, w=nrof_walks))
    count = 1
    #plt.subplot(1,rows,1)
    for signal in data['run']:
        plt.subplot(2,rows,count)
        plt.xlim(0,10)
        plt.grid()
        plt.title("Runnig {}".format(count))
        ft, fr = gen_frequesyresponse(signal[:,2])
        plt.plot(ft, fr)
        count += 1


    for signal in data['walk']:
        plt.subplot(2,rows,count)
        plt.xlim(0,10)
        plt.grid()
        plt.title("Walking {}".format(-1*(rows-count)))
        ft, fr = gen_frequesyresponse(signal[:,2])
        plt.plot(ft, fr)
        count += 1

    plt.show()