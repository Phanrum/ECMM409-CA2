import numpy as np

# import our own modules
#import sys
#sys.path.append('../src')

from parsing import Dataset, item_section, node_coord_section
from ttp import make_distance_matrix
from generate_cities_and_items_sanj import generate_cities_and_items_random
from time_function import calculate_travel_time
from pareto import calc_rank_and_crowding_distance, nsga_2_replacement_function


# read data
dataset = Dataset.new(open("data/a280-n279.txt", 'r').read())
print(dataset.name)

# basic info
number_of_cities = dataset.dimension
vmin = dataset.min_speed
vmax = dataset.max_speed
Q = dataset.knapsack_capacity

# sections
item_section = item_section(dataset)
node_coord_section = node_coord_section(dataset)

# construct a distance matrix
distance_matrix = make_distance_matrix(node_coord_section)

print((generate_cities_and_items_random(dataset, item_section))[0])# for i in range(pop_size)))

# generate solutions
pop_size = 100


# parents = #something


# assert len(parents) == pop_size, f"Wait, but the number of parents ({len(parents)}) is different to the population size ({pop_size})."
# now we've made a parent population

# evaluate all parents


#### here is where the main loop starts

# tournament selection

# crossover

# mutation

# evaluate all parents

# perform nsga-ii selection and replacement

# it expects a 2D numpy array of costs "R", where the first column has times and the second column has profits
R = np.zeros((2*pop_size, 2)) # initialise an array for children and parents

# Replace the following two lines with the costs of actual parents and children
R[:500] = np.random.normal(3, 2.5, size=(pop_size, 2)) # the first two columns are times and profits
R[500:] = np.random.normal(3, 2.5, size=(pop_size, 2)) # pretend these are children
# sick. now the main loop.

# assign ranks and distances
costs, fronts = calc_rank_and_crowding_distance(R, plot=True) # costs are basically R but updated
# find the solutions which should be carried over
idx = nsga_2_replacement_function(pop_size, costs, fronts)
# now make a new population and put in it the solutions which idx tells you to


# repeat until terminating condition

