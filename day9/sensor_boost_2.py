from utils.growing_list import GrowingList
from utils.utils import load_input_file

computer_init = [int(code) for code in load_input_file(9).readline().split(",")]


def run_program(computer: GrowingList, inputs: list, outputs: list):
    index = 0
    relative_offset = 0

    while True:
        opcode, first_mode, second_mode, third_mode = parse_operation(
            "{0:05d}".format(computer[index])
        )

        if opcode not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]:
            raise ValueError("Intcode computer failed. Diagnostic incomplete...")

        if opcode == 99:
            break

        # Get indexes epending on the mode
        first_idx = (
            relative_offset + computer[index + 1]
            if first_mode == 2
            else computer[index + 1]
        )
        second_idx = (
            relative_offset + computer[index + 2]
            if second_mode == 2
            else computer[index + 2]
        )
        third_idx = (
            relative_offset + computer[index + 3]
            if third_mode == 2
            else computer[index + 3]
        )

        # Get parameter values depending on the mode
        first_param = first_idx if first_mode == 1 else computer[first_idx]

        if opcode in [1, 2, 5, 6, 7, 8]:
            second_param = second_idx if second_mode == 1 else computer[second_idx]

        # Execute operation
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
        elif opcode == 9:
            relative_offset += first_param

        if opcode in [1, 2, 7, 8]:
            index += 4
        elif opcode in [3, 4, 9]:
            index += 2
        else:
            index += 3


def parse_operation(operation: str):
    return (
        int(operation[-2:]),
        int(operation[-3]),
        int(operation[-4]),
        int(operation[-5]),
    )


OUTPUTS = []
run_program(GrowingList(computer_init.copy()), [2], OUTPUTS)

print("Distress signal coordinates are {}".format(OUTPUTS[-1]))