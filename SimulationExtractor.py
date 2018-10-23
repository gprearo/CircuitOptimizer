import subprocess
import os


class SimulationExtractor:

    def __init__(self, file_list):
        self.file_list = file_list

    @staticmethod
    def simulate(file):
        init_eldo = "C:\\Windows\\SysWOW64\\cmd.exe /k \"\"D:\\WinPrograms\\AMS_16_2_patch3_win64\\bin\\ams_setup.bat" \
                    "\" \"D:\\WinPrograms\\AMS_16_2_patch3_win64\" eldo -help\""
        proc = subprocess.Popen(init_eldo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = proc.communicate('eldo "' + os.getcwd() + '\\' + file + '"\n')

        return stdout


    @staticmethod
    def get_sim_results(sim_output):
        pass


def main():
    out = SimulationExtractor.simulate("latch.cir")
    print(out)
    file_out = open("out", "w")
    file_out.write(out)
    file_out.close()


if __name__ == "__main__":
    main()
