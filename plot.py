import numpy as np
from scipy.fftpack import fft
from scipy.signal import medfilt
import matplotlib.pyplot as plt
from split import splitData
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
    fr[0] = 0
    N = len(signal)
    t = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    fr =  2.0 / N * np.abs(fr[0:N // 2])
    ft  = np.linspace(0,1/(2 * T ), N//2 )
    return ft,fr

def afrequesy_plot(data, run_or_walk:str, subplot:tuple):
    plt.subplot(subplot[0], subplot[1],subplot[2])
    plt.grid()
    plt.title("{}".format(run_or_walk.title()))
    plt.xlim(0,4)
    plt.ylim(0,10)
    for signal in data[run_or_walk]:
        ft,fl = gen_frequesyresponse(signal)
        plt.plot(ft,fl)

def median_plot(data:list, run_or_walk:str, subplot:tuple):
    plt.subplot(subplot[0], subplot[1],subplot[2])
    plt.grid()
    plt.title("{}".format(run_or_walk.title()))
    # plt.ylim(0,10)
    plt.xlim(0,100)
    length = max([len(x) for x in data[run_or_walk]])
    d = abs(np.array(data[run_or_walk]))
    env1 = np.zeros_like(d)
    env2 = np.zeros_like(d)
    for i in np.arange(len(d)):
        env1[i] = median(d[max(i-1000,0):i+1])
        env2[i] = mean(d[max(i-1000,0):i+1])
    plt.plot(range(len(d)), env1, color = 'green')
    plt.plot(range(len(d)), env2, color = 'red')





def median(lst): return np.median(np.array(lst))
def mean(lst): return sum(lst)/len(lst)











if __name__ == '__main__':
    data = splitData()
    afrequesy_plot(data,'walk',(4,1,1))
    afrequesy_plot(data,'run',(4,1,2))
    median_plot(data, 'walk', (4,1,3))
    median_plot(data, 'run', (4,1,4))
    plt.show()