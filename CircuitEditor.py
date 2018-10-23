import re
import threading
import numpy as np


class CircuitEditor:

    input_token = "COIn_"

    def __init__(self, filename):
        self.filename = filename
        self.src_file = open(filename, "r")
        self.src_circuit = self.src_file.read()
        self.src_file.close()

    def replace_params(self, dic, dst_filename):
        #  Replaces every param to be replaced on circuit file
        circuit = self.src_circuit
        for key, value in dic.items():
            search_term = r'.param\s+' + key + '\s*=\s*\'.*\''
            replace_term = r".param " + key + "= '" + str(value) + "'"
            circuit = re.sub(search_term, replace_term, circuit, flags=re.IGNORECASE)

        # Saves the circuit with replaced parameters
        dst_file = open(dst_filename, "w")
        dst_file.write(circuit)
        dst_file.close()

    def write_all_circuits(self, dic_list):
        threads = []
        files = []
        for i in range(len(dic_list)):
            # Generate the filename for this circuit, which is the first part of
            # the original filename plus underscore plus thread number plus ".cir"
            thr_filename = self.filename.split(".")[0] + "_" + str(i) + ".cir"
            files.append(thr_filename)

            # Create the thread to generate the circuit file
            t = threading.Thread(target=self.replace_params, args=(dic_list[i], thr_filename))
            threads.append(t)
            t.start()

        # Return the name of all files generated
        return files

    def get_params(self):
        # Search for parameters starting with the input token (COIn_)
        return re.findall('\.param\s+(' + self.input_token + '.+)\s*=\s*\'.*\'', self.src_circuit, re.IGNORECASE)


def main():
    ce = CircuitEditor("latch.cir")
    params = ce.get_params()
    num_member = 10

    population = []
    for i in range(num_member):
        dic = {}
        for param in params:
            dic[param] = np.random.uniform(0, 10)
        population.append(dic)

    print(population)
    ce.write_all_circuits(population)


if __name__ == "__main__":
    main()
