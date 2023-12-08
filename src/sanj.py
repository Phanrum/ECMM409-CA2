import numpy as np

def generate_weight_profit_velocity_random(vmax, vmin, weights, profit, curr_wt_of_kns, curr_pro_of_kns, Q):
  """
  This function randomly selects the items to be picked for the knapsack
  and returns the final weight after the items are added

  param:
  1. vmax: int
  Accepts the maximum possible velocity value
  2. vmin: int
  Accepts the minimum possible velocity value
  3. weights: int array
  Contains the weight of each of the items present in the city
  4. profit: int array
  Contains the profit of each of the items present in the city
  5. curr_wt_of_kns: int
  Accepts the current weight of the knapsack before adding any items
  6. curr_pro_of_kns: int
  Accepts the current profit of the knapsack before adding any items
  7. Q: int
  Accepts the total capacity of the knapsack

  return:
  1. w: int
  Returns the updated weight of the knapsack after adding the items
  2. p: int
  Returns the updated profit of the knapsack after adding the items
  3. v: int
  Returns the updated velocity of the knapsack after adding the items
  """
  w, p = 0, 0
  not_a_good_list = True
  while(not_a_good_list):
    w = curr_wt_of_kns
    p = curr_pro_of_kns
    z = np.random.choice([0, 1], size=len(weights))
    for pos in range(len(weights)):
      w+=(weights[pos]*z[pos])
      p+=(profit[pos]*z[pos])
    if w <= Q: not_a_good_list = False
    # the while loop keeps on generating the array z until the knapsack condition is not violated
  v = vmax-(w/Q*(vmax-vmin))
  return w, p, v