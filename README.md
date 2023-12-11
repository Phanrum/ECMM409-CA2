# ECMM409-CA2
## Introduction
We present an algorithm which tackles the Traveling Thief Problem by using a genetic algorithm (GA). It aims to optimise the travel plan and packing plan of the thief to maximise the profit he makes and minimise the time it takes him.
The GA used here is the NSGA-II with the following operators.
* Travel plan: Crossover with fix, Swap mutation
* Packing plan: CROSSOVER?, Bit swap mutation(TBC)

Crucially, the thief pays rent for the knapsack, which is deducted from his gross profit.
## Instructions
To run this program, open main.py. At the top of the file, input the following information:
* N (int) : population size
* iterations_total (int) : the total number of iterations you wish to execute
* tour_size (int) : tournament size
* data_name (str) : the path to the dataset you wish to use

The program has a pause/play functionality, which allows us to run the GA for a number of iterations, save the results, and then read them and continue evolving later.
Thus, the program will first ask you whether you wish to pick up where you left off. If not, simply press Enter to proceed. If so, input the root path to the saved results.
The number of iterations which will be executed from now on will be iterations_total minus the number of iterations you have already done.

Thank you for using our algorithm and we hope you have a smooth experience!