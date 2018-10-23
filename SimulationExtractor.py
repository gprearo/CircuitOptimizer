import subprocess
import os
import re


class SimulationExtractor:

    def __init__(self, file_list):
        self.file_list = file_list

    @staticmethod
    def simulate(file):
        # Initialize eldo
        init_eldo = "C:\\Windows\\SysWOW64\\cmd.exe /k \"\"D:\\WinPrograms\\AMS_16_2_patch3_win64\\bin\\ams_setup.bat" \
                    "\" \"D:\\WinPrograms\\AMS_16_2_patch3_win64\" eldo -help\""
        proc = subprocess.Popen(init_eldo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

        # Simulate
        stdout, stderr = proc.communicate('eldo "' + os.getcwd() + '\\' + file + '"\n')

        return stdout

    @staticmethod
    def get_sim_results(sim_output):
        find_term = "(?=Simulation completed)*([^\s]+)\s*=\s*([^\s]*)\s*"
        result = re.findall(find_term, sim_output, re.IGNORECASE)
        return result


def main():
    results = SimulationExtractor.get_sim_results("Simulation completed\n\nTEMPO         =  3.658768E-10" \
                                                  "\nTAU           =  4.23487E-3)")
    print(results)
    result_list = []
    for result in results:
        dic = dict()
        dic[result[0]] = result[1]
        result_list.append(dic)

    print(result_list)


if __name__ == "__main__":
    main()
