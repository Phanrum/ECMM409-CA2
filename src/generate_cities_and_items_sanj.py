import numpy as np

from calculate_total_time_file import calculate_total_time

def generate_cities_and_items_random(dataset, item_section, D, vmax, vmin, R):
    """
  This function generates and returns a random order in which cities are to be traversed,
  along with a binary array that decides which items must be put in the knapsack.

  Parameters
  ----------
  dataset : parsing.Dataset
    Parsed data.
  item_section : 2D numpy array
    A reconstruction of the item section from the parsed data.
  D : 2D numpy array
    Distance matrix calculated by make_distance_matrix().
  vmax, vmin : floats
    Max and min velocities of the thief.
  R : float
    Renting ratio.

  Returns
  -------
  city_travel : 1D numpy array
    The order in which cities should be visited.
  items_select : 1D numpy array
    A numpy array that decides which items are to be picked.

  """
    # Validate the input parameters
    if vmax <= 0 or vmin <= 0 or vmax < vmin:
        raise ValueError("Invalid velocities: vmax and vmin must be positive, and vmax must be greater than vmin.")

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

    return city_travel, items_select

def get_packing_list_and_profit_time(dataset, item_section, D, vmax, vmin, R):
    """
  This function generates and returns a dictionary containing the cities and items present there,
  along with the net profit obtained and the total time taken to traverse all the cities.

  Parameters
  ----------
  dataset : parsing.Dataset
    Parsed data.
  item_section : 2D numpy array
    A reconstruction of the item section from the parsed data.
  D : 2D numpy array
    Distance matrix calculated by make_distance_matrix().
  vmax, vmin : floats
    Max and min velocities of the thief.
  R : float
    Renting ratio.

  Returns
  -------
  cities_items_dict : dict{int: list of tuples (int, int)}
    A dictionary containing the list of items to be picked in each of the city and their weights present,
    and arranged in the order of cities to be visited

    cities_items_dict = {city1_index: [(item1_index, item1_wt), (item2_index, item2_wt), (item3_index, item3_wt)],
                        city2_index: [(item1_index, item1_wt), (item2_index, item2_wt)],
                        city3_index: [(item1_index, item1_wt)...and so on...]}

  net_profit : float
    The final profit of the knapsack which is the addition of all the profits of each of the items minus the rent.
  total_time : float
    The total time to travel.

  """

    city_travel, items_select = generate_cities_and_items_random(dataset, item_section, D, vmax, vmin, R)
    cities_items_dict = {}
    Q = dataset.knapsack_capacity
    for city in city_travel:
      cities_items_dict[city] = []
      for item in item_section[:, 0]:
        if items_select[int(item-1)] == 1 and item_section[int(item-1), 3] == city:
          cities_items_dict[city].append((item, item_section[int(item-1), 2]))

    total_profit = sum(items_select*item_section[:, 1])

    # calculating costs
    # first, the time
    total_time = calculate_total_time(D, Q, vmax, vmin, cities_items_dict, city_travel)

    # now the net profit
    net_profit = total_profit - (total_time * R)

    return cities_items_dict, net_profit, total_time
