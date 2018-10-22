import re
import _thread


class CircuitEditor:

    def __init__(self, filename):
        self.filename = filename
        self.src_file = open(filename, "r")
        self.src_circuit = self.src_file.read()
        self.src_file.close()

    def replace_params(self, dic, dst_filename):

        #  Replaces every param to be replaced on circuit file
        circuit = ""
        for key, value in dic.items():
            search_term = r'.param\s+' + key + '\s*=\s*\'(.*)\''
            replace_term = r".param " + key + "= '" + str(value) + "'"
            circuit = re.sub(search_term, replace_term, self.src_circuit)

        # Saves the circuit with replaced parameters
        dst_file = open(dst_filename, "w")
        dst_file.write(circuit)
        dst_file.close()

    def write_all_circuits(self, dic_list):
        for i in range(len(dic_list)):
            _thread.start_new_thread(self.replace_params, (dic_list[i], self.filename+"_" + str(i)))
