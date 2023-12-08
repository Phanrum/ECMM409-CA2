from io import StringIO

import pandas as pd
import math
import numpy as np

# import our own modules
import sys
sys.path.append('../src')

# from pareto import pareto_parents
from parsing import Dataset
from ttp import make_distance_matrix
from time_function import generate_weight_profit_velocity

# read data
dataset = Dataset.new(open("../data/a280-n279.txt", 'r').read())
print(dataset.name)

# construct a distance matrix
number_of_cities = dataset.dimension
print(f"number of cities: {number_of_cities}")

coordinates = np.zeros((number_of_cities, 2))
coordinates[:,0] = [dataset.nodes[i].x for i in range(number_of_cities)]
coordinates[:,1] = [dataset.nodes[i].y for i in range(number_of_cities)]

print(coordinates)

print(type(make_distance_matrix(dataset)))

