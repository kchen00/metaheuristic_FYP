import SA_workshift as SA
import GA_workshift as GA
import brute_force as BF
from helpers.helper import print_schedule
import random

# for debugging perpose
random.seed(1)

# # brute force method
# solution = BF.run()
# print_schedule(solution)

# # genetic algorithm method
# solution = GA.run()
# print_schedule(solution.genes)

# simulated annealing method
solution = SA.run()
print_schedule(solution.state)
