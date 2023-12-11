import numpy as np
import matplotlib.pyplot as plt

import logging

# dev
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.WARNING,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


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
    plt.scatter(D[:, 0], D[:, 1], marker='.', s=2)

    # while len(current_parents) < pop_size:
    # fill up the parents for evolution?
    # I need to do some research here on how to do this
    # I think i'll leave it in one function to find the pareto front of some data. and that's it.
    # because we'll call it at the end
    # meanwhile, another function will dissect layers of the front to get as many parents as we need

    # initialise the Pareto front - initially, all items count as being on the front until proven otherwise
    red_front = np.ones(len(D), dtype=bool)  # this is for the lowest scores

    # loop through each item, which will be compared to all other items. here, we make a mask for the data points to pick out pareto fronts
    for i in range(len(D)):
        for j in range(len(D)):

            # checking if it should be in the pareto front
            # if it's not been dominated by anyone, then it deserves to be in the front.
            if D[i, 0] > D[j, 0] and D[i, 1] < D[j, 1]:
                red_front[i] = False
                break

    # here, we only have the vectors which are not dominated
    pareto_front = D[red_front]
    # but sort them
    pareto_front = pareto_front[pareto_front[:, 0].argsort()]

    logging.info("pareto front:")
    logging.info(pareto_front)

    # plot the parrots
    plt.plot(pareto_front[:, 0], pareto_front[:, 1], color="r", label="Min front")
    plt.legend(fontsize=13)
    plt.xlabel("Time", fontsize=15)
    plt.ylabel("Profit", fontsize=15)
    plt.title("Pareto front of TTF solutions", size=17)

    # assert len(pareto_front) <= pop_size, "Oh no! We have more parrots than we want to go through to be evolved. We'll have to pick out the sparser ones"

    return pareto_front


def plot_pareto(costs, label):
    """
    Placeholder for the code which plots a pareto front
    Parameters
    ----------
    costs : 2D numpy array
        The first column will be plotted on the x axis, and the second on the y axis.
    label : str The label displayed on the plot

    Returns
    -------
    None
    """

    # plot the parrots
    costs = np.sort(costs, axis=0)

    plt.plot(costs[:, 0], costs[:, 1], label=label)
    plt.scatter(costs[:, 0], costs[:, 1], s=10, c="r")
    plt.legend(fontsize=13)
    plt.xlabel("Time", fontsize=15)
    plt.ylabel("Profit", fontsize=15)
    plt.title("Pareto front of TTF solutions", size=17)

    plt.show()


# ok basically
# here i have coded a naive approach which apparently scales with O(MN3)
# so maybe let's not do that
# like we can for comparison but if the complexity is this bad and we have this much data, then i'll start with nsga-II
def fast_non_dominated_sort(P):
    """
    Fast non-dom sorting approach proposed by Deb, K. et al in "A Fast and Elitist Multiobjective Genetic Algorithm:
NSGA-II"
    Pretty much from https://github.com/haris989/NSGA-II/blob/master/NSGA%20II.py (comments mine)

    Parameters
    ----------
    P : 2D numpy array
        Data to be ranked. The first column should be time, the second column should be profit.

    Returns
    -------
    front : list
        A list of fronts. Each item contains the indices of solutions belonging in each front.
    """

    time = P[:, 0]
    profit = P[:, 1]

    # looks like we're basically assuming that nothing dominates each p
    S = [[] for i in range(len(time))]  # sets of solutions which each p will dominate
    n = [0 for i in range(len(time))]  # numbers of solutions which dominate each p
    rank = [0 for i in range(len(time))]  # assume everyone's rank is 0
    front = [[]]  # i'm guessing each list in this list will be a different front

    for p in range(len(time)):
        logging.info("-" * 30)
        logging.info(f"p: {p}")
        logging.info(P[p])
        S[p] = []  # set of solutions that p dominates
        n[p] = 0  # number of solutions which dominate p

        for q in range(len(time)):
            if (time[p] < time[q] and profit[p] > profit[q]) or \
                    (time[p] <= time[q] and profit[p] > profit[q]) or \
                    (time[p] < time[q] and profit[p] >= profit[q]):  # if p dominates q

                if q not in S[p]:  # if q is not yet in the set of solutions that p dominates
                    S[p].append(q)

            elif (time[q] < time[p] and profit[q] > profit[p]) or \
                    (time[q] <= time[p] and profit[q] > profit[p]) or \
                    (time[q] < time[p] and profit[q] >= profit[p]):  # if q dominates p

                n[p] += 1  # increase the count of solutions which dominate p, by 1

        logging.info("number of sols which dominate p:")
        logging.info(n[p])

        if n[p] == 0:  # if nothing dominates p
            rank[p] = 0  # then it's got rank 0

            logging.info("Congrats! This p is in the front.")

            if p not in front[0]:  # if this p is not in the front yet
                front[0].append(p)

    # now we've got the actual front, now we do subsequent fronts
    i = 0
    while (front[i] != []):  # as long as something is in that front which is not an empty list
        Q = []  # stores the members of the next front
        for p in front[i]:  # for solution in this front
            for q in S[p]:  # visit every solution that p dominates
                n[q] -= 1  # decrease the number of sols that dominate it, by 1

                if n[q] == 0:  # if it's no longer dominated by anything
                    rank[q] = i + 1  # then it's rank is the next one

                    if q not in Q:  # if q is not in the set yet
                        Q.append(q)

        i += 1  # going to the next i
        front.append(Q)  # putting this front in our collection

    # ok now delete the last list because it has nothing in it
    del front[len(front) - 1]

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
    plt.scatter(data[:, 0], data[:, 1], marker='.', s=6)

    # plot each front
    for f in fronts:
        # but sort them for plotting
        nth_front = data[f]
        nth_front = nth_front[nth_front[:, 0].argsort()]

        plt.plot(nth_front[:, 0], nth_front[:, 1])

    plt.show()


def crowding_distance_assignment(I):
    """
    The crowding-distance computation procedure of all solutions in a non-dominated set I.

    Parameters
    ----------
    I : 2D array
        An array of non-dominated solutions. In our case, the first column should contain time, and the second - profit.

    Returns
    -------
    DistI : 1D array
        Crowding distances for each solution
    """

    l = len(I)  # number of solutions in I
    DistI = np.zeros((l, 1))  # distances for each solution

    for m in range(2):  # for each objective
        I = np.sort(I,
                    axis=m)  # sort by each objective - ie. sort by time first, then it'll sort by profit in the next loop
        DistI[0] = 99999999  # infinity, i guess
        DistI[-1] = 99999999  # set infinite distance to boundary cases

        for i in range(1, l - 1):  # for all other points, calculate the distance
            DistI[i] = DistI[i] + (I[i + 1, m] - I[i - 1, m]) / (np.max(I[m]) - np.min(I[m]))
            # where the denominator is composed of the max value of objective m and the min value of objective m
            # also, we sum up the distances for each objective

    return DistI


def crowded_comparison_operator(rank_i, rank_j, dist_i, dist_j):
    """
    Determines whether the partial order of i is higher than j, ie. if i should be preferred over j.
    But has an issue if the two are the same - attempts to be remedied in the paper i haven't understood yet.

    Parameters
    ----------
    rank_i : int
        The pareto front on which i is.
    rank_j : int
        The pareto front on which j is.
    dist_i : float
        The crowding distance of i.
    dist_j : float
        The crowding distance of j.

    Returns
    -------
    bool
        Whether i is preferred over j.
    """

    if rank_i < rank_j or ((rank_i == rank_j) and (dist_i > dist_j)):
        return True
    return False


def calc_rank_and_crowding_distance(P, plot=False):
    """
    Takes a population of times and costs and appends two columns: front rank and crowding distance.

    Parameters
    ----------
    P : 2D array
        The first column should be times and the second column should be profits.
    plot : bool (default: False)
        Determine whether to visualise the pareto fronts.

    Returns
    -------
    data : 2D array
        Same as P, but has two extra columns: front rank and crowding distance.

    """

    data = np.zeros((len(P), 5))  # initiate
    data[:, :2] = P  # the first two columns filled with solutions (that is, their evaluations)

    fronts = fast_non_dominated_sort(data[:, :2])  # calculate which front each solution belongs to

    # Now, for every solution, there has to be a rank column and a distance column
    for rank, f in enumerate(fronts):  # for every front
        # put ranks in the rank column
        for i in fronts[rank]:  # for every index in the front
            data[i, 2] = rank
        # put distances in the distances column
        I = data[f, :2]  # get this rank's points
        data[f, 3] = crowding_distance_assignment(I)[:, 0]  # put the distances in the last column of data

    # adding an index would be very useful
    data[:, -1] = list(range(len(P)))

    if plot:
        plot_fronts(P, fronts)

    return data, fronts


def nsga_2_replacement_function(N, costs, fronts):
    """
    Performs NSGA-II to use front ranking and crowd distance sorting to pick out a new population in an elitist way.

    Parameters
    ----------
    N : int
        Population size.
    costs : 2D numpy array
        columns:
        0 and 1: data (time, profit)
        2: front rank
        3: crowding distance
        4: index
    fronts : list[list[int]]
        A list of fronts in ascending order. The output of fast_non_dominated_sort().

    Returns
    -------
    solutions_to_carry : list[int]
        A list of indices. These indices tell us which solutions to pick for the next population. Because solutions
        should have the same indices as their cost evaluations.

    """
    # I don't know how to do it in a more efficient way but anyway
    # P_new = np.zeros((N, 2)) # initialise the new population which will come out at the end

    # maybe do it in a lazy way in the future but right now i just want something that will work
    solutions_to_carry = []
    i = -1
    while len(solutions_to_carry) <= N:
        i += 1

        logging.info(f"i: {i}")
        space_left = N - len(solutions_to_carry)
        logging.info(f"space left: {space_left}")
        logging.info(f"length of the front to add: {len(fronts[i])}")

        if len(fronts[i]) <= space_left:
            logging.info("solutions to carry extended")
            solutions_to_carry.extend(fronts[i])
            logging.info(f"length of current solutions to carry: {len(solutions_to_carry)}")
        else:
            # if you got to this point, that means there's a limited amount of space left
            group_to_assess = costs[fronts[i]]
            # sort by crowding distance
            group_to_assess = group_to_assess[group_to_assess[:, 3].argsort()[::-1]]
            logging.info("grop to assess:")
            logging.info(group_to_assess)

            # fill up solutions with enough of the assessed ones
            solutions_to_carry.extend(
                group_to_assess[:space_left, -1].astype(int))  # the last column because that's where the indices are

            logging.info("final solutions:")
            logging.info(solutions_to_carry)
            logging.info(f"length of solutions to carry: {len(solutions_to_carry)}")

            break

    return solutions_to_carry

def tour_select(tour_size, N, costs):
    """
    Runs a tournament of costs. Selects a winner based on front rank and then crowding distance.

    Parameters
    ----------
    tour_size : int
        The number of competing costs.
    N : int
        The size of the population.
    costs : 2D numpy array
        columns:
        0 and 1: data (time, profit)
        2: front rank
        3: crowding distance
        4: index

    Returns
    -------
    winner : int
        The index of the winning solution (taken from the last column)
    """

    lucky_numbers = np.random.randint(N, size=tour_size)
    competitors = costs[lucky_numbers]
    logging.info("lucky competitors!")
    logging.info(competitors)

    # now to choose the fittest. the fittest one will have the highest rank so only get those

    best_rank = np.min(competitors[:, 2])  # if it's totally random, it should be more diverse. if it's down to a probability
    # that's related to eg their rank, then it might converge to a local min. so we do it the random way for now.

    logging.info(f"best rank: {best_rank}")
    shortlist = competitors[np.where(competitors[:, 2] == best_rank)]
    logging.info("shortlist:")
    logging.info(shortlist)

    # and now break ties between the shortlisted ones
    winner = np.argmin(shortlist[:, 3])
    logging.info(f"winning solution: {shortlist[winner][-1]}")

    return int(shortlist[winner][-1])



