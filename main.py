from classes.population import Population

p = Population(database='databases/bur26a.dat', generations=100)
p.run()
print(p)

p1 = Population(database='databases/bur26a.dat', generations=100, variant='lamarckian')
p1.run()
print(p1)

# print(len(p.distances))
# print(p.distances)
# print(p.flows)
