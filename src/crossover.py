import numpy as np
import random

def crossover_basic(first_parent, second_parent):
    crossover_point = random.choice(first_parent)

    child1 = first_parent[:crossover_point] + second_parent[crossover_point:]
    child2 = second_parent[:crossover_point] + first_parent[crossover_point:]

    return child1, child2


def fix_tsp_crossover(cities_indices, child):
    missing_cities = []

    for index in cities_indices:
        if index not in child:
            missing_cities.append(index)

    duplicate_cities = []

    if missing_cities != []:
        for (i, x) in enumerate(child):
            for (j, y) in enumerate(child):
                if x == y and i < j:
                    duplicate_cities.append[i]
     
    duplicates = list(zip(duplicate_cities, missing_cities))

    for (index, new_city) in duplicates:
        child[index] = new_city

    return child


def is_unique(item_cities, child, max_weight):
    child_items = []

    for item in child:
        if item_cities[int(item) -1] not in child_items:
            child_items.append(item_cities[int(item) -1])

    if len(child_items) == len(child):
        return True
    else:
        return False
    
def is_under_weight(item_weight, child, max_weight):
    bruh = 0
    #for 



def fix_kp_crossover(items, child, max_weight):

    item_index = [items[i].index for i in range(len(items))]  # item indices
    item_weight = [items[i].weight for i in range(len(items))]  # item weights
    item_cities = [items[i].node_number for i in range(len(items))]  # which city each item is in

    while is_under_weight(item_weight, child, max_weight) and not is_unique(item_cities, child):
        bruh = 0






def crossover_tsp(cities_indices, path1, path2):
    """
    cities_indices: an array containing the index of every city
    path1: first parent for crossover
    path2: second parent for crossover

    returns two children
    """

    crossover_point = random.choice(path1)

    child1, child2 = crossover_basic(path1, path2)

    return fix_tsp_crossover(cities_indices, child1), fix_tsp_crossover(cities_indices, child2)


def crossover_kp(items, knapsack1, knapsack2, max_weight):
    """
    items: an array containing the items
    kanpsack1: first parent for crossover
    knapsack2: second parent for crossover
    max_weight: capacity of knapsack

    returns two children
    """

    crossover_point = random.choice(knapsack1)
    child1, child2 = crossover_basic(knapsack1, knapsack2)

    return fix_kp_crossover(items, child1, max_weight), fix_kp_crossover(items, child2, max_weight)
