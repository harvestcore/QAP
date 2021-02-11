from classes.population import Population

if __name__ == '__main__':
    p = Population(database='databases/tai256c.dat',
        population_size=10,
        generations=5,
        variant='lamarckian',
        mutation_probability=0.5,
        cross_probability=0.5,
        gene_mutations=2,
        best_chromosomes_ratio=0.3)
    p.run()
    print(p)
