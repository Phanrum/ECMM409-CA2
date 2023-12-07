import numpy as np
import matplotlib.pyplot as plt
def plot_pareto(df):
    """
    Plots the costs and times in a numpy array and then selects the Pareto fronts in green (max) and red (min).

    Parameters
    ----------
    data : numpy array
        Data to be plotted. The first column should be

    Returns
    -------
    None
    """


    # only get every 10th row of the data
    df1000 = df[np.arange(len(df)) % 10 == 0]

    # first, plot all the coordinates
    plt.scatter(df1000["LLH Long"], df1000["LLH Lat"], marker='.', s=2)

    # prepare the vectors
    D = np.asarray(df1000[["LLH Long", "LLH Lat"]])

# inspired by
# https://stackoverflow.com/questions/68284055/pareto-front-for-matplotlib-scatter-plot
    # initialise the Pareto front - initially, all items count as being on the front until proven otherwise
    green_front = np.ones(D.shape[0], dtype=bool) # this is for the highest scores
    red_front = np.ones(D.shape[0], dtype=bool) # this is for the lowest scores


    # loop through each item, which will be compared to all other items
    for i in range(D.shape[0]):
        # print("current vector:")
        # print(D[i])
        for j in range(D.shape[0]):
            # print("     compared to:")
            # print(D[j])

            # checking if it should be in the green front
            if D[i][0] < D[j][0] and D[i][1] < D[j][1]:
                # print(f"{D[i]} is dominated by {D[j]}!")
                # oh dear. in that case, let's mark this in our mask.
                green_front[i] = False
                # it's enough for it to be dominated by 1 vector
                break

        for j in range(D.shape[0]):

            # checking if it should be in the red front
            # essentially the same thing but the other way round. if it's not been dominated by anyone, then it deserves to be red.
            if D[i][0] > D[j][0] and D[i][1] > D[j][1]:

                red_front[i] = False
                break


    # here, we only have the vectors which are not dominated
    green_parrots = D[green_front]
    red_parrots = D[red_front]
    # but wait, parrots need to be a df
    green_parrots = pd.DataFrame(green_parrots)
    red_parrots = pd.DataFrame(red_parrots).sort_values(by=0, ascending=False)

    # plot the parrots
    plt.plot(green_parrots[0], green_parrots[1], color="g", label="Max front")
    plt.plot(red_parrots[0], red_parrots[1], color="r", label="Min front")
    plt.legend(fontsize=13)
    plt.xlabel("Longitude", fontsize=15)
    plt.ylabel("Latitude", fontsize=15)
    plt.title("Pareto front of GPS measurements", size=17)