import numpy as np


# Redefine the function to handle cases where the total weight exceeds the knapsack capacity
def generate_weight_profit_velocity(vmax, vmin, weights, profits, curr_wt_of_kns, curr_pro_of_kns, Q):
    """
    Generate the updated weight, profit, and velocity for the knapsack after picking items in a city.

    The function attempts to select a random combination of items. If the total weight of these items
    does not exceed the capacity of the knapsack (Q), it calculates the new velocity based on the 
    updated weight and returns the updated weight, profit, and velocity. If the total weight exceeds 
    the knapsack capacity, it will attempt to select another combination of items. This process is repeated 
    until a valid combination is found or the number of attempts exceeds a threshold (1000 attempts), 
    at which point the function returns None.

    Returning None serves several purposes:
    - It prevents the function from entering an infinite loop if it's impossible to find a valid combination
      of items that doesn't exceed the knapsack's capacity.
    - It maintains the integrity of the algorithm by ensuring that only valid item combinations are considered.
    - It signals to the calling function that it was not possible to add more items without violating the
      capacity constraint, allowing the calling function to handle this scenario appropriately (e.g., by skipping
      the city or not picking up new items).
    
    Parameters:
    - vmax (int): Maximum velocity of the thief.
    - vmin (int): Minimum velocity of the thief.
    - weights (list of int): Array of weights of the items in the current city.
    - profits (list of int): Array of profits of the items in the current city.
    - curr_wt_of_kns (int): Current weight of the knapsack.
    - curr_pro_of_kns (int): Current profit of the knapsack.
    - Q (int): Maximum capacity of the knapsack.

    Returns:
    - (tuple): Updated weight, profit, and velocity if the knapsack is not overloaded; otherwise, None.
    """
    # Initialization of the attempt count to ensure the function does not enter an infinite loop
    attempts = 0
    while True:
        # Start with the current weight and profit before picking new items
        w = curr_wt_of_kns
        p = curr_pro_of_kns
        # Randomly decide whether to pick each item or not
        z = np.random.choice([0, 1], size=len(weights))
        # Calculate the new weight and profit based on the items picked
        for pos in range(len(weights)):
            w += (weights[pos] * z[pos])  # Add the weight of picked items
            p += (profits[pos] * z[pos])  # Add the profit of picked items
        # Check if the total weight is within the knapsack's capacity
        if w <= Q:
            v = vmax - (w / Q * (vmax - vmin))  # Calculate the velocity based on the weight
            return w, p, v
        # Increment the attempt count and if it exceeds a threshold, return None to indicate failure
        attempts += 1
        if attempts > 1000:
            # After 1000 attempts, if no valid selection is found, return None to avoid infinite loop and indicate failure
            return None


def calculate_travel_time(cities, distance_matrix, vmax, vmin, weights, profits, Q):
    """
    Calculate the total travel time and profit for a given route of cities.

    Parameters:
    - cities (list of int): List of city indices to visit in order.
    - distance_matrix (2D list of int): Matrix of distances between cities.
    - vmax (int): Maximum velocity of the thief.
    - vmin (int): Minimum velocity of the thief.
    - weights (list of lists of int): List of arrays containing weights of items in each city.
    - profits (list of lists of int): List of arrays containing profits of items in each city.
    - Q (int): Maximum capacity of the knapsack.

    Returns:
    - (tuple): Total travel time and total profit for the route.
    """
    
    # Initialize total travel time and profit variables
    total_time = 0
    total_profit = 0
    
    # Initialize the current state of the knapsack
    curr_wt_of_kns = 0
    curr_pro_of_kns = 0
    
    # Begin with the minimum velocity
    velocity = vmin

    # Loop through each city in the route
    for i in range(len(cities) - 1):
        # Calculate the updated knapsack state after visiting the current city
        result = generate_weight_profit_velocity(vmax, vmin, weights[cities[i]], profits[cities[i]], curr_wt_of_kns, curr_pro_of_kns, Q)
        
        # Update the current state if the knapsack is not overloaded
        if result:
            curr_wt_of_kns, curr_pro_of_kns, velocity = result
        # If knapsack is overloaded, continue without updating
        
        # Calculate the time to travel to the next city based on the current velocity
        time_to_next_city = distance_matrix[cities[i]][cities[i+1]] / velocity
        total_time += time_to_next_city
        total_profit += curr_pro_of_kns  # Assuming profit is cumulative
        
    # Calculate the time to return to the starting city and update the total time
    time_to_start_city = distance_matrix[cities[-1]][cities[0]] / velocity
    total_time += time_to_start_city

    return total_time, total_profit

