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
    assert len(D) >= pop_size, "The population size you want is larger than the number of parents. Try a smaller value for pop_size."


    # first, plot all the coordinates
    plt.scatter(D[:,0], D[:,1], marker='.', s=2)

    current_parents = 0

    while len(current_parents) < pop_size:
        # fill up the parents for evolution?
        # I need to do some research here on how to do this

        # initialise the Pareto front - initially, all items count as being on the front until proven otherwise
        red_front = np.ones(len(D), dtype=bool) # this is for the lowest scores

        # loop through each item, which will be compared to all other items
        # here, we make a mask for the data points to pick out pareto fronts
        for i in range(len(D)):
            # print("current vector:")
            # print(D[i])
            for j in range(len(D)):

                # checking if it should be in the red front
                # if it's not been dominated by anyone, then it deserves to be red.
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

        assert len(pareto_front) <= pop_size, "Oh no! We have more parrots than we want to go through to be evolved. We'll have to pick out the sparser ones"

    return pareto_front