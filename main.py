import SA_workshift as SA
import GA_workshift as GA
from helpers.helper import print_schedule
import random

# for debugging perpose
random.seed(1)

# solution = SA.run()
# print_schedule(solution.state)

solution = GA.run()

print_schedule(solution.genes)