import numpy as np
import random


class Member:

    def __init__(self, inputs_info, outputs_info, member_id):
        self.inputs_info = inputs_info
        self.outputs_info = outputs_info
        self.member_id = member_id
        self.inputs = dict()
        self.outputs = dict()
        self.init()

    def init(self):
        np.random.seed(self.member_id)
        for key, value in self.inputs_info.items():
            self.inputs[key] = random.random()*(value['sup_limit']-value['inf_limit'])+value['inf_limit']

        for key, value in self.outputs_info.items():
            self.outputs[key] = 0.0

    def to_string(self):
        s = "Inputs:\n"
        for key, value in self.inputs.items():
            s = s + key + ":" + str(value) + "; "

        s = s + "\nOutputs:\n"
        for key, value in self.outputs.items():
            s = s + key + ":" + str(value) + "; "

        return s


class GeneticAlgorithm:
    fitness_values = []
    population = []

    def __init__(self, pop_count, num_gen, inputs_info, outputs_info):
        self.pop_count = pop_count
        self.num_gen = num_gen
        self.inputs_info = inputs_info
        self.outputs_info = outputs_info

    def init_pop(self):
        np.random.seed(0)
        for i in range(self.pop_count):
            member = Member(self.inputs_info, self.outputs_info, i)
            self.population.append(member)

    @staticmethod
    def score(val, score_curve):
        if score_curve['type'] == 'V-shape':
            if val <= score_curve['zero']:
                return score_curve['slope1']*(val - score_curve['zero'])
            else:
                return score_curve['slope2']*(score_curve['zero'] - val)
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
        for key, value in member.outputs:
            fitness_val = fitness_val + GeneticAlgorithm.score(value, self.outputs_info[key])

        return fitness_val

    def calculate_all_fitness(self):
        self.fitness_values = []
        for m in self.population:
            self.fitness_values.append(self.fitness(m))

    def print_pop(self):
        for m in self.population:
            print(m.to_string())
    # TODO crossover function

    # TODO mutation function


if __name__ == "__main__":
    np.random.seed(1)
    ga = GeneticAlgorithm(5, 10, {'in1': {'sup_limit': 10, 'inf_limit': 3}, 'in2': {'sup_limit': 19, 'inf_limit': 8}},
                          {'out1': 0, 'out2': 1})
    ga.init_pop()
    ga.print_pop()
    print(ga.population)
