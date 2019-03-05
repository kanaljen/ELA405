import numpy as np
import matplotlib.pyplot as plt
import seaborn as se
from scipy.signal import kaiserord, lfilter, firwin, freqz
from plot import gen_frequesyresponse, movingmedian_plot, avrage_data
from importdata import data

class fir_filter:
    """A fir filter class"""
    def __init__(self, signal:np.array, sample_rate=100, nsamples=100,ripple_db=60.0,cutoff_hz=2.0, with_rate=1.0, win='kaiser'):
        """
            Fir filter:
            Inputs:
                signal: is the data in an np.array.
                sample_rate: What rate was the signal reqorded at?
                ripple_db: The desierd attenuation in the stopbond, in dB.
                cutoff_hz: The cutoff frequency of the filter.
        """
        print(type(signal))
        assert(len(signal) > 1)
        self._sample_rate = sample_rate
        self._cutoff_hz = cutoff_hz
        self._ripple_db = ripple_db
        self._window_type = win
        self._nsamples=len(signal)
        self._t = np.arange(len(signal))/sample_rate
        self._nyq_rate = sample_rate/2
        self._width = with_rate/self._nyq_rate
        # Compute the Kaizer parameter for the FIR filter.
        self._N, self._beta = kaiserord(self._ripple_db,self._width)
        self._taps = firwin(self._N,cutoff_hz/self._nyq_rate, window=(win,self._beta))
        self._filterd_x = lfilter(self._taps,1.0,signal)
        self._fir_axis = list()
        self._fir_axis.append([0.42,0.6, 0.45, 0.25 ])
        self._fir_axis.append([0.42,0.25,0.45,0.25])
        self._supblot_limmits = list()

    def plot_signals(self,title, subplot=False):
        delay = 0.5 * (self._N - 1)/self._sample_rate
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        # Plot the filterd signal
        plt.plot(self._t - delay, self._filterd_x, 'r-')
        # Plot the good part of the filterd signal
        plt.plot(self._t[self._N-1:]-delay, self._filterd_x[self._N-1:], 'g', linewidth=4)
        plt.title(title)
        plt.xlabel('t')
        plt.ylabel('acceleration')
        pass

    def plot_fir_coefficients(self,gain_subplot=False):
        if not isinstance(subplot, bool):
            plt.subplot(gain_subplot)
        w, h = freqz(self._taps, worN=8000)
        plt.plot((w/np.pi)*self._nyq_rate,np.absolute(h),linewidth=2)
        plt.xlabel('Frequecy (Hz)')
        plt.ylabel('Gain')
        plt.title('Frequncy Response')
        plt.ylim(-0.05,1.05)
        plt.grid(True)
        # Insert smal plots in to the subplot
        # First the upper palt of teh plot
        ax1 = plt.axes(self._fir_axis[0])
        plt.plot((w/np.pi)* self._nyq_rate, np.absolute(h), linewidth=2)
        plt.xlim(0,0.8)
        plt.ylim(0.9985, 1.001)
        plt.grid(True)
        # Then the lower part of the plot
        ax2 = plt.axis()
        plt.plot((w/np.pi)* self._nyq_rate, np.absolute(h), linewidth=2)
        plt.xlim(12.0, 20.0)
        plt.ylim(0.0,0.0025)
        plt.grid(True)

    def __str__(self):
        return "FirFilter type={t}, sample rate={sr}, cutoff={hz}Hz".format(
                t = self._window_type, sr=self._sample_rate, hz=self._cutoff_hz)






if __name__ == '__main__':
    data = data()
    for key in data.keys():
        if key == 'walk':
            subplot = 221
        else:
            subplot = 223
        for signal in data[key]:
            fir = fir_filter(signal)
            fir.plot_signals('signals of {}'.format(key),subplot=subplot)
            fir.plot_fir_coefficients(gain_subplot=subplot + 1)

    plt.show()

