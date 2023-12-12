import numpy as np
import math
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def make_distance_matrix(node_coord_section):
    """
    Creates a distance matrix between cities based on the euclidean distance between them.

    Parameters
    ----------
    node_coord_section : 2D numpy array
        Array of cities and their coordinates.

    Returns
    -------
    distance_matrix : 2D np array
        A matrix of distances between all cities.

    """

    # preparing information from the dataset
    number_of_cities = len(node_coord_section)
    coords_only = node_coord_section[:,1:]

    # prepare the distance matrix
    dist_matrix = np.zeros((number_of_cities, number_of_cities), dtype=np.float64)

    for i in range(number_of_cities):
        for j in range(number_of_cities):
            if(i!=j):
                dist_matrix[i][j] = euclidean_distance(coords_only[i], coords_only[j])

    return dist_matrix

def packing_list_mutation(current_packing_list, item_section, Q):
    """
    Performs a bit flip mutation on the current packing list.

    Parameters
    ----------
    current_packing_list : list[binary]
        A binary list determining which items to pick up.
    item_section : 2D numpy array
        A reconstruction of the item section from the parsed data.
    Q : float
        Maximum capacity of the knapsack.

    Returns
    -------
    mutated_list : list[binary]
        A mutated packing list.
    """

    weight_array = item_section[:,2]
    not_a_good_list = True
    mutated_list = None  # initiate a packing list
    while not_a_good_list:




        ####### use current_packing_list to create a new mutated list
        # mutated_list = ########### this variable will contain your mutated packing list




        w = sum(weight_array * mutated_list)
        if w <= Q: not_a_good_list = False
        # the while loop keeps on generating the array z until the knapsack condition is not violated

    return mutated_list
