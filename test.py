from split import splitData
import numpy as np
from plot import *

def prune_f(signal:list, cut:list):
    ret = np.array(signal[1])
    print(ret.shape)
    assert(len(ret.shape) == 1)
    for x in  np.arange(ret.size):
        if not (cut[0] < x and x < cut[1]):
            ret[x] = 0
    return ret





if __name__ == '__main__':
    data = splitData()
    running = data['run']
    walking = data['walk']
    fwalking = gen_frequesyresponse(walking[0])
    frunning = gen_frequesyresponse(running[0])
    cutwalking = [17,21]
    cutrunning = [24,28]
    pruned_walking = prune_f(fwalking, cutwalking)
    pruned_running = prune_f(frunning, cutrunning)
    data_walking = max(pruned_walking)
    data_running = max(pruned_running)
    total = data_running + data_walking
    pwalking = data_walking/total
    prunning = data_running/total
    print("P(walking)={w}, P(running)={r}".format(w=pwalking, r=prunning))




