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
    def __init__(self, jobs: list, teams: list, cooling_rate: float = 0.95, temperature: float = 1) -> None:
        self.jobs = jobs
        self.teams = teams

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
    
    def create_initial_solution(self) -> Solution:
        """
        creates the initial solution
        """
        state = []

        for j in self.jobs:
            # assign random team to the job
            selected_team = random.choice(self.teams)
            new_state = State(j, selected_team)
            state.append(new_state)
        
        current = Solution(state)
        return current

    def evaluate_candidate(self, candidate: Solution):
        """
        evaluates the candidate solution
        """
        # fitness in terms of make span
        t, make_span = helper.calculate_make_span(candidate.state)
        candidate.make_span = make_span
        candidate.fitness = make_span

        # keeping track of the best solution 
        if self.iteration == 1:
            self.best = self.current
            print("New best found!")
        else:
            if self.current.fitness < self.best.fitness:
                self.best = self.current
                print("New best found!")
        
    def create_neighbour_solution(self, change_prob: float) -> Solution:
        """
        based on the current solution create a neighbour solution by randomly activating and deactivating the state

        the amount of changes depends on the change_prob
        """
        state = []

        for s in self.current.state:
            new_state = State(s.job, s.team)
            if random.random() < change_prob:
                selected_team = random.choice(self.teams)
                new_state.team = selected_team
            
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
                    
        # else, based on a decreasng probability, determine whether or not to accept the solution
        else:
            if random.random() < self.temperature:
                self.current = self.neighbour
                print("RNG god accepts the neighbour solution")
        
        self.hist.append(self.current.fitness)
    
    def cool_down(self):
        self.temperature *= self.cooling_rate

def run():
    jobs = helper.create_random_jobs(10)
    teams = helper.create_random_team(5)

    anneal = Anneal(jobs, teams, cooling_rate=0.8)
    anneal.current = anneal.create_initial_solution()
    anneal.evaluate_candidate(anneal.current)
    
    for i in range(100):
        print(f"iteration {anneal.iteration} | temp: {anneal.temperature}")
        anneal.neighbour = anneal.create_neighbour_solution(anneal.temperature)
        anneal.evaluate_candidate(anneal.neighbour)
        anneal.decide_solution()
        anneal.cool_down()
        
        anneal.iteration += 1
    
    plt.plot(anneal.hist)
    plt.show()
    
    return anneal.best
    

