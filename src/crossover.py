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

    child1, child2 = fix_kp_crossover(child1, child2, knapsack1, knapsack2)

    return child1, child2
