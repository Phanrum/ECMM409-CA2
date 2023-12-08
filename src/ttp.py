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
        Array of cities and their coordinates

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
    