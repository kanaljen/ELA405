import matplotlib.pyplot as plt
from importdata import data

def plotPair(number):
    dataset = data()
    subplot = 210
    plt.figure(figsize=(5, 8), dpi=160)
    for key in dataset:
        subplot += 1
        plt.subplot(subplot)
        plt.plot(dataset[key][number])
        plt.ylim(0,27)
        plt.title('{} raw signal'.format(key))
        plt.ylabel('acceleration')
        plt.xlabel('samples')
    plt.subplots_adjust(hspace=0.53)
    plt.savefig('presentation/figures/rawplot.png')


if __name__ == '__main__':
    plotPair(2)