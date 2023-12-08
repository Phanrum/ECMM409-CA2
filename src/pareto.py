import numpy as np
import matplotlib.pyplot as plt

def pareto_parents(D, pop_size):
    """
    Plots the costs and times in a numpy array and then selects the Pareto fronts in green (max) and red (min).

    Parameters
    ----------
    D : numpy array
        Data to be plotted. The first column should be time, the second should be profit.
    pop_size : int
        Size of the population you'd like to choose.

    Returns
    -------
    pareto_front : numpy array
        An aray of pareto parents.
    """

    # errors
    # assert len(D) >= pop_size, "The population size you want is larger than the number of parents. Try a smaller value for pop_size."
    # actually this is ok. if it's <pop size then we'll need to sort them somehow and pick out as many as pop says

    # first, plot all the coordinates
    plt.scatter(D[:,0], D[:,1], marker='.', s=2)

    # while len(current_parents) < pop_size:
        # fill up the parents for evolution?
        # I need to do some research here on how to do this
        # I think i'll leave it in one function to find the pareto front of some data. and that's it.
        # because we'll call it at the end
        # meanwhile, another function will dissect layers of the front to get as many parents as we need



    # initialise the Pareto front - initially, all items count as being on the front until proven otherwise
    red_front = np.ones(len(D), dtype=bool) # this is for the lowest scores

    # loop through each item, which will be compared to all other items. here, we make a mask for the data points to pick out pareto fronts
    for i in range(len(D)):
        for j in range(len(D)):

            # checking if it should be in the pareto front
            # if it's not been dominated by anyone, then it deserves to be in the front.
            if D[i,0] > D[j,0] and D[i,1] < D[j,1]:
                red_front[i] = False
                break


    # here, we only have the vectors which are not dominated
    pareto_front = D[red_front]
    # but sort them
    pareto_front = pareto_front[pareto_front[:, 0].argsort()]

    print("pareto front:")
    print(pareto_front)

    # plot the parrots
    plt.plot(pareto_front[:,0], pareto_front[:,1], color="r", label="Min front")
    plt.legend(fontsize=13)
    plt.xlabel("Time", fontsize=15)
    plt.ylabel("Profit", fontsize=15)
    plt.title("Pareto front of TTF solutions", size=17)

    # assert len(pareto_front) <= pop_size, "Oh no! We have more parrots than we want to go through to be evolved. We'll have to pick out the sparser ones"

    return pareto_front

def plot_pareto(stuff):
    """
    Placeholder for the code which plots pareto
    Parameters
    ----------
    stuff

    Returns
    -------

    """


# ok basically
# here i have coded a naive approach which apparently scales with O(MN3)
# so maybe let's not do that
# like we can for comparison but if the complexity is this bad and we have this much data, then i'll start with nsga-II
def fast_non_dominated_sort(P):
    """
    Fast non-dom sorting approach proposed by Deb, K. et al in "A Fast and Elitist Multiobjective Genetic Algorithm:
NSGA-II"

    Parameters
    ----------
    P : 2D numpy array
        Data to be ranked. The first column should be time, the second column should be profit.

    Returns
    -------
    idk yet
    """

    # looks like we're basically assuming that nothing dominates each p
    S = [[] for i in range(len(P))] # sets of solutions which each p will dominate
    n = [0 for i in range(len(P))] # numbers of solutions which dominate each p
    rank = [0 for i in range(len(P))] # assume everyone's rank is 0
    front = [[]] # i'm guessing each list in this list will be a different front

    for i, p in enumerate(P): # p is a solution
        print("p:")
        print(p)
        print("i:")
        print(i)

        S[i] = [] # set of solutions that p dominates
        n[i] = 0 # number of solutions which dominate p


        for q in P: # compare p to every other solution
            # print("    q:")
            # print(f"    {q}")
            if (p[0] < q[0] and p[1] < q[1]) or \
                    (p[0] <= q[0] and p[1] < q[1]) or \
                    (p[0] < q[0] and p[1] <= q[1]): # if p dominates q

                S[i].append(q) # append q to the list of sols dominated by p
                # tu może być problem bo kod s gita ma tu indeksy a nie full q

            elif p[0] > q[0] and p[1] > q[1]: # if q dominates p
                n[i] += 1 # increase the number of sols which dominate p
                # print("np increased - p got dominated")
        print(f"n[{i}]: {n[i]}")
        if n[i] == 0: # if so, then p belongs to the first front
            prank = 1
            F[1].append(p)
            print(f"congrats! the following p is in the first front:\n{p}")
            print(F)

        print("-"*30)


    f = 1 # initialise the front counter
    # while F[f]:
    #     Q = 0 # stores the members of the next front
    #
    #     for i, p in enumerate(F[f]):
    #         for q in S[i]: # i'm not sure i understand

    return F





# make a random array to test this on
data = np.random.normal(3, 2.5, size=(60, 2))

print(fast_non_dominated_sort(data))

F = fast_non_dominated_sort(data)

print(F)
