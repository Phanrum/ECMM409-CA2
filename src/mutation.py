import numpy as np

def single_swap_mutation_tsp(child):
    """
    This function performs a single-swap mutation on a child.

    Parameters
    ----------
    child : 1D numpy array
        Child which is to be mutated.

    Returns
    -------
    child : 1D numpy array
        Child generated after performing the mutation.
    """

    mutation_index_1, mutation_index_2 = np.random.choice(len(child), 2, replace=False)
    child[mutation_index_1], child[mutation_index_2] = child[mutation_index_2], child[mutation_index_1]

    return child

def bit_flip_mutation_kp(child):
    """
    This function performs a bit-flip mutation on a child.

    Parameters
    ----------
    child : 1D numpy array
        Child which is to be mutated.

    Returns
    -------
    child : 1D numpy array
        Child generated after performing the mutation.
    """

    one_indices = np.where(child == 1)[0]
    zero_indices = np.where(child == 0)[0]
    random_index_one = np.random.choice(one_indices, 1)
    random_index_zero = np.random.choice(zero_indices, 1)
    child[random_index_one[0]] = 1 - child[random_index_one[0]]
    child[random_index_zero[0]] = 1 - child[random_index_zero[0]]

    return child

# def multiple_swap_mutation(child, no_swaps):
#    """
#    This function performs a multiple-swap mutation on a child.
#
#    Parameters
#    ----------
#    child : 1D numpy array
#        Child which is to be mutated.
#    no_swaps : int
#        Number of swaps to be performed on the child.
#
#    Returns
#    -------
#    mutated_individual : 1D numpy array
#        Child generated after performing the mutation.
#    """
#
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
    """
    This function checks whether the recently mutated child violates the rule of knapsack or not.

    Parameters
    ----------
    item_weight : 1D numpy array
        An array containing the weights of all the items.
    child : 1D numpy array
        Recently generated child.
    max_weight : float
        Maximum capacity of the knapsack.

    Returns
    -------
    True/False : Boolean Value
        Returns whether the sum of all the selecetd items represented by the binary list
        is greater than the weight of the knapsack or not.
    """
    
    calculated_weight: int = 0

    for (i,city) in enumerate(child):
        if city == 1:
            calculated_weight += item_weight[i]

    if calculated_weight < max_weight:
        return False
    else:
        return True



def fix_kp_mutation(items, max_weight, knapsack):
    """
    This function fixes a recently generated knapsack child by performing a bit-flip mutation.
    A child is to be fixed if it violates the rule of knapsack.

    Parameters
    ----------
    items : An items object
        An object representing an item.
    max_weight : float
        Maximum capacity of the knapsack.
    knapsack : 1D numpy array
        Recently generated child.

    Returns
    -------
    child1 : 1D numpy array
        Child generated after fixing the errors.
    """

    item_weight = [items[i].weight for i in range(len(items))]  # item weights

    while is_over_weight(item_weight, child1, max_weight):
        child1 = bit_flip_mutation_kp(knapsack)

    return child1

def tsp_mutation(tsp_parent_1, tsp_parent_2):
    """
    This function accepts 2 city travel arrays and performs a single-swap mutation on both of them.

    Parameters
    ----------
    tsp_parent_1, tsp_parent_2 : 1D numpy array
        Parents selected for the single-swap mutation.

    Returns
    -------
    child1, child2 : 1D numpy array
        The resultant children generated after performing a single-swap mutation.
    """

    child1 = single_swap_mutation_tsp(tsp_parent_1)
    child2 = single_swap_mutation_tsp(tsp_parent_2)

    return child1, child2

def kp_mutation(item_section, knapsack1, knapsack2, Q):
    """
    Performs a bit flip mutation on two packing lists.

    Parameters
    ----------
    item_section : 2D numpy array
        A reconstruction of the item section from the parsed data.
    knapsack1, knapsack2 : 1D numpy array
        A binary list determining which items to pick up.
    Q : float
        Maximum capacity of the knapsack.

    Returns
    -------
    child_knapsack_1, child_knapsack_2 : 1D numpy array
        Mutated packing lists.
    """


    weight_array = item_section[:,2]

    not_a_good_list = True

    while not_a_good_list:

        child_knapsack_1, child_knapsack_2 = bit_flip_mutation_kp(knapsack1), bit_flip_mutation_kp(knapsack2)

        w1 = sum(weight_array * child_knapsack_1)
        w2 = sum(weight_array * child_knapsack_2)
        if w1 <= Q and w2 <= Q: not_a_good_list = False
        # the while loop keeps on generating packing lists until the knapsack condition is not violated

    return child_knapsack_1, child_knapsack_2

    
    


