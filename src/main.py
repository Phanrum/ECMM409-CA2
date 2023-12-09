# import our own modules
#import sys
#sys.path.append('../src')

from parsing import Dataset, item_section, node_coord_section
from ttp import make_distance_matrix
from generate_cities_and_items_sanj import generate_cities_and_items_random
from time_function import calculate_travel_time
import pareto


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

# tournament selection

# crossover

# mutation


# perform nsga-ii selection and replacement
## combined_pop = children + parents
## something
## new parent population comes out


# repeat

