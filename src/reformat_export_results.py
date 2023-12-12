import numpy as np
import pickle
import os

# import our own modules
import sys
sys.path.append('../src')

from parsing import Dataset

# input desired data
filename_costs = r"cache/a280-TTP_n1395_1200_iter_costs_2023-12-12 20-21-12.npy"
filename_population = r"cache/a280-TTP_n1395_1200_iter_population_2023-12-12 20-21-12.pkl"
data_name = "../data/a280-n1395.txt"


#Load cost and pop
fake_costs_extended = np.load(filename_costs)[:,:2]
with open(filename_population, 'rb') as f:
    population = pickle.load(f)
dataset = Dataset.new(open(data_name, 'r').read())
iterations = int(os.path.basename(filename_population).split("_")[2])

# create file called f"p_is_for_pomegranate_{dataset_name}.x"
with open(f"../results/p_is_for_pomegranate_{dataset.name}-n{dataset.number_items}_iter_{iterations}.x", "w") as xfile:

    for (city_travel, items_select) in population:
        xfile.write(f"{' '.join(str(e) for e in city_travel)}\n")
        xfile.write(f"{' '.join(str(e) for e in items_select)}\n")
        xfile.write("\n")

    xfile.close()

# create file called f"p_is_for_pomegranate_{dataset_name}.f"
with open(f"../results/p_is_for_pomegranate_{dataset.name}-n{dataset.number_items}_iter_{iterations}.f", "w") as ffile:

    #extract time and profit from fake_costs_extended
    time = fake_costs_extended[:, 0]
    profit = fake_costs_extended[:, 1]

    for (i,t) in enumerate(time):
        ffile.write(f"{t} {profit[i]}\n")

    ffile.close()
