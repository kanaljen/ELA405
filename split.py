import numpy as np
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


def splitData():
    data = loadData()
    split = []
    for key in data:
        for table in data[key]:
            floor = 0
            ceil = 1000
            while ceil < len(table):
                split.append(table[floor:ceil,2])
                floor = ceil
                ceil += 1000
    dataset = dict()
    dataset['run'] = split[0:8]
    dataset['walk'] = split[9:len(dataset)]
    return dataset
