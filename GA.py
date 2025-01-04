from models.assignment import Assignment
from models.project import Project
import setup
import fitness_checker
import random
import difference_checker
import numpy as np
from matplotlib import pyplot as plt

class Genes(Assignment):
    def __init__(self, task, member):
        super().__init__(task, member)

class Chromosomes:
    def __init__(self, genes: list[Genes]):
        self.genes: list[Genes] = genes
        self.fitness = 0
    
    def produce_bebe(self, partner: 'Chromosomes'):
        k = random.randint(1, len(self.genes) - 1)

        g1 = self.genes[:k] + partner.genes[k:]
        g2 = partner.genes[:k] + self.genes[k:]

        b1 = Chromosomes(g1)
        b2 = Chromosomes(g2)

        return b1, b2
    
class GeneticAlgoritm:
    def __init__(self, size: int = 400, mutation: float = 0.5, cross_over: float = 0.5):
        self.size = size
        self.chromosomes: list[Chromosomes] = list()
        self.generation = 1

        self.mutation = mutation
        self.cross_over = cross_over
        self.initialize_population()

        self.best:Chromosomes = None
        self.average_fit = list()
        self.best_fit = list()

    def initialize_population(self):
        for i in range(self.size):
            chromosome = Chromosomes(
                [
                    Genes(t, random.choice(setup.members)) for t in setup.tasks
                ]
            )

            self.chromosomes.append(chromosome)

    def evaluate_chromosome(self, initial_formation: Project):
        '''evaluates the fitness of the chromosomes
        returns average of fitness and the best fitness'''
        for c in self.chromosomes:
            c.fitness = fitness_checker.check_fitness(c.genes, initial_formation)

        fitness = [c.fitness for c in self.chromosomes]
        return np.mean(fitness), max(fitness)

    def eliminate_chromosome(self, top: float = 0.2):
        self.chromosomes.sort(key=lambda x: x.fitness, reverse=True)
        top_rank = int(self.size * top)
        self.chromosomes = self.chromosomes[:top_rank]

        current_best:Chromosomes = self.chromosomes[0]
        if self.generation == 1:
            self.best = current_best
        else:
            # if the current_best is better than previoud best, accept it
            if current_best.fitness > self.best.fitness:
                print(f"new best found! {self.best.fitness}->{current_best.fitness}")
                self.best = current_best
    
    def tournament_selection(self, tournament_size: int = 2, parent_num: int = 20):
        '''use tournament selection to choose parent for crossover operation'''
        winners = list()
        while len(winners) < parent_num:
            parents: list[Chromosomes] = random.sample(self.chromosomes, tournament_size)
            winner = max(parents, key=lambda x: x.fitness)
            winners.append(winner)
            self.chromosomes.remove(winner)

        self.chromosomes = winners

        current_best:Chromosomes = max(self.chromosomes, key=lambda x: x.fitness)
        if self.generation == 1:
            self.best = current_best
        else:
            # if the current_best is better than previoud best, accept it
            if current_best.fitness > self.best.fitness:
                print(f"new best found! {self.best.fitness}->{current_best.fitness}")
                self.best = current_best
    
    def produce_bebes(self):
        '''produce new bebes and make mutation'''
        # cross over operation
        bebes: list[Chromosomes] = list()
        while len(self.chromosomes) + len(bebes) < self.size:
            if random.random() < self.cross_over:
                parent_1, parent_2 = random.sample(self.chromosomes, 2)
                bebe_1, bebe_2 = parent_1.produce_bebe(parent_2)

                bebes.append(bebe_1)
                bebes.append(bebe_2)
        
        # mutation operation
        for b in bebes:
            for i, g in enumerate(b.genes):
                if random.random() < self.mutation:
                    new_member = random.choice([m for m in setup.members if m != g.member])
                    b.genes[i] = Genes(g.task, new_member)
        
        self.chromosomes += bebes
        
        # resample to make sure that the size of chromosome is equal to population size
        self.chromosomes = random.sample(self.chromosomes, self.size)

    def record_fitness(self, average_fitness: float, best_fitness: float):
        '''record the average fitness and best fitness'''
        self.average_fit.append(average_fitness)
        if len(self.best_fit) == 0:
            self.best_fit.append(best_fitness)
        else:
            self.best_fit.append(best_fitness if best_fitness > self.best_fit[-1] else self.best_fit[-1])

def run(initial_formation: Project, max_iteration: int = 800, enable_visuals:bool = True) -> tuple:
    ga = GeneticAlgoritm(100, 0.1, 0.9)
    while ga.generation <= max_iteration:
        average_fitness, best_fitness = ga.evaluate_chromosome(initial_formation)
        ga.tournament_selection(tournament_size=4, parent_num=80)
        ga.produce_bebes()

        ga.record_fitness(average_fitness, best_fitness)
        print(f"GA | Generation: {ga.generation} | Population: {len(ga.chromosomes)} | Average fitness: {average_fitness:.4f} | Best fit: {ga.best_fit[-1]:.4f}")
        ga.generation += 1

    if enable_visuals:
        plt.plot(ga.average_fit)
        plt.show()

        new_solution: Project = Project(setup.project.name, ga.best.genes)
        difference_checker.print_comparison(setup.project, new_solution)

    return ga.average_fit, ga.best_fit