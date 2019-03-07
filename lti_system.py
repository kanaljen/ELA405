import numpy as np
import matplotlib.pyplot as plt
import seaborn as se
from scipy.signal import kaiserord, lfilter, firwin, freqz
from plot import gen_frequesyresponse, movingmedian_plot, avrage_data
from importdata import data

class fir_filter:
    """A fir filter class"""
    def __init__(self, signal:np.array, sample_rate=100, nsamples=100,ripple_db=60.0,cutoff_hz=2.0, with_rate=1.0, win='kaiser', higpas=False):
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
        self._signal = signal
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
        self._freqz = freqz(self._taps, worN=8000)
        self._h_dB = 20*np.log(np.abs(self._freqz[1]))
        self._ishigpass = higpas
        if self._ishigpass == True:
            self._taps = -self._taps
            self._taps[self._N//2] = self._taps[self._N//2] + 1
        self._filterd_x = lfilter(self._taps,1.0,signal)
        delay = 0.5 * (self._N - 1)/self._sample_rate
        self._good_t = self._t[self._N-1:]-delay,
        self._good_signal = self._filterd_x[self._N-1:]
        self._fir_axis = list()
        self._fir_axis.append([0.42,0.6, 0.45, 0.25 ])
        self._fir_axis.append([0.42,0.25,0.45,0.25])
        self._supblot_limmits = list()

    def get_statistics(self):
        median = np.median(self._good_signal)
        sigma  = np.std(self._good_signal)
        print("median={}, sigma={}".format(median,sigma))
        return median, sigma

    def plot_filterd_signals(self,title, subplot=False):
        delay = 0.5 * (self._N - 1)/self._sample_rate
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        # Plot the filterd signal
        m,s = self.get_statistics()
        #t = np.arange(len(self._good_t))
        #t = self._good_t[0]
        t = self._t
        hig_sima = t*0 + (m+s)
        low_sima = t*0 + (m-s)
        fig1=plt.fill_between(t,hig_sima,low_sima, facecolor='blue', alpha=0.2 , label='$\sigma$')
        #plt.fill_between(self._good_t,temp ,0, facecolor='green')
        fig2=plt.plot(self._t - delay, self._filterd_x, 'r-', label='Bad signal')
        # Plot the good part of the filterd signal
        fig3=plt.plot(self._t[self._N-1:]-delay, self._filterd_x[self._N-1:], 'g', linewidth=4 ,label='Good signal')
        plt.title(title)
        plt.legend(["Bad","Good", "$\sigma$"], loc=4)
        plt.xlabel('t')
        plt.ylabel('acceleration')
        plt.grid(True)
        pass

    def plot_raw_signal(self, title="", xlim=False,ylim=False,subplot=False):
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        plt.plot(self._t,self._signal)
        plt.title(title)
        plt.xlabel("time (t)")
        plt.ylabel("amplitude (g)")
        if not isinstance(xlim, bool):
            plt.xlim(xlim)
        if not isinstance(ylim, bool):
            plt.ylim(ylim)
        plt.grid(True)


    def plot_magnitude(self,subplot=False):
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        w = self._freqz[0]
        h = self._freqz[1]
        plt.plot((w/np.pi)*self._nyq_rate,np.absolute(h),linewidth=2)
        plt.xlabel('Frequecy (Hz)')
        plt.ylabel('Gain')
        plt.title('Frequncy Response')
        plt.ylim(-0.05,1.05)
        plt.xlim(-0.5,10)
        plt.grid(True)
        # Insert smal plots in to the subplot
        # First the upper palt of teh plot
        # ax1 = plt.axes(self._fir_axis[0])
        # plt.plot((w/np.pi)* self._nyq_rate, np.absolute(h), linewidth=2)
        # plt.xlim(0,0.8)
        # plt.ylim(0.9985, 1.001)
        # plt.grid(True)
        # # Then the lower part of the plot
        # ax2 = plt.axis()
        # plt.plot((w/np.pi)* self._nyq_rate, np.absolute(h), linewidth=2)
        # plt.xlim(12.0, 20.0)
        # plt.ylim(0.0,0.0025)
        # plt.grid(True)

    def plot_frequesy_response(self, subplot=False):
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        plt.plot(self._freqz[0]/np.max(self._freqz[0]), self._h_dB)
        plt.ylabel('Magnitude (db)')
        plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
        plt.title(r'Frequency response')

    def plot_impulse_response(self, subplot=False):
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        l = len(self._taps)
        impulse = np.repeat(0.,l); impulse[0] =1.
        x = np.arange(0,l)
        response = lfilter(self._taps,1,impulse)
        plt.stem(x, response)
        plt.ylabel('Amplitude')
        plt.xlabel(r'n (samples)')
        plt.title(r'Impulse response')

    def plot_phase_response(self, subplot=False):
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        h_phase = np.unwrap(np.arctan2(np.imag(self._freqz[1]), np.real(self._freqz[1])))
        plt.plot(self._freqz[0]/np.max(self._freqz[0]), h_phase)
        plt.ylabel('Phase (radians)')
        plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
        plt.title(r'Phase response')


    def plot_coefficients(self, subplot):
        if not isinstance(subplot, bool):
            plt.subplot(subplot)
        plt.plot(self._taps, 'bo-', linewidth=2)
        plt.title("Filter Coefficeents ({} taps)".format(self._N))
        plt.grid()


    def __str__(self):
        return "FirFilter type={t}, sample rate={sr}, cutoff={hz}Hz".format(
                t = self._window_type, sr=self._sample_rate, hz=self._cutoff_hz)



def plot_filter_results(data:dict, savefig='temp.png', signalnr=5, cutoff_hz=2, hp=False):
    # Layout of plot is:
    # -----------------------------------------------
    # | walk signal raw   | walk signal filterd     |
    # -----------------------------------------------
    # | Run signal raw    | walk singal filterd     |
    # -----------------------------------------------
    firWalk= fir_filter(data['walk'][signalnr], cutoff_hz=cutoff_hz, higpas=hp)
    firRun= fir_filter(data['run'][signalnr], cutoff_hz=cutoff_hz, higpas=hp)
    # firWalk.plot_coefficients(321)
    # firWalk.plot_magnitude(322)
    firWalk.plot_raw_signal(title="RAW walk signal", subplot=221)
    firWalk.plot_filterd_signals("Filterd walk", subplot=222)
    firRun.plot_raw_signal(title="RAW run signal", subplot=223)
    firRun.plot_filterd_signals(title='Filterd run', subplot=224)
    plt.subplots_adjust(hspace=0.3)
    plt.savefig("presentation/figures/{}".format(savefig))

def plot_lit_sytem(data, walk_run='walk', signalnr=4, cutoff_hz=2.0, savefig='pltot_lti.png', hp=False):
    # Layout of the plot is:
    # -----------------------------------------------
    # | Impulse response to system
    # -----------------------------------------------
    # | Step response to system
    # -----------------------------------------------
    # | Frequensy response
    # -----------------------------------------------
    # | Phase response
    # -----------------------------------------------
    fir = fir_filter(data[walk_run][signalnr], cutoff_hz=cutoff_hz, higpas=hp)
    fir.plot_impulse_response(411)
    fir.plot_magnitude(412)
    fir.plot_frequesy_response(413)
    fir.plot_phase_response(414)

    plt.savefig("presentation/figures/{}".format(savefig))



if __name__ == '__main__':
    data = data()
    # plt.rc('text', usetex=True)
    # plt.figure(c)
    # c += 1
    # plot_filter_results(data, savefig="plot_lti_lopasl.png")
    # plt.figure(c)
    # c += 1
    # plot_filter_results(data, savefig='plot_lti_higpas.png', cutoff_hz=2.5, hp=True)
    # --------- Lopass filter plot ------------
    fig=plt.figure(figsize=(8,13), tight_layout=True)
    fig.suptitle("LOW pass filter")
    plot_lit_sytem(data,walk_run='run', signalnr=4, savefig='plot_system_lopass')
    # --------- Higpass filter plot ------------
    fig=plt.figure(figsize=(8,13), tight_layout=True)
    fig.suptitle("HIGH pass filter")
    plot_lit_sytem(data,walk_run='run', signalnr=4, savefig='plot_system_lopass', cutoff_hz=2.45, hp=True)

    # for key in data.keys():
    #     if key == 'walk':
    #         subplot = 221
    #     else:
    #         subplot = 223
    #     for signal in data[key]:
    #         fir = fir_filter(signal)
    #         fir.plot_signals('signals of {}'.format(key),subplot=subplot)
    #         fir.plot_fir_coefficients(gain_subplot=subplot + 1)

    plt.show()

