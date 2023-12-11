def calculate_knapsack_weight_at_city(city_index, tour, items, decision_vector):
    """
    Calculate the weight of the knapsack at a given city during the thief's tour.

    Parameters:
    - city_index: The index of the current city in the tour.
    - tour: A list representing the order in which cities are visited (permutation vector).
    - items: A list of tuples, each representing an item and containing its availability at each city (binary)
             and its weight (e.g., [(availability, weight), ...]).
    - decision_vector: A binary list indicating whether each item is picked (1) or not (0).

    Returns:
    - The total weight of the knapsack at the given city.
    """
    total_weight = 0

    # Sum the weight of all items picked so far
    for k in range(city_index + 1):  # Include the current city in the sum
        city = tour[k]
        for j, (availability, weight) in enumerate(items):
            # If the item is available at the current city and is picked, add its weight
            if availability[city] == 1 and decision_vector[j] == 1:
                total_weight += weight

    return total_weight
