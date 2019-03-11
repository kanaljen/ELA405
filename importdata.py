# New version of split.py

from numpy import sqrt, genfromtxt
import os


def loadData():
    data = dict()
    data["run"] = list()
    data["walk"] = list()

    for filename in os.listdir('data'):
        if filename.endswith(".csv"):
            csv = genfromtxt('data/'+filename, delimiter=',')
            if "run" in filename:
                data["run"].append(csv)
            elif "walk" in filename:
                data["walk"].append(csv)
    return data


def processData():
    data = loadData()
    datasets = dict()
    for key in data:
        set = []
        for table in data[key]:
            for row in table:
                y = 0
                for x in row:
                    y += x**2
                y = sqrt(y)
                set.append(y)
        datasets[key] = set
    return datasets


def splitData():
    data = processData()
    datasets = dict()
    for key in data:
        ceil = 1000
        floor = 0
        set = []
        while ceil < len(data[key]):
            set.append(data[key][floor:ceil])
            floor = ceil
            ceil += 1000
        datasets[key] = set
    return datasets


def data():
    return splitData()