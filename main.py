from classes.population import Population

p = Population(database='databases/bur26a.dat', generations=100)

p.run()

print(p)
# print(len(p.distances))
# print(p.distances)
# print(p.flows)
