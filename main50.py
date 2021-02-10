from classes.population import Population

if __name__ == '__main__':
    p = Population(database='databases/tai256c.dat', generations=50)
    p.run()
    print(p)

    p1 = Population(database='databases/tai256c.dat', generations=50, variant='lamarckian')
    p1.run()
    print(p1)

    p2 = Population(database='databases/tai256c.dat', generations=50, variant='baldwinian')
    p2.run()
    print(p2)

# print(len(p.distances))
# print(p.distances)
# print(p.flows)
