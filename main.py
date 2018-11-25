from optimization import GeneticAlgorithm
import matplotlib.pyplot as plt


pop_count = 25
gen_count = 50

ga = GeneticAlgorithm(pop_count, gen_count, {'COIN_X1': {'sup_limit': 100, 'inf_limit': 1},
                                             'COIN_X2': {'sup_limit': 100, 'inf_limit': 1},
                                             'COIN_X3': {'sup_limit': 100, 'inf_limit': 1}},
                      {'COOUT_TEMPO': {'type': 'single-slope', 'slope': 3e9},
                       'COOUT_POT': {'type': 'single-slope', 'slope': 4e3}})
ga.init_pop()
for i in range(gen_count):
    print("Running generation {}".format(i))
    ga.evaluation()
    ga.calculate_all_fitness()
    if i > 5:
        if sum(ga.best_fitness[-5:])/5 == ga.best_fitness[-1]:
            break
    ga.crossover()
    ga.mutation()

log_file = open("log.txt", 'w')
for m in ga.best_members:
    log_file.write(m.to_string())
    log_file.write("\n")

log_file.close()

fig, ax = plt.subplots()
print(ga.best_fitness)
ax.plot(ga.best_fitness)
fig.suptitle('Fitness do melhor individuo por geração')
plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.show()
