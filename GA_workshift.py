from models.assignment import Assignment
from models.job import Job
from models.team import Team
from helpers import helper
import random
import numpy as np
from matplotlib import pyplot as plt

class Gene(Assignment):
    def __init__(self, j: Job, t: Team) -> None:
        super().__init__(j, t)

class Chromosome:
    def __init__(self, genes: list) -> None:
        self.genes = genes
        self.fitness = 0
        self.make_span = 0
    
    def cross_over(self, partner: 'Chromosome') -> 'Chromosome':
        """
        produce new chromosome using a single point cross over
        """

        # some assert check to make sure that all things are correct
        # making sure that the length of genes are the same
        assert len(self.genes) == len(partner.genes)
        for s, p in zip(self.genes, partner.genes):
            # make sure the job object is the same
            assert s.job == p.job, f"{s.job.name} is not {p.job.name}"
        
        # choosing a random point for cross over
        random_point = random.randint(1, len(self.genes) - 1)

        # slicing genes from self and partner
        upper_gene = self.genes[:random_point]
        lower_gene = partner.genes[random_point:]
        comb_gene = upper_gene + lower_gene

        # extracting the job and team from original genes
        # create a new gene object from it
        bebe_gene = []
        g: Gene
        for g in comb_gene:
            new_gene = Gene(g.job, g.team)
            bebe_gene.append(new_gene)

        # some assertion check again to make sure things are correct
        for s, b in zip(self.genes, bebe_gene):
            assert s.job == b.job

        bebe = Chromosome(bebe_gene)
        return bebe

class Population:
    def __init__(self, jobs: list, teams: list, size: int, top: float = 0.5, cross_over_rate: float = 0.95, mutation_rate: float = 0.1):
        """
        represent a population of chromosome
        
        use high cross over rate, and low mutation rate
        """
        self.generation = 1
        self.size = size
        self.chromosomes = []

        # list of teams and jobs
        self.jobs = jobs
        self.teams = teams
        
        self.top = top
        self.cross_over_rate = cross_over_rate
        self.mutation_rate = mutation_rate

        self.previous_high = 0
        self.previous_low = 0
        # storing the best solution
        self.best = None

        self.hist = []

    def generate_chromosomes(self, amount: int):
        """
        generate chromosomes based on the amount specified
        """
        for i in range(amount):
            genes = []
            j: Job
            for j in self.jobs:
                choosen_team = random.choice(self.teams)
                new_gene = Gene(j, choosen_team)
                genes.append(new_gene)

            new_chromosome = Chromosome(genes)
            self.chromosomes.append(new_chromosome)
        

    def evaluate_chromosome(self):
        """
        evaluates the fitness of the chromosome
        """
        c: Chromosome
        for c in self.chromosomes:
            # fitness in terms of make span
            t, make_span = helper.calculate_make_span(c.genes)
            c.make_span = make_span
            c.fitness = make_span

        current_best = min(self.chromosomes, key=lambda x: x.fitness)
        
        if self.generation == 1:
            self.best = current_best
            print("New best found!")
        else:
            if current_best.fitness < self.best.fitness:
                self.best = current_best              
                print("New best found!")
        
        self.hist.append(np.mean([c.make_span for c in self.chromosomes]))              

    def eliminate_chromosome(self):
        """
        eliminates the chromosome, choose the chromosomes that are to the top percentage
        """
        before = len(self.chromosomes)
        
        self.chromosomes.sort(key=lambda x: x.fitness, reverse=True)
        # selecting the top percent of chromosome
        top = int(before * self.top)
        self.chromosomes = self.chromosomes[top:]
        
        after = len(self.chromosomes)
        print(f"eliminated {before - after} chromosomes")


    def tournament(self, p1:Chromosome, p2:Chromosome):
        return p1 if p1.fitness > p2.fitness else p2

    def produce_bebe(self):
        """
        cross over operation using tournament selection
        
        then randomly mutate the gene of the bebe produced
        """
        bebes = []
        for i in range(self.size):
            if random.random() < self.cross_over_rate:
                competitors = random.sample(self.chromosomes, 4)
                for c1, c2, c3, c4 in [competitors]:
                    p1 = self.tournament(c1, c2)
                    p2 = self.tournament(c3, c4)

                    bebe_1 = p1.cross_over(p2)
                    bebe_2 = p2.cross_over(p1)

                    bebes += [bebe_1, bebe_2]

        # mutate the genes in the bebe
        b: Chromosome
        for b in bebes:
            g: Gene
            for g in b.genes:
                if random.random() < self.mutation_rate:
                    g.team = random.choice(self.teams)

        self.chromosomes += bebes

        # check if the population is less than the population size stated
        # else sample the population size needed only
        if len(self.chromosomes) > self.size:
            self.chromosomes = random.sample(self.chromosomes, self.size)
        # else:
        #     # just produce some copy of existing chromosome to make up the number of chromosome
        #     while len(self.chromosomes) < self.size:
        #         random_chromosome = random.choice(self.chromosomes)
        #         new_chromosome = Chromosome(random_chromosome.genes)
        #         self.chromosomes.append(new_chromosome)



def run() -> Chromosome:
    jobs = helper.create_random_jobs(10)
    teams = helper.create_random_team(5)
    population = Population(jobs, teams, 500, cross_over_rate=0.95, mutation_rate=0.2)
    population.generate_chromosomes(population.size)
    
    while population.generation <= 200:
        print(f"Generation {population.generation} | population: {len(population.chromosomes)}")
        population.evaluate_chromosome()
        population.eliminate_chromosome()
        population.produce_bebe()
        population.generation += 1

    plt.plot(population.hist)
    plt.show()

    return population.best
