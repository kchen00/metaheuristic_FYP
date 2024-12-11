from models.assignment import Assignment
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

        self.record = list()

    def initialize_population(self):
        for i in range(self.size):
            chromosome = Chromosomes(
                [
                    Genes(t, random.choice(setup.members)) for t in setup.tasks
                ]
            )

            self.chromosomes.append(chromosome)

    def evaluate_chromosome(self):
        for c in self.chromosomes:
            c.fitness = fitness_checker.check_fitness(c.genes)

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
    
    def produce_bebes(self):
        # cross over operation
        bebes: list[Chromosomes] = list()
        while len(self.chromosomes) + len(bebes) < self.size:
            if random.random() < self.cross_over:
                parent_1 = self.best
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

ga = GeneticAlgoritm(200, 0.5, 0.99)
max_iteration = 1000
while ga.generation <= max_iteration:
    ga.evaluate_chromosome()
    ga.eliminate_chromosome(0.6)
    ga.produce_bebes()

    average_fitness = np.mean([c.fitness for c in ga.chromosomes])
    print(f"Generation: {ga.generation} | Population: {len(ga.chromosomes)} | Average fitness: {average_fitness:.4f}")
    ga.record.append(ga.best.fitness)

    ga.generation += 1

plt.plot(ga.record)
plt.show()

print(ga.best)
for g in ga.best.genes:
    print(f"{g.task.name} -> {g.member.name}", [a.member.name for a in setup.project.assignments if (a.task == g.task and a.member != g.member)])
difference_checker.check_difference(ga.best.genes)