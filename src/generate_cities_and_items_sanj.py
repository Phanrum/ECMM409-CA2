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
  cities_items_dict : dict{int: list of tuples (int, int)}
    A dictionary containing the list of items to be picked in each of the city and their weights present,
    and arranged in the order of cities to be visited

    cities_items_dict = {city1_index: [(item1_index, item1_wt), (item2_index, item2_wt), (item3_index, item3_wt)],
                        city2_index: [(item1_index, item1_wt), (item2_index, item2_wt)],
                        city3_index: [(item1_index, item1_wt)...and so on...]}

  city_travel : 1D numpy array
    The order in which cities should be visited

  total_profit : int
    The final profit of the knapsack which is the addition of all the profits of each of the items

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

    not_a_good_list = True
    items_select = None # initiate a packing list
    while not_a_good_list:
        items_select = np.random.choice([0, 1], p=[1 - prob, prob], size=len(item_section))
        w = sum(weight_array * items_select)
        if w <= Q: not_a_good_list = False
        # the while loop keeps on generating the array z until the knapsack condition is not violated

    cities_items_dict = {}
    for city in city_travel:
      cities_items_dict[city] = []
      for item in item_section[:, 0]:
        if items_select[int(item-1)] == 1 and item_section[int(item-1), 3] == city:
          cities_items_dict[city].append((item, item_section[int(item-1), 2]))
    total_profit = sum(items_select*item_section[:, 1])
    return cities_items_dict, city_travel, total_profit


