from helpers import helper
from models.job import Job
from models.team import Team
from models.assignment import Assignment
import random
import numpy as np
from matplotlib import pyplot as plt

class State(Assignment):
    def __init__(self, j: Job, t: Team):
        super().__init__(j, t)
        self.active = False

class Solution:
    """
    represent a possible solution in search space
    """
    def __init__(self, state: list):
        self.state = state
        self.fitness = 0
        self.make_span = 0

class Anneal:
    """
    represent the simulated annealing process
    """
    def __init__(self, cooling_rate: float = 0.95, temperature: float = 1) -> None:
        self.iteration = 1
        self.cooling_rate = cooling_rate
        self.temperature = temperature
        
        # the current candidate that is being evaluated
        self.current = None
        # the neighbbour solution
        self.neighbour = None
        # the best candidate overall
        self.best = None
        self.hist = []
    
    def evaluate_candidate(self, candidate: Solution):
        """
        evaluates the candidate solution
        """
        # fitness in terms of make span
        t, make_span_fit = helper.calculate_make_span(candidate.state)
        candidate.make_span = make_span_fit
        
        # fitness in terms of job acquired
        unique_job = {s.job for s in candidate.state}
        job_acquired = [s.job for s in candidate.state if s.active]
        job_fit = len(unique_job) - len(job_acquired)
        
        # if there is too much or too less job, add an arbitary large value
        if job_fit > len(unique_job) or job_fit < 0:
            job_fit += 9999

        candidate.fitness = make_span_fit + job_fit

    def create_neighbour_solution(self, change_prob: float) -> Solution:
        """
        based on the current solution create a neighbour solution by randomly activating and deactivating the state

        the amount of changes depends on the change_prob
        """
        # extracting the job and team from the current solution
        state = []
        for s in self.current.state:
            new_state = State(s.job, s.team)
            new_state.active = s.active
            if random.random() < change_prob:
                new_state.active ^= True
            
            state.append(new_state)
        
        neighbour = Solution(state)
        return neighbour
    
    def decide_solution(self):
        """
        accepts the neighbour solution based on probability
        """
        # if the neighbour solution is better, accepts it no matter what
        if self.neighbour.fitness < self.current.fitness:
            self.current = self.neighbour
            print(f"Neighbour solution is better than current solution")
            
            # keep track the best solution so far
            if self.iteration == 1:
                self.best = self.current
            else:
                if self.current.fitness < self.best.fitness:
                    self.best = self.current
                    print(f"New best found:  {"".join([str(int(s.active)) for s in self.best.state])} | {self.best.fitness}")
        
        # else, based on a decreasng probability, determine whether or not to accept the solution
        else:
            if random.random() < self.temperature:
                self.current = self.current
                print("RNG god accepts the neighbour solution")
        
        self.hist.append(self.current.fitness)
    
    def cool_down(self):
        self.temperature *= self.cooling_rate


def create_random_states(jobs: list, teams: list) -> list:
    """
    creates random states by randomly activating the states
    """
    state = []

    for j in jobs:
        for t in teams:
            new_state = State(j, t)
            new_state.active = random.choice([True, False])
            state.append(new_state)
    
    return state

def crete_random_solution(jobs: list, teams: list) -> Solution:
    state = create_random_states(jobs, teams)
    solution = Solution(state)
    return solution

jobs = helper.create_random_jobs(10)
teams = helper.create_random_team(5)

def run():
    anneal = Anneal(temperature=1)
    anneal.current = crete_random_solution(jobs, teams)
    anneal.evaluate_candidate(anneal.current)

    
    for i in range(200):
        anneal.neighbour = anneal.create_neighbour_solution(anneal.temperature)
        anneal.evaluate_candidate(anneal.neighbour)
        anneal.decide_solution()
        anneal.cool_down()
        
        anneal.iteration += 1
    
    plt.plot(anneal.hist)
    plt.show()
    
    return anneal.best
    

