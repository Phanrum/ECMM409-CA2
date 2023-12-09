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

# generate solutions
pop_size = 100

travel_plan, packing_plan = [generate_cities_and_items_random(dataset, item_section) for i in range(pop_size)]
parents = [[t, p] for t, p in zip(travel_plan, packing_plan)] # putting parents in one long list, where every item is a zip of each travel plan and packing plan
assert len(parents) == pop_size, f"Wait, but the number of parents ({len(parents)}) is different to the population size ({pop_size})."
# now we've made pop_size travel plans and packing plans

for parent in parents: # now sure yet whether it would be better to iterate over a big array or two lists but that can be optimised later


    print("travel plan:")
    print(parent[0])
    print("-"*20)
    print("packing plan:")
    print(parent[1])

    # evaluate a solution
    # total_time, net_profit = calculate_travel_time(travel_plan, distance_matrix)
    #TODO evaluation function is kind of still wip, relies on sanj's packing list func to be fixed
    parent_fitnesses =

# once we have a population, perform crossovers and mutations to get the same number of children as parents
#TODO crossovers and mutations - your time to shine lads

children = parents # change this to actual children
children_fitnesses =

# perform nsga-ii selection
combined_pop = children + parents
combined_fitnesses = children_fitnesses + parents_fitnesses
# get their ranks
fronts = fast_non_dominated_sort(combined_pop)
plot_fronts(combined_pop, fronts)