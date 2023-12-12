import random
import numpy as np

def crossover_basic(first_parent, second_parent):
    """
    This function performs a crossover on 2 selected parents.

    Parameters
    ----------
    first_parent, second_parent, knapsack2 : 1D numpy array
        Parents selected for the crossover.

    Returns
    -------
    child1, child2 : 1D numpy array
        The resultant children generated through the crossover.
    """

    crossover_point = random.choice(first_parent)

    child1 = np.concatenate((first_parent[:crossover_point], second_parent[crossover_point:]))
    child2 = np.concatenate((second_parent[:crossover_point], first_parent[crossover_point:]))

    return child1, child2



def fix_tsp_crossover(parent, child):
    """
    This function fixes the child generated while performing crossover for the city travel array.

    Parameters
    ----------
    parent : 1D numpy array
        One of the selected parent for the crossover.
    child : 1D numpy array
        Recently generated child.

    Returns
    -------
    child : 1D numpy array
        The resultant children generated after fixing the errors.
    """

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
    """
    This function checks whether the recently generated child violates the rule of knapsack or not.

    Parameters
    ----------
    item_weight : 1D numpy array
        An array containing the weights of all the items.
    child : 1D numpy array
        Recently generated child.
    max_weight : float
        Maximum capacity of the knapsack.

    Returns
    -------
    True/False : Boolean Value
        Returns whether the sum of all the selecetd items represented by the binary list
        is greater than the weight of the knapsack or not.
    """
    
    calculated_weight: int = 0

    for (i,city) in enumerate(child):
        if city == 1:
            calculated_weight += item_weight[i]

    if calculated_weight < max_weight:
        return False
    else:
        return True



def fix_kp_crossover(items, child1, child2, max_weight, knapsack1, knapsack2):
    """
    This function performs a crossover on 2 binary arrays for knapsack.

    Parameters
    ----------
    items : 1D numpy array
        An array containing the items.
    child1, child2 : 1D numpy array
        Children who were generated through the crossover.
    max_weight : float
        Maximum capacity of the knapsack.
    knapsack1, knapsack2 : 1D numpy array
        Parents selected for the crossover.

    Returns
    -------
    child1, child2 : 1D numpy array
        The resultant children generated through the crossover.
    """

    item_weight = [items[i].weight for i in range(len(items))]  # item weights

    while is_over_weight(item_weight, child1, max_weight) or is_over_weight(item_weight, child2, max_weight):
        child1, child2 = crossover_basic(knapsack1, knapsack2)

    return child1, child2


def crossover_tsp(path1, path2):
    """
    This function performs a crossover on 2 travel path lists.

    Parameters
    ----------
    path1, path2 : 1D numpy array
        Parents selected for the crossover.

    Returns
    -------
    fix_tsp_crossover(path1, child1), fix_tsp_crossover(path1, child2) : 1D numpy array
        The resultant children generated through the crossover, after fixing them.
    """

    child1, child2 = crossover_basic(path1, path2)


    return fix_tsp_crossover(path1, child1), fix_tsp_crossover(path1, child2)



def crossover_kp(items, knapsack1, knapsack2, max_weight):
    """
    This function performs a crossover on 2 binary arrays for the knapsack.

    Parameters
    ----------
    items : 1D numpy array
        An array containing the items.
    knapsack1, knapsack2 : 1D numpy array
        Parents selected for the crossover.
    max_weight : float
        Maximum capacity of the knapsack.

    Returns
    -------
    child1, child2 : 1D numpy array
        The resultant binary arrays for the knapsack generated through the crossover.
    """

    child1, child2 = crossover_basic(knapsack1, knapsack2)

    child1, child2 = fix_kp_crossover(items, child1, child2, max_weight, knapsack1, knapsack2)

    return child1, child2

def crossover_kp_but_make_it_indian(knapsack1, knapsack2,  item_section, Q):
    """
    This function performs a crossover on two packing lists.

    Parameters
    ----------
    knapsack1, knapsack2 : 1D numpy array
        A binary list determining which items to pick up.
    item_section : 2D numpy array
        A reconstruction of the item section from the parsed data.
    Q : float
        Maximum capacity of the knapsack.

    Returns
    -------
    child_knapsack_1, child_knapsack_2 : 1D numpy array
        Resulting packing list after the crossover has occuredd.
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
