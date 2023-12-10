from parsing import node_coord_section
from ttp import make_distance_matrix

def calculate_total_time(D, Q, vmax, vmin, cities_items_dict):
  """
  This function calculates and returns the total time taken to travel all the cities.

  Parameters
  ----------
  D : 2D matrix
    Distance matrix for distances between all cities.
  Q : float
    Knapsack capacity.
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

  city_list = list(cities_items_dict.keys())
  time, weight, v = 0, 0, 0
  for city1, city2 in zip(city_list[:-1], city_list[1:]):
    weight = sum(wt for _, wt in cities_items_dict[city1])
    v = vmax-(weight/Q)*(vmax-vmin)
    time += (D[city1, city2]/v)
  weight = sum(wt for _, wt in cities_items_dict[city_list[-1]])
  v = vmax-(weight/Q)*(vmax-vmin)
  time += (D[city_list[-1], city_list[0]]/v)
  return time
