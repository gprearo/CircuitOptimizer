import numpy as np

class GeneticAlgorithm:
    fitness_values = []
    population = []

    def __init__(self, pop_count, num_gen, curves):
        self.pop_count = pop_count
        self.num_gen = num_gen
        self.curves = curves

    def init_pop(self):
        for i in range(self.pop_count) :
            member = dict()
            for key, value in self.curves.items():
                member[key] = np.rand()*(value['sup_limit']*value['inf_limit'])+value['inf_limit']
            self.population.append(member)

    @staticmethod
    def score(val, score_curve):
        if score_curve['type'] == 'V-shape':
            if val <= score_curve['zero'] :
                return score_curve['slope1']*(val - score_curve['zero'])
            else:
                return score_curve['slope2']*(score_curve['zero']-val)
        elif score_curve['type'] == 'range':
            if val < score_curve['zero1']:
                return score_curve['slope1']*(val - score_curve['zero1'])
            elif val > score_curve['zero2']:
                return score_curve['slope2']*(score_curve['zero2'] - val)
            else:
                return 0
        elif score_curve['type'] == 'single-slope':
            return val*score_curve['slope']
        return 0

    def fitness(self, member):
        fitness_val = 0
        for key, value in member.items():
            fitness_val = fitness_val + GeneticAlgorithm.score(value, self.curves[key])

        return fitness_val

    def calculate_all_fitness(self):
        self.fitness_values = []
        for m in self.population:
            self.fitness_values.append(self.fitness(m))

    # TODO crossover function

    # TODO mutation function
    
