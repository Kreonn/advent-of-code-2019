from itertools import permutations

from utils.utils import load_input_file

computer_init = [int(code) for code in load_input_file(7).readline().split(",")]


def run_program(computer: list, inputs: list, outputs: list):
    index = 0

    while True:
        opcode, first_mode, second_mode = parse_operation(
            "{0:05d}".format(computer[index])
        )

        if opcode not in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
            raise ValueError("Intcode computer failed. Diagnostic incomplete...")

        if opcode == 99:
            break

        first_idx = computer[index + 1]
        second_idx = computer[index + 2]
        third_idx = computer[index + 3]

        first_param = first_idx if first_mode else computer[first_idx]

        if opcode in [1, 2, 5, 6, 7, 8]:
            second_param = second_idx if second_mode else computer[second_idx]

        if opcode == 1:
            computer[third_idx] = first_param + second_param
        elif opcode == 2:
            computer[third_idx] = first_param * second_param
        elif opcode == 3:
            computer[first_idx] = inputs.pop(0)
        elif opcode == 4:
            outputs.append(first_param)
        elif opcode == 5:
            if first_param != 0:
                index = second_param
                continue
        elif opcode == 6:
            if first_param == 0:
                index = second_param
                continue
        elif opcode == 7:
            computer[third_idx] = 1 if first_param < second_param else 0
        elif opcode == 8:
            computer[third_idx] = 1 if first_param == second_param else 0

        if opcode in [1, 2, 7, 8]:
            index += 4
        elif opcode in [3, 4]:
            index += 2
        else:
            index += 3


def parse_operation(operation: str):
    return int(operation[-2:]), operation[-3] == "1", operation[-4] == "1"


OUTPUTS = [0]

max_thruster_signal = 0

for phase_sequence in list(permutations(range(5), 5)):
    try:
        for phase in phase_sequence:
            run_program(computer_init.copy(), [phase, OUTPUTS.pop(0)], OUTPUTS)

        if OUTPUTS[0] > max_thruster_signal:
            max_thruster_signal = OUTPUTS[0]
    except Exception:
        print(
            "Something went wrong while running phase sequence {}".format(
                phase_sequence
            )
        )

    OUTPUTS = [0]


print("Max thruster signal attainable is {}".format(max_thruster_signal))
