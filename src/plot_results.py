import matplotlib.pyplot as plt
import numpy as np
import os

# import our own modules
import sys
sys.path.append('../src')

from pareto import plot_pareto

dataset = "a280-TTP_n1395"

files = [
    "a280-TTP_n1395_1200_iter_costs_2023-12-12 20-21-12.npy",
    "a280-TTP_n1395_1000_iter_costs_2023-12-12 02-17-38.npy",
    "a280-TTP_n1395_800_iter_costs_2023-12-12 00-57-08.npy",
]

for f in files:

    filename_costs = rf"cache/{f}"
    iterations = int(os.path.basename(filename_costs).split("_")[2])
    fake_costs_extended = np.load(filename_costs)[:,:2]

    plot_pareto(fake_costs_extended, f"{iterations} iters", title=dataset, single=False, show=False)

plt.savefig(f"../figs/several_pareto_{dataset}.png", dpi=600, bbox_inches="tight")
plt.show()