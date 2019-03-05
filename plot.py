import numpy as np
from scipy.fftpack import fft
from scipy.signal import medfilt
import matplotlib.pyplot as plt
from split import splitData
from matplotlib import rc
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
    fsignal = fft(signal)
    fsignal[0] = 0
    N = len(signal)
    fsignal =  2.0 / N * np.abs(fsignal[0:N // 2])
    frequency = np.linspace(0,1/(2 * T ), N//2 )
    return {'frequency':frequency,'magnitude':fsignal}

def afrequesy_plot(data, run_or_walk:str, subplot:tuple):
    plt.subplot(subplot[0], subplot[1],subplot[2])
    plt.grid()
    plt.title("{}".format(run_or_walk.title()))
    plt.xlabel(r'\textbf{frequency} ($\omega$)')
    plt.ylabel(r'($|S(J\omega )|$)')
    plt.xlim(0,4)
    plt.ylim(0,10)
    for signal in data[run_or_walk]:
        x = gen_frequesyresponse(signal)
        plt.plot(x['frequency'], x['magnitude'])


def avrage_data(data, run_or_walk:str):
    temp = list()
    w_axis = list()
    for signal in data[run_or_walk]:
        x = signal
        xa = gen_frequesyresponse(x)
        w_axis = xa
        temp.append(xa['magnitude'])
    length = max([len(x) for x in temp])
    #print("max legth is: {}".format(legth))
    moving_avg = np.zeros(length)
    min_sigma = np.zeros(length)
    max_sigma = np.zeros(length)
    for w in np.arange(length):
        tot = 0
        c = 0
        sigma = 0
        for sig in temp:
            tot += sig[w]
            c += 1
        moving_avg[w] = tot/c
        for sig in temp:
            sigma += (sig[w]- moving_avg[w])**2
        sigma = np.sqrt((1/c)*sigma)
        min_sigma[w] = moving_avg[w] - sigma
        max_sigma[w] = moving_avg[w] + sigma

    moving_avg = np.array(moving_avg).transpose()
    #return (xa, moving_avg, min_sigma, max_sigma)
    return {'frequency':xa, 'avg':moving_avg, 'min sigma':min_sigma, 'max sigma':max_sigma}

def movingmedian_plot(data, run_or_walk:str, subplot:tuple):
    plt.subplot(subplot[0], subplot[1],subplot[2])
    plt.grid()
    plt.title("{} avrage".format(run_or_walk.title()))
    plt.xlabel(r'\textbf{frequency} ($\omega$)')
    plt.ylabel(r'($|S(J\omega )|$)')
    plt.xlim(0,4)
    plt.ylim(0,10)
    outtemp = avrage_data(data,run_or_walk)
    xa, moving_avg, min_sigma, max_sigma = outtemp['frequency'], outtemp['avg'], outtemp['min sigma'], outtemp['max sigma']
    plt.fill_between(xa['frequency'],min_sigma,max_sigma,alpha=0.4)
    plt.plot(xa['frequency'],moving_avg,'r')



    #plt.plot(x['frequency'], x['magnitude'])


def median(lst): return np.median(np.array(lst))
def mean(lst): return sum(lst)/len(lst)



if __name__ == '__main__':
    data = splitData()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    fig = plt.figure(figsize=(8,13), tight_layout=True)
    # ax = list()
    # ax.append()
    afrequesy_plot(data,'walk',(4,1,1))
    afrequesy_plot(data,'run',(4,1,2))
    movingmedian_plot(data,'walk',(4,1,3))
    movingmedian_plot(data,'run',(4,1,4))
    plt.subplots_adjust(hspace=0.53)
    plt.savefig('presentation/figures/plot.png')
    #plt.show()