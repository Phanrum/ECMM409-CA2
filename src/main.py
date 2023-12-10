import numpy as np
from tqdm import trange

# import our own modules
import sys
sys.path.append('../src')

from parsing import Dataset, item_section, node_coord_section
from ttp import make_distance_matrix
from generate_cities_and_items_sanj import generate_cities_and_items_random
from calculate_total_time_file import calculate_total_time
from pareto import calc_rank_and_crowding_distance, nsga_2_replacement_function, tour_select, plot_pareto


# read data
dataset = Dataset.new(open("../data/a280-n279.txt", 'r').read())
print(dataset.name)

# basic info from data
number_of_cities = dataset.dimension
vmin = dataset.min_speed
vmax = dataset.max_speed
Q = dataset.knapsack_capacity

# sections (from data)
item_section = item_section(dataset)
node_coord_section = node_coord_section(dataset)

# construct a distance matrix
distance_matrix = make_distance_matrix(node_coord_section)

# # test solution
# cities_items_dict, total_profit = generate_cities_and_items_random(dataset, item_section)
# print(calculate_total_time(distance_matrix, Q, vmax, vmin, cities_items_dict))

# generate solutions
N = 100 # population size
population = [generate_cities_and_items_random(dataset, item_section) for i in range(N)]

assert len(population) == N, f"Wait, but the number of parents ({len(population)}) is different to the population size ({N})."



# evaluate all parents

fake_costs = np.zeros((N+2, 2)) # initialise an array for parents and children

fake_costs[:N] = np.random.normal(3, 2.5, size=(N, 2)) # replace with actual costs of parents. First column is meant to be time, second is meant to be profits.
# to the evaluations, append front ranks and crowding distance
fake_costs_extended, _ = calc_rank_and_crowding_distance(fake_costs[:N])#, plot=True) # costs are basically costs but updated

#### here is where the main loop starts
# assume stopping criterion is number of iterations
iterations = 50
tour_size = 10

for i in trange(iterations):

    # tournament selection

    print("tournament selection")
    print(f"We must choose solution number {tour_select(tour_size, N, fake_costs_extended)}.")
    winner1 = population[tour_select(tour_size, N, fake_costs_extended)]
    print(f"The second winner is solution number {tour_select(tour_size, N, fake_costs_extended)}.")
    winner2 = population[tour_select(tour_size, N, fake_costs_extended)]

    # crossover

    # mutation

    fake_children = [generate_cities_and_items_random(dataset, item_section) for i in range(2)]
    # evaluate the children
    fake_costs[N:] = np.random.normal(3, 2.5, size=(2, 2)) # replace with actual costs of the children

    ## perform nsga-ii selection and replacement

    # assign ranks and distances
    costs, fronts = calc_rank_and_crowding_distance(fake_costs)#, plot=True) # costs are basically R but updated
    # find the solutions which should be carried over
    idx = nsga_2_replacement_function(N, costs, fronts)
    # now make a new population and put in it the solutions which idx tells you to
    print("We should keep the following candidates from the combined pop:")
    print(idx)

    # i don't think it's the most brilliant idea to concat lists of solutions.
    # instead, i'll see what the largest 2 numbers are and if they are larger than N, they are the children.
    # print(heapq.nlargest(2, idx))
    # or just see if the children are in there
    child_idx = []
    if 100 in idx:
        child_idx.append(0)
        idx.remove(100)
    if 101 in idx:
        child_idx.append(1)
        idx.remove(101)

    # new population
    population = [population[q] for q in idx] + [fake_children[q] for q in child_idx]

    print(population)
    print(f"len of new pop: {len(population)}")
    print("Amazing! we've made a new population!")
    print("="*50)

    # evaluate it

    fake_costs = np.zeros((N + 2, 2))  # initialise an array for parents and children

    fake_costs[:N] = np.random.normal(3, 2.5, size=(N, 2))  # replace with actual costs of parents. First column is meant to be time, second is meant to be profits.
    # to the evaluations, append front ranks and crowding distance
    fake_costs_extended, _ = calc_rank_and_crowding_distance(fake_costs[:N])  # , plot=True) # costs are basically costs but updated

    # repeat until terminating condition

print("the costs of this final population are:")
plot_pareto(fake_costs[:-2], "NSGA-II Pareto front")
