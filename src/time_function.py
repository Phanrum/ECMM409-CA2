import numpy as np

def generate_weight_profit_velocity(vmax, vmin, weights, profits, curr_wt_of_kns, curr_pro_of_kns, Q):
    # Attempt to find a valid combination of items
    attempts, max_attempts = 0, 1000
    while attempts < max_attempts:
        w, p = curr_wt_of_kns, curr_pro_of_kns
        z = np.random.choice([0, 1], size=len(weights))

        for pos in range(len(weights)):
            if w + weights[pos] * z[pos] <= Q:
                w += weights[pos] * z[pos]
                p += profits[pos] * z[pos]

        if w <= Q:
            v = vmax - (w / Q * (vmax - vmin))
            return w, p, v

        attempts += 1
    return None  # Return None if no valid combination is found

def calculate_travel_time(cities, distance_matrix, vmax, vmin, weights, profits, Q):
    if vmax <= 0 or vmin <= 0 or vmax < vmin:
        raise ValueError("Invalid velocities: vmax and vmin must be positive, and vmax must be greater than vmin.")
    if not cities or not distance_matrix:
        raise ValueError("Cities and distance matrix must not be empty.")

    total_time, curr_wt_of_kns, curr_pro_of_kns, velocity = 0, 0, 0, vmin

    for i in range(len(cities) - 1):
        result = generate_weight_profit_velocity(vmax, vmin, weights[cities[i]], profits[cities[i]], curr_wt_of_kns, curr_pro_of_kns, Q)
        if result:
            curr_wt_of_kns, curr_pro_of_kns, velocity = result
        else:
            break  # Break the loop if no valid combination is found

        time_to_next_city = distance_matrix[cities[i]][cities[i+1]] / velocity
        total_time += time_to_next_city

    if result:  # Check if the last iteration was successful
        time_to_start_city = distance_matrix[cities[-1]][cities[0]] / velocity
        total_time += time_to_start_city

    total_profit = curr_pro_of_kns
    return total_time, total_profit

# Example usage:
# Define the cities and the order in which they will be visited.
#cities = ['A', 'B', 'C', 'D']

# Define the distance matrix.
#distance_matrix = {
    'A': {'B': 100, 'C': 250, 'D': 120}#,
    'B': {'A': 100, 'C': 150, 'D': 350}#,
    'C': {'A': 250, 'B': 150, 'D': 200}#,
    'D': {'A': 120, 'B': 350, 'C': 200}
#}

# Define the weights and profits for each city.
#weights = {
    'A': [1, 2]#,
    'B': [2, 3]#,
    'C': [3, 4]#,
    'D': [4, 5]
#}
#profits = {
    'A': [10, 20]#,
    'B': [20, 30]#,
    'C': [30, 40]#,
    'D': [40, 50]
#}

# Knapsack capacity
#Q = 5

# Velocities
#vmax = 100
#vmin = 50

# Calculate the travel time and profit.
#total_time, total_profit = calculate_travel_time(cities, distance_matrix, vmax, vmin, weights, profits, Q)

# Output the results.
#print(total_time, total_profit)