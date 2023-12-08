import numpy as np
from sanj import generate_weight_profit_velocity_random

from sanj import generate_weight_profit_velocity_random

def calculate_travel_time(cities, distance_matrix, vmax, vmin, weights, profits, Q,renting_ratio):
    """
    Calculates the total travel time and net profit for a given route through cities, taking into account 
    the variation in velocity due to changes in the weight of the knapsack and the renting cost.

    Parameters:
    - cities (list of str): List of cities in the order they will be visited.
    - distance_matrix (dict): 2D dictionary with distances between each pair of cities.
    - vmax (float): Maximum velocity of the thief.
    - vmin (float): Minimum velocity of the thief.
    - weights (dict): Dictionary with weights of items in each city.
    - profits (dict): Dictionary with profits of items in each city.
    - Q (float): Maximum capacity of the knapsack.
    - renting_ratio (float): Renting cost per unit time.

    Returns:
    tuple: Total travel time and net profit for the route.
    """

    # Validate the input parameters
    if vmax <= 0 or vmin <= 0 or vmax < vmin:
        raise ValueError("Invalid velocities: vmax and vmin must be positive, and vmax must be greater than vmin.")
    if not cities or not distance_matrix:
        raise ValueError("Cities and distance matrix must not be empty.")

    # Initialize the variables for total travel time, current knapsack weight, profit, and velocity
    total_time, curr_wt_of_kns, curr_pro_of_kns, velocity = 0, 0, 0, vmin

    # Iterate through each city in the route
    for i in range(len(cities) - 1):
        # Determine the weight, profit, and velocity for the current city
        result = generate_weight_profit_velocity_random(vmax, vmin, weights[cities[i]], profits[cities[i]], curr_wt_of_kns, curr_pro_of_kns, Q)
        # If a valid combination is found, update the knapsack and velocity
        if result:
            curr_wt_of_kns, curr_pro_of_kns, velocity = result
        else:
            # If no valid combination is found, exit the loop
            break

        # Calculate the time to travel to the next city and update the total travel time
        time_to_next_city = distance_matrix[cities[i]][cities[i+1]] / velocity
        total_time += time_to_next_city

    # If the last city processed successfully, calculate the time to return to the starting city
    if result:
        time_to_start_city = distance_matrix[cities[-1]][cities[0]] / velocity
        total_time += time_to_start_city

    # The final total profit is the current profit in the knapsack
    total_profit = curr_pro_of_kns

    # Net profit calculation:
    # The thief incurs a cost for the time spent traveling through cities while collecting items. This cost is quantified by the renting ratio, 
    # which represents the rental cost of the knapsack  per unit of time. To compute the actual gain (net profit) from the journey, 
    # we subtract the total travel cost (calculated as the total travel time multiplied by the renting ratio) from the total profit accumulated 
     # from picking up items. The resulting figure is the net profit, which is the real measure of the thief's gain from the adventure after 
     # factoring in the costs.

    net_profit = total_profit - (total_time * renting_ratio)

    return total_time, net_profit
