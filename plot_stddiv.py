import numpy as np
import matplotlib.pyplot as plt
import seaborn as se
from plot import gen_frequesyresponse, movingmedian_plot, avrage_data
from split import splitData

########################################
# In this code I aim to creat an plot
# that shows the avrage frequensy
# for both signals.
########################################

def frequensy_avrage(data, run_or_walk:str):
    '''
    Generates the avrage frequensy diagram
    in: data is the data flow.
    in: run_or_walk slects the class.
    out: np.array() statictical signal.
    '''

    pass



if __name__ == '__main__':
    data = splitData()
    fig = plt.figure()
    ax = list()
    ax.append(fig.add_subplot(2,2,1))
    ax.append(fig.add_subplot(2,2,2))
    ax.append(fig.add_subplot(2,2,3))
    ax.append(fig.add_subplot(2,2,4))
    ax[0].set_title('walk distrobution plot')
    ax[1].set_title('run distrobution plot')
    ax[2].set_title('walk box plot')
    ax[3].set_title('run box plot')
    ax[0].set_xlim([0,1])
    ax[1].set_xlim([0,1])
    ax[2].set_xlim([0,1])
    ax[3].set_xlim([0,1])
    twalk = avrage_data(data, 'walk')
    trun  = avrage_data(data, 'run')
    se.boxplot(twalk['avg'], ax=ax[2])
    se.boxplot(trun['avg'], ax=ax[3])
    se.distplot(twalk['avg'], ax=ax[0])
    se.distplot(trun['avg'], ax=ax[1])
    plt.show()
