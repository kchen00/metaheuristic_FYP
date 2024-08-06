# TODO
# figure out the acceptance prob, somehow it keep increasing over iterations

from models.job import Job
from models.team import Team
from models.assignment import Assignment
import random
from helpers import helper
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt

jobs = helper.create_random_jobs(10)
teams = helper.create_random_team(4)

class Candidate:
    def __init__(self, state: list) -> None:
        self.state: list = state
        self.fitness: float = 0

def create_starting_state(j: Job, t: Team) -> list:
    """
    create a starting state for starting state
    """
    state = []

    for j in jobs:
        for t in teams:
            new_assignment = Assignment(j, t)
            state.append(new_assignment)
        
        # the choosen assigment to activate
        choosen_assigment: Assignment = random.choice([s for s in state if s.job == j])
        choosen_assigment.active = True
    
    return state

def create_neighbour_candidate(current_state: list, t: float) -> Candidate:
    """
    generates the neighbour candiate by modifying the current state
    controlled by the temperature
    higher temp means more changes 
    """
    neighbour_state = deepcopy(current_state)
    unique_jobs = {s.job for s in neighbour_state}

    # then choose a assignment with unique job and activate it
    for j in unique_jobs:
        if random.random() < t:
            state = [s for s in neighbour_state if s.job == j]
            random.shuffle(state)

            for s in state:
                s.active = False
            
            random.choice(state).active = True
    
    neighbour = Candidate(neighbour_state)

    return neighbour



def run(cooling_rate: float = 0.95) -> Candidate:
    """
    perform simulated annealing to find the best job and team assigment
    """
    starting_state = create_starting_state(jobs, teams)
    current = Candidate(starting_state)
    current.fitness = helper.calculate_make_span(starting_state)[1]
    hist = []
    temperature = 1

    for i in range(50):
        neighbour = create_neighbour_candidate(current.state, temperature)
        neighbour.fitness = helper.calculate_make_span(neighbour.state)[1]

        diff = neighbour.fitness - current.fitness
        accept_prob = 1 / (i + 1)

        # make span -> fitness of the state
        # lower maker span -> higher fitness
        # if the neighbour is better than the current one, ie lower make span

        # since the diff is determined by neighour - current
        # when diff is negative, means that neighbour make span is less than current one, accept it 
        if diff < 0 :
            print(f"{neighbour} has a shorter make span")            
            current = neighbour
        
        elif random.random() < accept_prob:
            print(f"RNG god says accept {neighbour} worse solution")
            current = neighbour
        
        else:
            print(f"{neighbour} solution is discarded")
        
        # cooling down the temperature
        hist.append(current.fitness)
        temperature *= cooling_rate
            


    plt.plot(hist)
    plt.show()
    return current

