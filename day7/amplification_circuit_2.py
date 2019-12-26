from itertools import permutations
from queue import SimpleQueue
from threading import Thread

from utils.utils import load_input_file

computer_init = [int(code) for code in load_input_file(7).readline().split(",")]


class IntcodeComputer(Thread):
    def __init__(self, computer: list, base_inputs: list, link=None):
        super().__init__()

        self.computer = computer
        self.link = link
        self.inputs = SimpleQueue()
        self.outputs = SimpleQueue()

        for item in base_inputs:
            self.inputs.put(item)

    def set_link(self, link):
        self.link = link

    def run(self):
        index = 0

        while True:
            opcode, first_mode, second_mode = IntcodeComputer.__parse_operation(
                "{0:05d}".format(self.computer[index])
            )

            if opcode not in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
                raise ValueError("Intcode computer failed...")

            if opcode == 99:
                break

            # Get indexes
            first_idx = self.computer[index + 1]

            if index + 2 < len(self.computer):
                second_idx = self.computer[index + 2]

            if index + 3 < len(self.computer):
                third_idx = self.computer[index + 3]

            # Get parameter values depending on the mode
            first_param = first_idx if first_mode else self.computer[first_idx]

            if opcode in [1, 2, 5, 6, 7, 8]:
                second_param = second_idx if second_mode else self.computer[second_idx]

            # Execute operation
            if opcode == 1:
                self.computer[third_idx] = first_param + second_param
            elif opcode == 2:
                self.computer[third_idx] = first_param * second_param
            elif opcode == 3:
                self.computer[first_idx] = self.get_input()
            elif opcode == 4:
                self.outputs.put(first_param)
            elif opcode == 5:
                if first_param != 0:
                    index = second_param
                    continue
            elif opcode == 6:
                if first_param == 0:
                    index = second_param
                    continue
            elif opcode == 7:
                self.computer[third_idx] = 1 if first_param < second_param else 0
            elif opcode == 8:
                self.computer[third_idx] = 1 if first_param == second_param else 0

            if opcode in [1, 2, 7, 8]:
                index += 4
            elif opcode in [3, 4]:
                index += 2
            else:
                index += 3

    def get_input(self):
        if self.inputs.empty():
            if self.link is not None:
                self.inputs.put(self.link.get_output())

        return self.inputs.get()

    def get_output(self):
        return self.outputs.get()

    @staticmethod
    def __parse_operation(operation: str):
        return int(operation[-2:]), operation[-3] == "1", operation[-4] == "1"


max_thruster_signal = 0

for phase_sequence in list(permutations(range(5, 10), 5)):
    # Create feedback loop
    accA = IntcodeComputer(computer_init.copy(), [phase_sequence[0], 0])
    accB = IntcodeComputer(computer_init.copy(), [phase_sequence[1]], link=accA)
    accC = IntcodeComputer(computer_init.copy(), [phase_sequence[2]], link=accB)
    accD = IntcodeComputer(computer_init.copy(), [phase_sequence[3]], link=accC)
    accE = IntcodeComputer(computer_init.copy(), [phase_sequence[4]], link=accD)
    accA.set_link(accE)

    accA.start()
    accB.start()
    accC.start()
    accD.start()
    accE.start()

    accA.join()
    accB.join()
    accC.join()
    accD.join()
    accE.join()

    thruster_signal = accE.get_output()

    if thruster_signal > max_thruster_signal:
        max_thruster_signal = thruster_signal


print("Max thruster signal attainable is {}".format(max_thruster_signal))
