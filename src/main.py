import numpy as np
from tqdm import trange
import logging

# import our own modules
import sys
sys.path.append('../src')

from parsing import Dataset, item_section, node_coord_section
from ttp import make_distance_matrix
from generate_cities_and_items_sanj import generate_cities_and_items_random, turn_binary_to_dictionary_and_calc_cost
from crossover import crossover_tsp
from pareto import calc_rank_and_crowding_distance, nsga_2_replacement_function, tour_select, plot_pareto

# dev
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# read data
dataset = Dataset.new(open("../data/a280-n279.txt", 'r').read())
print(dataset.name)

# basic info from data
number_of_cities = dataset.dimension
vmin = dataset.min_speed
vmax = dataset.max_speed
Q = dataset.knapsack_capacity
R = dataset.renting_ratio
city_indices = [dataset.nodes[i].index for i in range(number_of_cities)]

# sections (from data)
item_section = item_section(dataset)
node_coord_section = node_coord_section(dataset)

# construct a distance matrix
distance_matrix = make_distance_matrix(node_coord_section)

# # test solution
city_travel, items_select = generate_cities_and_items_random(Q, number_of_cities, city_indices, item_section)

# generate solutions
N = 100 # population size

population = [generate_cities_and_items_random(Q, number_of_cities, city_indices, item_section) for i in range(N)]

logging.info(population[0])

assert len(population) == N, f"Wait, but the number of parents ({len(population)}) is different to the population size ({N})."



# evaluate all parents

fake_costs = np.zeros((N+2, 2)) # initialise an array for parents and children
fake_costs[:N] = [turn_binary_to_dictionary_and_calc_cost(c, item_section, i, distance_matrix, Q, vmax, vmin, R) for c, i in population]
# to the evaluations, append front ranks and crowding distance
fake_costs_extended, _ = calc_rank_and_crowding_distance(fake_costs[:N])#, plot=True) # costs are basically costs but updated


#### here is where the main loop starts
# assume stopping criterion is number of iterations
iterations = 20
tour_size = 10

for i in trange(iterations):

    # tournament selection

    logging.debug("tournament selection")
    logging.debug(f"We must choose solution number {tour_select(tour_size, N, fake_costs_extended)}.")
    win_tour_1, win_packing_1 = population[tour_select(tour_size, N, fake_costs_extended)]
    logging.debug(f"The second winner is solution number {tour_select(tour_size, N, fake_costs_extended)}.")
    win_tour_2, win_packing_2 = population[tour_select(tour_size, N, fake_costs_extended)]

    # crossover


    # mutation

    child_tour_1, child_tour_2 = crossover_tsp(win_tour_1, win_tour_2)
    fake_children = [
        ()
    ]


    # replace this with mutated individuals
    fake_children = [generate_cities_and_items_random(Q, number_of_cities, city_indices, item_section) for i in range(2)]
    # evaluate the children by calling
    fake_costs[N:] = [turn_binary_to_dictionary_and_calc_cost(c, item_section, i, distance_matrix, Q, vmax, vmin, R) for c, i in fake_children]

    ## perform nsga-ii selection and replacement

    # assign ranks and distances
    fake_costs_extended, fronts = calc_rank_and_crowding_distance(fake_costs)#, plot=True)
    # find the solutions which should be carried over
    idx = nsga_2_replacement_function(N, fake_costs_extended, fronts)
    # now make a new population and put in it the solutions which idx tells you to
    logging.debug("We should keep the following candidates from the combined pop:")
    logging.debug(idx)

    # i don't think it's the most brilliant idea to concat lists of solutions.
    # instead, just see if the children are among recommended survivors
    child_idx = []
    if N in idx:
        child_idx.append(0)
        idx.remove(N)
    if N+1 in idx:
        child_idx.append(1)
        idx.remove((N+1))

    # new population
    population = [population[q] for q in idx] + [fake_children[q] for q in child_idx]

    logging.debug(population)
    logging.debug(f"len of new pop: {len(population)}")
    logging.debug("Amazing! we've made a new population!")
    logging.debug("="*50)

    # evaluate it

    # fake_costs = np.zeros((N + 2, 2))  # we could wipe the costs but it might be a waste of time
    fake_costs[:N] = [turn_binary_to_dictionary_and_calc_cost(c, item_section, i, distance_matrix, Q, vmax, vmin, R) for
                      c, i in population]
    # to the evaluations, append front ranks and crowding distance
    fake_costs_extended, _ = calc_rank_and_crowding_distance(fake_costs[:N])#, plot=True)

    # repeat until terminating condition

logging.info("the costs of this final population are:")
plot_pareto(fake_costs[:-2], "NSGA-II Pareto front")
