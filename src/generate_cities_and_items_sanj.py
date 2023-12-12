import numpy as np

from calculate_total_time_file import calculate_total_time

def generate_cities_and_items_random(Q, number_of_cities, city_indices, item_section):
    """
  This function generates and returns a random order in which cities are to be traversed,
  along with a binary array that decides which items must be put in the knapsack.

  Parameters
  ----------
  Q : float
    the capacity of the knapsack.
  number_of_cities : int
    The number of cities in the data.
  city_indices : list[int]
    A list of all cities.
  item_section : 2D numpy array
    A reconstruction of the item section from the parsed data.

  Returns
  -------
  city_travel : 1D numpy array
    The order in which cities should be visited.
  items_select : 1D numpy array
    A numpy array that decides which items are to be picked.

  """

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


def turn_binary_to_dictionary_and_calc_cost(city_travel, item_section, items_select, D, Q, vmax, vmin, R):
    """
    Turns the binary items selection array into a dictionary which matches up items with the cities they're packed at.
    Description of the dictionary:
    A dictionary containing the list of items to be picked in each of the city and their weights present,
    and arranged in the order of cities to be visited

    cities_items_dict = {city1_index: [(item1_index, item1_wt), (item2_index, item2_wt), (item3_index, item3_wt)],
                        city2_index: [(item1_index, item1_wt), (item2_index, item2_wt)],
                        city3_index: [(item1_index, item1_wt)...and so on...]}

    Parameters
    ----------
    city_travel : 1D numpy array
        An ordered list of cities to visit.
    item_section : 2D numpy array
        A 2D matrix derived from the section of the dataset which contains the details about the items available.
    items_select : 1D numpy array
        A binary array of which items to take. Ordered the same way as it is in item_section.
    D : 2D numpy array
        Distance matrix.
    Q : float
        Maximum capacity of the knapsack.
    vmax : float
        Max velocity of the thief.
    vmin : float
        Min velocity of the thief.
    R : float
        Renting ratio.

    Returns
    -------
    total_time : float
        Time taken for the thief to travel.
    net_profit : float
        The profit after adding up item profits and subtracting rent.


    """
    # Validate the input parameters
    if vmax <= 0 or vmin <= 0 or vmax < vmin:
        raise ValueError("Invalid velocities: vmax and vmin must be positive, and vmax must be greater than vmin.")

    # turn binary item array into a dict so that time can be calculated
    cities_items_dict = {}

    for city in city_travel:
      cities_items_dict[city] = []
      for item in item_section[:,0]:
        if items_select[int(item-1)] == 1 and item_section[int(item-1), 3] == city: # checks if the item has been selected and check if the item is present in the city
          cities_items_dict[city].append((item, item_section[int(item-1), 2]))


    # calculating costs
    # first, the time
    total_time = calculate_total_time(D, Q, vmax, vmin, cities_items_dict, city_travel)

    # now the net profit
    items_profit = sum(items_select*item_section[:, 1])
    net_profit = items_profit - (total_time * R)

    return total_time, net_profit


