from io import StringIO
import pandas as pd
import numpy as np


def generate_cities_and_items_random(dataset, item_section):
    """
  This function generates and returns a random order in which cities are to be traversed,
  along with a binary array that decides which items must be put in the knapsack

  Parameters
  ----------
  dataset : parsing.Dataset
    Parsed data.
  item_section : 2D numpy array
    A reconstruction of the item section from the parsed data.

  Returns
  -------
  city_travel : np.array[int]
    The order of cities to be visited
  items_selected : np.array[int]
    A binary array which decides which items are to be picked

  """

    # reading the required qualities
    Q = dataset.knapsack_capacity
    number_of_cities = dataset.dimension
    city_indices = [dataset.nodes[i].index for i in range(number_of_cities)]

    # create a list of cities to visit
    city_travel = np.random.choice(city_indices, size=number_of_cities, replace=False)

    # stochastic - items will get selected with a probability which depends on how heavy they are
    weight_array = item_section[:,2]
    prob = Q / sum(weight_array)

    ####
    not_a_good_list = True
    items_select = None # initiate a packing list
    while not_a_good_list:
        items_select = np.random.choice([0, 1], p=[1 - prob, prob], size=len(item_section))
        w = sum(weight_array * items_select)
        if w <= Q: not_a_good_list = False
        # the while loop keeps on generating the array z until the knapsack condition is not violated
    return city_travel, items_select
