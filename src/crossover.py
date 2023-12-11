import random
import numpy as np

def crossover_basic(first_parent, second_parent):
    crossover_point = random.choice(first_parent)

    child1 = np.concatenate((first_parent[:crossover_point], second_parent[crossover_point:]))
    child2 = np.concatenate((second_parent[:crossover_point], first_parent[crossover_point:]))

    return child1, child2



def fix_tsp_crossover(parent, child):
    missing_cities = []

    for index in parent:
        if index not in child:
            missing_cities.append(index)

    duplicate_cities = []

    if missing_cities != []:
        for (i, x) in enumerate(child):
            for (j, y) in enumerate(child):
                if x == y and i < j:
                    duplicate_cities.append(i)
     
    duplicates = list(zip(duplicate_cities, missing_cities))

    for (index, new_city) in duplicates:
        child[index] = new_city

    return child
    
def is_over_weight(item_weight, child, max_weight):
    
    calculated_weight: int = 0

    for (i,city) in enumerate(child):
        if city == 1:
            calculated_weight += item_weight[i]

    if calculated_weight < max_weight:
        return False
    else:
        return True



def fix_kp_crossover(items, child1, child2, max_weight, knapsack1, knapsack2):
    item_weight = [items[i].weight for i in range(len(items))]  # item weights

    while is_over_weight(item_weight, child1, max_weight) or is_over_weight(item_weight, child2, max_weight):
        child1, child2 = crossover_basic(knapsack1, knapsack2)

    return child1, child2


def crossover_tsp(path1, path2):
    """

    path1: first parent for crossover
    path2: second parent for crossover

    returns two children
    """

    child1, child2 = crossover_basic(path1, path2)


    return fix_tsp_crossover(path1, child1), fix_tsp_crossover(path1, child2)



def crossover_kp(items, knapsack1, knapsack2, max_weight):
    """
    items: an array containing the items
    kanpsack1: first parent for crossover
    knapsack2: second parent for crossover
    max_weight: capacity of knapsack

    returns two children
    """
    child1, child2 = crossover_basic(knapsack1, knapsack2)

    child1, child2 = fix_kp_crossover(items, child1, child2, max_weight, knapsack1, knapsack2)

    return child1, child2

def crossover_kp_but_make_it_indian(knapsack1, knapsack2,  item_section, Q):
    """
    Performs a crossover on two packing lists.

    Parameters
    ----------
    knapsack1, knapsack2 : list[binary]
        A binary list determining which items to pick up.
    item_section : 2D numpy array
        A reconstruction of the item section from the parsed data.
    Q : float
        Maximum capacity of the knapsack.

    Returns
    -------
    child_knapsack_1, child_knapsack_2 : list[binary]
        Crossovered (crossed-over?) packing list.
    """

    weight_array = item_section[:,2]
    not_a_good_list = True
    child_knapsack_1, child_knapsack_2 = None, None  # initiate packing lists

    while not_a_good_list:

        child_knapsack_1, child_knapsack_2 = crossover_basic(knapsack1, knapsack2)

        w1 = sum(weight_array * child_knapsack_1)
        w2 = sum(weight_array * child_knapsack_2)
        if w1 <= Q and w2 <= Q: not_a_good_list = False
        # the while loop keeps on generating packing lists until the knapsack condition is not violated

    return child_knapsack_1, child_knapsack_2