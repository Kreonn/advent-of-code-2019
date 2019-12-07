from utils.utils import load_input_file

computer_init = [int(code) for code in load_input_file(2).readline().split(",")]
awaited_result = 19690720


def run_program(computer, noun, verb):
    index = 0

    computer[1] = noun
    computer[2] = verb

    while True:
        opcode = computer[index]

        if opcode not in [1, 2, 99]:
            raise ValueError("Drift away in space forever...")

        if opcode == 99:
            break

        operand1 = computer[computer[index + 1]]
        operand2 = computer[computer[index + 2]]
        result_idx = computer[index + 3]

        if opcode == 1:
            computer[result_idx] = operand1 + operand2
        else:
            computer[result_idx] = operand1 * operand2

        index += 4

    return computer[0]


for noun in range(0, 100):
    for verb in range(0, 100):
        result = run_program(computer_init.copy(), noun, verb)

        if result == awaited_result:
            print(
                "Program completed, gravity assist code is {}".format(100 * noun + verb)
            )
            exit(0)
