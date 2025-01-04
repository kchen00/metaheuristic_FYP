from models.assignment import Assignment
from models.project import Project
import setup
import fitness_checker
import random
import numpy as np
from matplotlib import pyplot as plt
import difference_checker
from copy import deepcopy

class State(Assignment):
    '''represent a possible state'''
    def __init__(self, task, member):
        super().__init__(task, member)

class Solution:
    def __init__(self, states: list):
        self.states:list[State] = states
        self.fitness = 0

class SimulatedAnnealing:
    def __init__(self, current_solution, initial_temperature: float = 1000, cd: float = 0.99, total_neighbour: int = 5):
        self.temperature = initial_temperature
        self.cd = cd
        self.total_neighbours = total_neighbour
        self.neighbours:list[Solution] = list()
        self.current_solution:Solution = current_solution
        self.current_solution.fitness = fitness_checker.check_fitness(self.current_solution.states)

        self.iteration = 1

        self.average_fit = list()
        self.best_fit = list()
    
    def cooldown(self):
        '''cool down the temperature'''
        self.temperature *= self.cd
        # preventing the temperature going too low
        self.temperature = max(self.temperature, 0.0001)

    def create_neighbour_solution(self):
        '''creates neighbour solution
        
        the rate of changes is based on the temperature

        higher - more changes
        
        lower - less changes'''
        new_neighbours = list()
        change_prob = np.exp(-self.iteration/self.temperature) 

        for i in range(self.total_neighbours):
            states = list()
            for a in self.current_solution.states:
                state = None
                if random.random() < change_prob:
                    state = State(a.task, random.choice(setup.members))
                else:
                    state = State(a.task, a.member)
                
                states.append(state)
            
            solution = Solution(states)
            new_neighbours.append(solution)
        
        self.neighbours = new_neighbours
    
    def evaluate_solution(self):
        '''evaluates the fitness of all solutions
        returns the average fitness and best fitness'''
        for n in self.neighbours:
            n.fitness = fitness_checker.check_fitness(n.states)
        
        fitness = [n.fitness for n in self.neighbours]
        return np.mean(fitness), max(fitness)

    def decide_solution(self):
        '''decide which solution to take after the fitness is evaluated'''
        # get the best neighbour
        # check if it is a better solution in the current solution
        # if yes, ie best neighbour fitness > current best fitness, always accept the better solution
        # if no, ie best neighbour fitness < current best fitness, ask god whether to accept it or not
        
        # since the algorithm is trying to maximize the fitness of solution
        # when is worse solution is found, the diff should be < 0
        # therefore we need to use current fitness - new fitness

        best_neighbour = max(self.neighbours, key=lambda x: x.fitness)
        diff = self.current_solution.fitness - best_neighbour.fitness
        accept_prob = np.exp(-diff/self.temperature)
        if random.random() < accept_prob:
            # when diff > 0, the new solution is worse than the current solution
            if diff > 0:
                print("God has accepted the worse solution")

            # when diff < 0, the new solution is better than the current solution
            elif diff < 0:
                print("New best found!")
            
            self.current_solution = best_neighbour

        # recording the best fitness
        if len(self.best_fit) == 0:
            self.best_fit.append(self.current_solution.fitness)
        else:
            current_best = self.best_fit[-1]
            if current_best < self.current_solution.fitness:
                self.best_fit.append(self.current_solution.fitness)
            else:
                self.best_fit.append(current_best)
        
    def record_fitness(self, average_fitness: float, best_fitness: float):
        '''record the average fitness and best fitness'''
        self.average_fit.append(average_fitness)
        if len(self.best_fit) == 0:
            self.best_fit.append(best_fitness)
        else:
            self.best_fit.append(best_fitness if best_fitness > self.best_fit[-1] else self.best_fit[-1])

initial_solution = Solution(setup.assignments)
def run(max_iteration: int = 800, enable_visuals: bool = True) -> tuple:
    sa = SimulatedAnnealing(initial_solution, initial_temperature=10000, cd=0.99, total_neighbour=100)
    while sa.iteration <= max_iteration:
        sa.create_neighbour_solution()
        average_fitness, best_fitness = sa.evaluate_solution()
        sa.decide_solution()
        sa.cooldown()
        sa.record_fitness(average_fitness, best_fitness)
        
        print(f"SA | Iteration {sa.iteration} | temperature={sa.temperature:.8f} | Average fitness:{average_fitness:.4f} | Best fit: {sa.best_fit[-1]:.4f}")
        sa.iteration += 1

    if enable_visuals: 
        plt.plot(sa.average_fit)
        plt.show()

        new_solution: Project = Project(setup.project.name, sa.current_solution.states)
        difference_checker.print_comparison(setup.project, new_solution)

    return sa.average_fit, sa.best_fit

# run()