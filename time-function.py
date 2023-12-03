import numpy as np


# The function is designed to compute the total travel time for the traveling thief problem.
def calculate_time(distances, weights, profits, knapsack_capacity, vmax, vmin, tour):
    """
    Calculate the total travel time of the thief based on the provided formula.
    """
    
    # Initialize the total travel time to zero. This variable will accumulate the travel time over the entire tour.
    total_time = 0
    
    # Initialize the current weight and profit of the knapsack to zero.
    # These will be updated as the thief picks items from each city.
    curr_wt_of_kns = 0  # Current weight of the knapsack.
    curr_pro_of_kns = 0  # Current profit of the knapsack.

    # Iterate over the tour. The range function generates a sequence from 0 to the length of the tour minus one.
    # This is because the last travel leg will be handled separately to close the loop of the tour.
    for i in range(len(tour) - 1):
        # Call 'generate_weight_profit_velocity' to determine which items to pick from the current city,
        # and update the knapsack's weight, profit, and the thief's velocity accordingly.
        curr_wt_of_kns, curr_pro_of_kns, velocity = generate_weight_profit_velocity(
            vmax, vmin, weights[tour[i]], profits[tour[i]], curr_wt_of_kns, curr_pro_of_kns, knapsack_capacity)
        
        # Calculate the time to travel from the current city to the next city in the tour.
        # This is done by dividing the distance between the two cities by the thief's current velocity.
        # distances[tour[i]][tour[i+1]] gets the distance from the distance matrix for the current leg of the journey.
        time = distances[tour[i]][tour[i+1]] / velocity
        
        # Add the calculated time for the current leg to the total travel time.
        total_time += time

    # After the loop, handle the travel from the last city back to the starting city.
    # This requires one more update to the knapsack's weight, profit, and velocity.
    curr_wt_of_kns, curr_pro_of_kns, velocity = generate_weight_profit_velocity(
        vmax, vmin, weights[tour[-1]], profits[tour[-1]], curr_wt_of_kns, curr_pro_of_kns, knapsack_capacity)
    
    # Add the travel time for the final leg of the journey, from the last city back to the first.
    # This is done by dividing the distance between the last and first cities by the velocity.
    total_time += distances[tour[-1]][tour[0]] / velocity
    
    # The function returns the total travel time after calculating the time for each leg of the journey.
    return total_time

