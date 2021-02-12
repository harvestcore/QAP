from classes.population import Population

if __name__ == '__main__':
    p = Population(database='databases/tai256c.dat', generations=10, variant='baldwinian')
    p.run()
    print(p)
