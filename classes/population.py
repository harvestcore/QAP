import uuid
import random
import sys

from .chromosome import Chromosome

VARIANTS = ['standard', 'lamarckian', 'baldwinian']

class Population:
    # Number of chromosomes
    size = 0

    # Path where the data is stored
    database = ''

    # Flows and distances
    flows = []
    distances = []

    # Ratio of best elements to be taken in mind when reproducing
    best_chromosomes_ratio = 0.1
    
    # Array of dictionaries.
    # Each dict contains:
    # { ch: chromosome, fitness: its fitness value }
    fitness = []
    
    def __init__(self, database, variant='standard', generations=100, mutation_probability=0.5, cross_probability=0.5, gene_mutations=2, seed=None):
        # Algorithm iterations.
        self.iterations = 0

        self.variant = variant if variant in VARIANTS else 'regular'

        self.best_chromosome = { 'fitness': sys.maxsize }

        # Generations management.
        self.generations = generations

        # Database management + fetch data.
        self.database = database
        self.__fetch_data_from_database()

        # Mutation and cross probabilities.
        self.mutation_probability = mutation_probability
        self.cross_probability = cross_probability

        # Genes to be mutated
        self.gene_mutations = gene_mutations

        # Seed management.
        self.seed = uuid.uuid4() if seed is None else uuid.UUID(seed)
        random.seed(self.seed)

        # Generate first chromosomes.
        self.chromosomes = [Chromosome(size=self.size, gene_mutations=self.gene_mutations) for _ in range(self.size)]

    def __fetch_data_from_database(self):
        with open(self.database) as file:
            content = file.readlines()
            self.size = int(content[0].strip())

            for i in range(2, self.size + 2):
                line = content[i].replace('\n', '')
                splitted = list(filter(None, line.split(' ')))
                self.flows.append([int(val.replace('\n', '')) for val in splitted])

            for i in range(self.size + 3, (self.size * 2) + 3):
                line = content[i].replace('\n', '')
                splitted = list(filter(None, line.split(' ')))
                self.distances.append([int(val.replace('\n', '')) for val in splitted])

    def __compute_fitness_by_chromosome(self, chromosome):
        fitness = 0.0
        
        for i in range(self.size):
            for j in range(self.size):
                fitness += self.flows[i][j] * self.distances[chromosome.get_gen(i)][chromosome.get_gen(j)]

        return fitness

    def compute_all_chromosomes_fitness(self):
        # Compute the fitness of all chromosomes.
        fitness = [{
                'ch': ch,
                'fitness': self.__compute_fitness_by_chromosome(ch)
            } for ch in self.chromosomes]

        # Order the chromosomes by its fitness.
        self.fitness = sorted(fitness, key=lambda f: f['fitness'])

        return self.fitness

    def mutate_chromosomes(self):
        for ch in self.chromosomes:
            ch.perform_mutation(self.mutation_probability)

    def reproduce_chromosomes(self):
        if random.uniform(0, 1) < self.cross_probability:
            # Possible best chromosomes.
            pbc = self.size * self.best_chromosomes_ratio

            # Ensure that the possible best chromosomes are at least 2.
            pbc = int(pbc if pbc >= 2 else 2)

            # Array with the best chromosomes.
            best_chs = self.fitness[:pbc]

            # Add the first best chromosomes.
            children = [
                ch['ch'] for ch in best_chs
            ]

            for _ in range(self.size - pbc):
                # Random split point.
                split = random.randint(0, self.size - 1)

                # Get parents and join them.
                parents = random.sample(best_chs, 2)
                joined_genes = parents[0]['ch'].get_genes()[split:] + parents[0]['ch'].get_genes()[:split]

                # Child chromosome.
                child = Chromosome(
                    size=parents[0]['ch'].get_size(),
                    genes=joined_genes,
                    gene_mutations=self.gene_mutations
                )

                # Add new children.
                children.append(child)

                # Assign new chromosomes.
                self.chromosomes = children

    def compute_best_chromosome(self):
        best = sorted(self.fitness, key=lambda f: f['fitness'])[0]

        if best['fitness'] < self.best_chromosome['fitness']:
            self.best_chromosome = {
                'ch': best['ch'].get_genes(),
                'fitness': best['fitness'],
                'generation': self.iterations
            }

    def get_best_chromosome(self):
        return self.best_chromosome

    def run(self):
        for _ in range(self.generations):
            # Increment iterations.
            self.iterations += 1

            # Compute algorithm.
            self.compute_all_chromosomes_fitness()
            self.reproduce_chromosomes()
            self.mutate_chromosomes()

            # Update the best chromosome.
            self.compute_best_chromosome()

    def json(self):
        return {
            'population_size': self.size,
            'mutation_probability': self.mutation_probability,
            'cross_probability': self.cross_probability,
            'generations': self.generations,
            'seed': str(self.seed),
            # 'chromosomes': [ ch.get_genes() for ch in self.chromosomes ],
            # 'fitness': [ f['fitness'] for f in self.fitness ],
            'best_chromosome': self.get_best_chromosome()
        }

    def __str__(self):
        return str(self.json())

