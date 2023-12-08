import numpy as np
import matplotlib.pyplot as plt

def pareto_parents(D):
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
    Pretty much from https://github.com/haris989/NSGA-II/blob/master/NSGA%20II.py

    Parameters
    ----------
    P : 2D numpy array
        Data to be ranked. The first column should be time, the second column should be profit.

    Returns
    -------
    front : list
        A list of fronts? I'm not sure tbh
    """

    time = P[:,0]
    profit = P[:,1]

    # looks like we're basically assuming that nothing dominates each p
    S = [[] for i in range(len(time))] # sets of solutions which each p will dominate
    n = [0 for i in range(len(time))] # numbers of solutions which dominate each p
    rank = [0 for i in range(len(time))] # assume everyone's rank is 0
    front = [[]] # i'm guessing each list in this list will be a different front

    for p in range(len(time)):
        # print("-"*30)
        # print(f"p: {p}")
        # print(P[p])
        S[p] = [] # set of solutions that p dominates
        n[p] = 0 # number of solutions which dominate p

        for q in range(len(time)):
            if (time[p] < time[q] and profit[p] > profit[q]) or \
                    (time[p] <= time[q] and profit[p] > profit[q]) or \
                    (time[p] < time[q] and profit[p] >= profit[q]): # if p dominates q

                if q not in S[p]: # if q is not yet in the set of solutions that p dominates
                    S[p].append(q)

            elif (time[q] < time[p] and profit[q] > profit[p]) or \
                (time[q] <= time[p] and profit[q] > profit[p]) or \
                (time[q] < time[p] and profit[q] >= profit[p]): # if q dominates p

                n[p] += 1 # increase the count of solutions which dominate p, by 1

        # print("number of sols which dominate p:")
        # print(n[p])

        if n[p] == 0: # if nothing dominates p
            rank[p] = 0 # then it's got rank 0

            # print("Congrats! This p is in the front.")

            if p not in front[0]: # if this p is not in the front yet
                front[0].append(p)

    # now we've got the actual front, now we do subsequent fronts
    i = 0
    while (front[i] != []): # as long as something is in that front which is not an empty list
        Q = [] # stores the members of the next front
        for p in front[i]: # for solution in this front
            for q in S[p]: # visit every solution that p dominates
                n[q] -= 1 # decrease the number of sols that dominate it, by 1

                if n[q] == 0: # if it's no longer dominated by anything
                    rank[q] = i + 1 # then it's rank is the next one

                    if q not in Q: # if q is not in the set yet
                        Q.append(q)

        i += 1 # going to the next i
        front.append(Q) # putting this front in our collection

        # del front[len(front) - 1] # ngl not sure what this is for
    return front


def plot_fronts(data, fronts):
    """
    Make a pot of pareto fronts
    Parameters
    ----------
    data : 2D array
        The data which will be plotted on the scatterplot
    fronts : list [lists]
        A list of fronts. Each list contains integers which correspond to indices of data points.

    Returns
    -------
    None
    """

    # plot the data
    plt.scatter(data[:,0], data[:,1], marker='.', s=2)

    # plot each front
    for f in fronts:
        # but sort them for plotting
        nth_front = data[f]
        nth_front = nth_front[nth_front[:, 0].argsort()]

        plt.plot(nth_front[:,0], nth_front[:,1])

    plt.show()



# # make a random array to test this on
# data = np.random.normal(3, 2.5, size=(600, 2))
#
#
# fronts = fast_non_dominated_sort(data)
#
# print(fronts)
#
# plot_fronts(data, fronts)