import statistics
from importdata import data

dataset = data()
print(statistics.mean(dataset['walk'][3]))
print(statistics.mean(dataset['run'][3]))
