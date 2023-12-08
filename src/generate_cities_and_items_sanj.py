from io import StringIO
import pandas as pd
import numpy as np


def generate_cities_and_items(Q, file):
    """
  This function generates and returns a random order in which cities are to be traversed,
  along with a binary array that decides which items must be put in the knapsack

  Parameters
  ----------
  Q : int
    The total capacity of the knapsack
  file : str
    The path to the dataset file


  Returns
  -------
  city_travel : np.array[int]
    The order of cities to be visited
  items_selected : np.array[int]
    A binary array which decides which items are to be picked

  """

    # reading the file
    dataset_file = open(file, 'r').read()
    heading1 = 'NODE_COORD_SECTION	(INDEX, X, Y): '
    heading2 = 'ITEMS SECTION	(INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER): '
    pos1 = dataset_file.find(heading1) + len(heading1)
    pos2 = dataset_file.find(heading2) + len(heading2)

    # unpacking the data
    cities_dataset = pd.read_csv(StringIO(dataset_file[pos1:pos2 - len(heading2)]), sep='\t')
    cities_dataset.columns = ['INDEX', 'X', 'Y']
    items_dataset = pd.read_csv(StringIO(dataset_file[pos2:]), sep='\t')
    items_dataset.columns = ['INDEX', 'PROFIT', 'WEIGHT', 'ASSIGNED NODE NUMBER']

    city_travel = np.random.choice(cities_dataset['INDEX'], size=len(cities_dataset), replace=False)
    weight_array = np.array(items_dataset['WEIGHT'])
    prob = Q / sum(weight_array)

    ####
    not_a_good_list = True
    items_select = None # initiate a packing list
    while (not_a_good_list):
        w = 0
        items_select = np.random.choice([0, 1], p=[1 - prob, prob], size=len(items_dataset))
        w = sum(weight_array * items_select)
        if w <= Q: not_a_good_list = False
        # the while loop keeps on generating the array z until the knapsack condition is not violated
    return city_travel, items_select
