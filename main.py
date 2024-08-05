import SA_workshift as SA
from helpers.helper import print_schedule
import random

# for debugging perpose
random.seed(1)

solution = SA.run()
print_schedule(solution.state)