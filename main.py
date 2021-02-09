from classes.population import Population

# p = Population(database='databases/tai256c.dat', generations=50)
p1 = Population(database='databases/tai256c.dat', generations=125)
p1.run()
print(p1)

# p = Population(database='databases/chr12a.dat', generations=1, variant='baldwinian')
# p.run()
# print(p)


# print(len(p.distances))
# print(p.distances)
# print(p.flows)
