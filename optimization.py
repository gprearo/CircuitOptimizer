import numpy as np
import copy
import random
from simulation import SimulationExtractor
from netlist import CircuitEditor


class Member:

    def __init__(self, inputs_info, outputs_info, member_id):
        self.inputs_info = inputs_info
        self.outputs_info = outputs_info
        self.member_id = member_id
        self.inputs = dict()
        self.outputs = dict()
        self.fitness = 0
        self.init()

    def init(self):
        for key, value in self.inputs_info.items():
            self.inputs[key] = np.random.uniform(value['inf_limit'], value['sup_limit'])

        for key, value in self.outputs_info.items():
            self.outputs[key] = np.random.uniform(0, 10)

    def to_string(self):
        s = "Inputs:\n"
        for key, value in self.inputs.items():
            s = s + key + ":" + str(value) + "; "

        s = s + "\nOutputs:\n"
        for key, value in self.outputs.items():
            s = s + key + ":" + str(value) + "; "

        return s


class GeneticAlgorithm:

    def __init__(self, pop_count, num_gen, inputs_info, outputs_info):
        self.pop_count = pop_count
        self.num_gen = num_gen
        self.inputs_info = inputs_info
        self.outputs_info = outputs_info
        self.fitness_values = []
        self.population = []
        self.best_members = []

    def init_pop(self):
        for i in range(self.pop_count):
            member = Member(self.inputs_info, self.outputs_info, i)
            self.population.append(member)

    def evaluation(self):
        #ce = CircuitEditor("latch.cir")
        #file_lst = ce.write_all_circuits([m.inputs for m in self.population])
        #se = SimulationExtractor(file_lst)
        #result_lst = se.get_all_results()
        for i in range(self.pop_count):
            tempo = i + 1
            potencia = i + 1
            aux = {'COOUT_TEMPO': tempo, 'COOUT_POT': potencia}
            self.population[i].outputs = aux #result_lst[i]

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
        for key, value in member.outputs.items():
            fitness_val = fitness_val + GeneticAlgorithm.score(value, self.outputs_info[key])

        fitness_val = 1/fitness_val if fitness_val != 0 else float('inf')
        member.fitness = fitness_val
        return fitness_val

    def calculate_all_fitness(self):
        self.fitness_values = []
        for m in self.population:
            self.fitness_values.append(self.fitness(m))
        self.fitness_values = np.array(self.fitness_values)
        self.best_members.append(copy.copy(self.population[int(np.argmax(self.fitness_values))]))

    def print_pop(self):
        for m in self.population:
            print(m.to_string())

    # TODO crossover function
    def crossover(self):
        best_member = self.population[int(np.argmax(self.fitness_values))]
        for i in range(self.pop_count):
            for key, value in self.population[i].inputs.items():
                self.population[i].inputs[key] = (self.population[i].inputs[key] + best_member.inputs[key])/2
        return self.population[int(np.argmax(self.fitness_values))]

    # TODO mutation function
    def mutation(self):
        mutation_rate = 1/10
        best_member = (np.argmax(self.fitness_values))
        for i in range(self.pop_count):
            if i == best_member:
                pass
            else:
                mutation_chance = 100/len(self.population[i].inputs)
                for key, value in self.population[i].inputs.items():
                    if random.uniform(0, 100) < mutation_chance:
                        if random.uniform(0, 100) < 50:
                            if (self.population[i].inputs[key] + (self.population[i].inputs[key] * mutation_rate)) < self.population[i].inputs_info[key]['sup_limit']:
                                self.population[i].inputs[key] = self.population[i].inputs[key] + (self.population[i].inputs[key] * mutation_rate)
                            else:
                                self.population[i].inputs[key] = self.population[i].inputs[key] - (self.population[i].inputs[key] * mutation_rate)
                        else:
                            if (self.population[i].inputs[key] + (self.population[i].inputs[key] * mutation_rate)) < self.population[i].inputs_info[key]['inf_limit']:
                                self.population[i].inputs[key] = self.population[i].inputs[key] - (self.population[i].inputs[key] * mutation_rate)
                            else:
                                self.population[i].inputs[key] = self.population[i].inputs[key] + (self.population[i].inputs[key] * mutation_rate)

if __name__ == "__main__":
    ga = GeneticAlgorithm(6, 10, {'COIN_X1': {'sup_limit': 50, 'inf_limit': 1},
                                  'COIN_X2': {'sup_limit': 50, 'inf_limit': 1},
                                  'COIN_X3': {'sup_limit': 50, 'inf_limit': 1}},
                          {'COOUT_TEMPO': {'type': 'single-slope', 'slope': 3e9},
                           'COOUT_POT': {'type': 'single-slope', 'slope': 1e3}})
    ga.init_pop()
    ga.evaluation()
    ga.calculate_all_fitness()
    print(ga.fitness_values)
    print(ga.crossover())
    print(ga.mutation())
    print(ga.best_members[0].outputs)
