from utils.utils import load_input_file

computer = [int(code) for code in load_input_file(2).readline().split(",")]

index = 0

# Code 1202 !!!
computer[1] = 12
computer[2] = 2

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

print("Program completed, final result is {}".format(computer[0]))
