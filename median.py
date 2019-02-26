import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import butter, lfilter, medfilt
from scipy.fftpack import fft
from split import splitData
from plot import gen_frequesyresponse, afrequesy_plot


data = splitData()
walk = data['walk']
run  = data['run']
wft, wfl = gen_frequesyresponse(walk)
plt.plot(wft,wfl)
plt.show()
