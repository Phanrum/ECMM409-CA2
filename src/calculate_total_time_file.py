from parsing import node_coord_section
from ttp import make_distance_matrix

def calculate_total_time(dataset, vmax, vmin, cities_items_dict):
  """
  This function calculates and returns the total time taken to travel all the cities.

  Parameters
  ----------
  dataset : parsing.Dataset
    Parsed data.
  vmax : int
    The maximum possible velocity.
  vmin : int
    The minimum possible velocity.
  cities_items_dict : dict{int: list of tuples (int, int)}
    A dictionary containing the list of items to be picked in each of the city and their weights present,
    and arranged in the order of cities to be visited.

  Returns
  -------
  time : int
    The total time taken to travel through all the cities.
  """
  D = make_distance_matrix(node_coord_section(dataset))
  Q = dataset.knapsack_capacity
  time = 0
  for city1, city2 in zip(list(cities_items_dict.keys())[:-1], list(cities_items_dict.keys())[1:]):
    weight = sum(wt for _, wt in cities_items_dict[city1])
    v = vmax-(weight/Q)*(vmax-vmin)
    time += D[city1, city2]/v
  return time
