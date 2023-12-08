from io import StringIO

import pandas as pd
import math
import numpy as np

# import our own modules
import sys
sys.path.append('../src')

# from pareto import pareto_parents
from parsing import Dataset, item_section, node_coord_section
from ttp import make_distance_matrix
from generate_cities_and_items_sanj import generate_cities_and_items_random
from time_function import calculate_travel_time


# read data
dataset = Dataset.new(open("../data/a280-n279.txt", 'r').read())
print(dataset.name)

number_of_cities = dataset.dimension
item_section = item_section(dataset)
node_coord_section = node_coord_section(dataset)

# construct a distance matrix
distance_matrix = make_distance_matrix(node_coord_section)
print(distance_matrix[:,:4])

# generate a solution
travel_plan, packing_plan = generate_cities_and_items_random(dataset)