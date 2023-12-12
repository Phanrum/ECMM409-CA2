import sys
sys.path.append('/Users/nikhil/latest_8_dec/ECMM409-CA2/src')  ##remove this and give urs if neeeded 
import math
import numpy as np
from parsing import Dataset, item_section
from ttp import make_distance_matrix
from crossover import crossover_tsp, crossover_kp_but_make_it_indian

# Function to calculate Euclidean distance between two nodes
def euclidean_distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

# Placeholder functions for checking validity
def is_valid_tour(tour, num_cities):
    return len(tour) == num_cities and len(set(tour)) == num_cities

def is_valid_knapsack(knapsack, items, capacity):
    total_weight = sum(item.weight for item, k in zip(items, knapsack) if k == 1)
    return total_weight <= capacity


file_path = "/Users/nikhil/latest_8_dec/ECMM409-CA2/data/a280-n279.txt"

# Read the content of the file
with open(file_path, 'r') as file:
    file_content = file.read()

# Parse the data
parsed_dataset = Dataset.new(file_content)

# Check the parsing results
print("Number of nodes correct:", len(parsed_dataset.nodes) == 280)
print("Number of items correct:", len(parsed_dataset.items) == 279)

# Create a distance matrix
num_cities = len(parsed_dataset.nodes)
distance_matrix = np.zeros((num_cities, num_cities))
for i in range(num_cities):
    for j in range(num_cities):
        if i != j:
            distance_matrix[i][j] = euclidean_distance(parsed_dataset.nodes[i], parsed_dataset.nodes[j])

# Test the distance calculation
city1, city2 = parsed_dataset.nodes[0], parsed_dataset.nodes[1]
manual_distance = euclidean_distance(city1, city2)
matrix_distance = distance_matrix[city1.index - 1][city2.index - 1]
print("Manual distance:", manual_distance)
print("Matrix distance:", matrix_distance)
print("Distance calculation correct:", np.isclose(manual_distance, matrix_distance))

# Test TSP crossover
parent1 = [1, 2, 3, 4, 5]  #
parent2 = [5, 4, 3, 2, 1]  
child1, child2 = crossover_tsp(parent1, parent2)
print("Child1 valid:", is_valid_tour(child1, len(parent1)))
print("Child2 valid:", is_valid_tour(child2, len(parent2)))

# Test KP crossover
knapsack1 = [0] * len(parsed_dataset.items)
knapsack2 = [0] * len(parsed_dataset.items)
# Set some items to 1 as needed for testing
child1, child2 = crossover_kp_but_make_it_indian(knapsack1, knapsack2, item_section(parsed_dataset), parsed_dataset.knapsack_capacity)
print("Child1 valid:", is_valid_knapsack(child1, parsed_dataset.items, parsed_dataset.knapsack_capacity))
print("Child2 valid:", is_valid_knapsack(child2, parsed_dataset.items, parsed_dataset.knapsack_capacity))



