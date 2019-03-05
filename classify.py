import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import butter, lfilter
from scipy.fftpack import fft
from split import splitData
from plot import gen_frequesyresponse, afrequesy_plot

def prune_f(signal:list, cut:list):
    ret = np.array(signal)
    #ret = np.array(signal[1])
    assert(len(ret.shape) == 1)
    for x in np.arange(ret.size):
        if not (cut[0] < x and x < cut[1]):
            ret[x] = 0
    return ret

def test_signal(signal:list, cut:list):
    ''' Test a singel signal and return the probobiltity
        it is ether a running or walking signal.'''
    fsignal = gen_frequesyresponse(signal)
    psignal = prune_f(fsignal,cut)
    return max(psignal)


if __name__ == '__main__':
    cutwalking = [17,21]
    cutrunning = [24,28]
    data = splitData()
    # print(test_signal(data['run'][0], cutrunning))
    # print(test_signal(data['run'][0], cutwalking))
    # print(test_signal(data['walk'][0], cutrunning))
    # print(test_signal(data['walk'][0], cutwalking))

    for key in data.keys():
        if key == 'run':
            cut = cutrunning
            plt.subplot(2,1,1)
        else:
            cut = cutwalking
            plt.subplot(2,1,2)
        plt.xlim([15,30])
        plt.title("{} filerd".format(key))
        for signal in data[key]:
            fsignal = gen_frequesyresponse(signal)
            psignal = prune_f(fsignal['magnitude'], cut)
            plt.plot(psignal)
    plt.show()





