from models.assignment import Assignment
from models.project import Project
import setup
import fitness_checker
import random
import numpy as np
from matplotlib import pyplot as plt
import difference_checker

class Node(Assignment):
    '''represent a node taken choosen by the ant'''
    def __init__(self, task, member):
        super().__init__(task, member)
        self.pheromone = 1

class Ant:
    '''represent an ant in the colony'''
    def __init__(self):
        self.nodes: list[Node] = list()
        self.fitness = 0

    def explore(self, nodes: list[Node]):
        '''explore and choose the node
        
        leaves pheromones on the node'''
        path = list()
        for t in setup.tasks:
            valid_nodes: list[Node] = [n for n in nodes if n.task == t]
            
            # calculating the probabilitiy of choosing a node to explore 
            sum_of_pheromone = sum([n.pheromone for n in valid_nodes])
            probability = [n.pheromone/sum_of_pheromone for n in valid_nodes]
            
            # choose node based on probability
            choosen_node = random.choices(valid_nodes, probability)
            
            path.append(choosen_node[0])

        self.nodes = path
    
    def leave_pheromone(self, rank: int):
        '''leaves pheromone on the choosen nodes'''
        # using ranking as pheromone value, because sometimes ant may have fitness of 0
        for n in self.nodes:
            n.pheromone += 1/rank


class ACO:
    def __init__(self, population: int = 100, evaporate: float = 0.2):
        self.population = population
        self.evaporate = 1 - evaporate
        self.iteration = 1
        self.ants = [Ant() for i in range(self.population)]
        self.path_nodes = self.initilize_path_nodes()

        self.best = None
        self.record = list()

    def initilize_path_nodes(self) -> list[Node]:
        '''generates all possible node'''
        nodes = list()
        for t in setup.tasks:
            for m in setup.members:
                node = Node(t, m)
                nodes.append(node)
        
        return nodes

    def evaluate_fitness(self):
        '''evaluates the fitness of each ant'''        
        for a in self.ants:
            a.fitness = fitness_checker.check_fitness(a.nodes)

    def update_pheromone(self, top: float = 0.6):
        '''updates the pheromone'''
        # only allowing top ranking ants to leave pheromone
        self.ants.sort(key=lambda x: x.fitness, reverse=True)
        top_ranking_ants = self.ants[:int(len(self.ants) * top)]

        for rank, a in enumerate(top_ranking_ants):
            a.leave_pheromone(rank+1)
            
        # evaporates the pheromone of each node
        for n in self.path_nodes:
            n.pheromone *= self.evaporate

        # recording the best ant
        if self.iteration == 1:
            self.best = top_ranking_ants[0]
        elif top_ranking_ants[0].fitness > self.best.fitness:
            print(f"new best found! {self.best.fitness}->{top_ranking_ants[0].fitness}")
            self.best = top_ranking_ants[0]


aco = ACO(population=100, evaporate=0.01)
max_iteration = 800
while aco.iteration <= max_iteration:
    for a in aco.ants:
        a.explore(aco.path_nodes)
    
    aco.evaluate_fitness()
    aco.update_pheromone(top=0.1)
    
    average_fitness = np.mean([a.fitness for a in aco.ants])
    print(f"iteration {aco.iteration} | Average fitness: {average_fitness:.4f}")
    aco.record.append(average_fitness)

    aco.iteration += 1
    
plt.plot(aco.record)
plt.show()

new_solution: Project = Project(setup.project.name, aco.best.nodes)
difference_checker.print_comparison(setup.project, new_solution)