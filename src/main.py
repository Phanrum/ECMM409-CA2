# import our own modules
import sys
sys.path.append('../src')

from parsing import Dataset, item_section, node_coord_section
from ttp import make_distance_matrix
from generate_cities_and_items_sanj import generate_cities_and_items_random
from time_function import calculate_travel_time


# read data
dataset = Dataset.new(open("../data/a280-n279.txt", 'r').read())
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

# generate a solution
travel_plan, packing_plan = generate_cities_and_items_random(dataset, item_section)

print("travel plan:")
print(travel_plan)
print("-"*20)
print("packing plan:")
print(packing_plan)

# evaluate a solution
# total_time, net_profit = calculate_travel_time(travel_plan, distance_matrix)
#TODO evaluation function is kind of still wip, relies on sanj's packing list func to be fixed