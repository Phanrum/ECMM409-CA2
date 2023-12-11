def single_swap_mutation_tsp(child):
    mutation_index_1, mutation_index_2 = np.random.choice(len(child), 2, replace=False)
    child[mutation_index_1], child[mutation_index_2] = child[mutation_index_2], child[mutation_index_1]
    return child
def bit_flip_mutation_kp(child):
    mutation_index= np.random.choice(len(child), 1, replace=False)
    mutated_vector[idx] = 1 - mutated_vector[mutation_index]
    return child

# def multiple_swap_mutation(child, no_swaps):
#     mutated_individual = child.copy()
#
#     # Choose distinct random positions to swap
#     positions = np.random.choice(len(mutated_individual), size=no_swaps, replace=False)
#
#     # Perform the swaps by shuffling the selected positions
#     np.random.shuffle(positions)
#
#     # Apply the swaps to the chromosome
#     for i in range(no_swaps):
#         mutated_individual[positions[i]], mutated_individual[positions[(i + 1) % no_swaps]] = (
#             mutated_individual[positions[(i + 1) % no_swaps]],
#             mutated_individual[positions[i]]
#         )
#
#     return mutated_individual



def is_over_weight(item_weight, child, max_weight):
    
    calculated_weight: int = 0

    for (i,city) in enumerate(child):
        if city == 1:
            calculated_weight += item_weight[i]

    if calculated_weight < max_weight:
        return False
    else:
        return True



def fix_kp_mutation(items,max_weight, knapsack):
    item_weight = [items[i].weight for i in range(len(items))]  # item weights

    while is_over_weight(item_weight, child1, max_weight):
        child1 = bit_flip_mutation_kp(knapsack)

    return child1

def tsp_mutation(child):
    """

   
    child: first child for mutation

    returns mutated child
    """

    child1= single_swap_mutation(child)


    return child1

def kp_mutation(items,knapsack,max_weight):
    child1=bit_flip_mutation_kp(knapsack)
    return fix_kp_mutation(items, child1, max_weight, knapsack)

    
    


