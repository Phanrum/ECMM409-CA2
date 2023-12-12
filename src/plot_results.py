import matplotlib.pyplot as plt
import numpy as np
import os

# import our own modules
import sys
sys.path.append('../src')

from pareto import plot_pareto

files = [
    "a280-TTP_n279_600_iter_costs_2023-12-11 17-01-01.npy",
    "a280-TTP_n279_1000_iter_costs_2023-12-11 19-30-56.npy",
    "a280-TTP_n279_2000_iter_costs_2023-12-12 12-25-28.npy",
    "a280-TTP_n279_3000_iter_costs_2023-12-12 13-04-39.npy",
    "a280-TTP_n279_4000_iter_costs_2023-12-12 13-51-26.npy",
    "a280-TTP_n279_5000_iter_costs_2023-12-12 14-45-43.npy",
    "a280-TTP_n279_6000_iter_costs_2023-12-12 16-26-40.npy"
]

for f in files:

    filename_costs = rf"cache/{f}"
    iterations = int(os.path.basename(filename_costs).split("_")[2])
    fake_costs_extended = np.load(filename_costs)[:,:2]

    plot_pareto(fake_costs_extended, f"{iterations} iters", show=False)

# filename_costs = r"cache/a280-TTP_n279_2000_iter_costs_2023-12-12 12-25-28.npy"
# iterations = int(os.path.basename(filename_costs).split("_")[2])
# fake_costs_extended = np.load(filename_costs)[:,:2]
#
# plot_pareto(fake_costs_extended, "brr", show=True)
plt.savefig("test_pareto.png", dpi=600, bbox_inches="tight")
plt.show()