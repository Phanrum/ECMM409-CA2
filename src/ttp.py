import numpy as np
import math
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def make_distance_matrix(dataset):
    """
    Creates a distance matrix between cities based on the euclidean distance between them.

    Parameters
    ----------
    dataset : parsing.Dataset
        Parsed data for the problem

    Returns
    -------
    distance_matrix : 2D np array
        A matrix of distances between all cities.

    """

    # preparing information from the dataset
    number_of_cities = dataset.dimension
    # getting coordinates
    city_cordinates = np.zeros((number_of_cities, 2), dtype=np.float64)
    city_cordinates[:, 0] = [dataset.nodes[i].x for i in range(number_of_cities)]
    city_cordinates[:, 1] = [dataset.nodes[i].y for i in range(number_of_cities)]

    # prepare the distance matrix
    dist_matrix = np.zeros((number_of_cities, number_of_cities), dtype=np.float64)

    for i in range(number_of_cities):
        for j in range(number_of_cities):
            if(i!=j):
                dist_matrix[i][j] = euclidean_distance(city_cordinates[i], city_cordinates[j])

    return dist_matrix
    