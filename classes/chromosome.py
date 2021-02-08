import random

class Chromosome:
    def __init__(self, size, genes = []):
        self.size = size
            
        self.genes = []

        if len(genes) == 0:
            for _ in range(self.size):
                self.genes.append(random.randint(0, self.size - 1))
        else:
            self.genes = genes

    def get_size(self):
        return self.size

    def get_gen(self, index):
        return self.genes[index]

    def get_genes(self):
        return self.genes

    def perform_mutation(self, probability = 0.5):
        if self.size > 0:
            prob = random.uniform(0, 1)

            if prob <= probability:
                for i in range(self.size):
                    mutatedGen = random.randint(0, self.size - 1)

                    while mutatedGen == self.genes[i]:
                        mutatedGen = random.randint(0, self.size - 1)

                    self.genes[i] = mutatedGen
    
    def output(self):
        return {
            'seed': self.seed,
            'genes': self.genes
        }
                