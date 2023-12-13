# ECMM409-CA2
## Introduction
We present a program which tackles the Traveling Thief Problem by using a genetic algorithm (GA). It aims to optimise the travel plan and packing plan of the thief to maximise the profit he makes and minimise the time it takes him to travel.
The GA used here is the NSGA-II with the following operators.
* Travel plan: Crossover with fix, Swap mutation
* Packing plan: Single point crossover, Bit flip mutation

Crucially, the thief pays rent for the knapsack, which is deducted from his gross profit.
## Instructions
To run this program, open main.py. At the top of the file, input the following information:
* N (int) : population size
* iterations_total (int) : the total number of iterations you wish to execute
* tour_size (int) : tournament size
* data_name (str) : the path to the dataset you wish to use

The program has a pause/play functionality, which allows us to run the GA for a number of iterations, save the results, and then read them and continue evolving later.
Thus, the program will first ask you whether you wish to pick up where you left off. If not, simply press Enter twice to proceed. If you wish to continue from a saved point, input the root path to the saved results (these are stored in src/cache). The number of iterations which will be executed from now on will be iterations_total minus the number of iterations you have already done.

All visualisations are present in the "figs" directory, and the competition-compatible outputs are in the "results" directory.

Thank you for using our algorithm and we hope you have a smooth experience!
