from queue import SimpleQueue
from threading import Thread

from utils.growing_list import GrowingList
from utils.utils import load_input_file

computer_init = [int(code) for code in load_input_file(13).readline().split(",")]


class Computer(Thread):
    def __init__(self, computer_init: list):
        super().__init__()

        self.program = GrowingList(computer_init.copy())
        self.inputs = SimpleQueue()
        self.outputs = SimpleQueue()

    def run(self):
        index = 0
        relative_offset = 0

        while True:
            opcode, first_mode, second_mode, third_mode = Computer.parse_operation(
                "{0:05d}".format(self.program[index])
            )

            if opcode not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]:
                raise ValueError("Intcode computer failed. Diagnostic incomplete...")

            if opcode == 99:
                break

            # Get indexes epending on the mode
            first_idx = (
                relative_offset + self.program[index + 1]
                if first_mode == 2
                else self.program[index + 1]
            )
            second_idx = (
                relative_offset + self.program[index + 2]
                if second_mode == 2
                else self.program[index + 2]
            )
            third_idx = (
                relative_offset + self.program[index + 3]
                if third_mode == 2
                else self.program[index + 3]
            )

            # Get parameter values depending on the mode
            first_param = first_idx if first_mode == 1 else self.program[first_idx]

            if opcode in [1, 2, 5, 6, 7, 8]:
                second_param = (
                    second_idx if second_mode == 1 else self.program[second_idx]
                )

            # Execute operation
            if opcode == 1:
                self.program[third_idx] = first_param + second_param
            elif opcode == 2:
                self.program[third_idx] = first_param * second_param
            elif opcode == 3:
                self.program[first_idx] = self.inputs.get()
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
                self.program[third_idx] = 1 if first_param < second_param else 0
            elif opcode == 8:
                self.program[third_idx] = 1 if first_param == second_param else 0
            elif opcode == 9:
                relative_offset += first_param

            if opcode in [1, 2, 7, 8]:
                index += 4
            elif opcode in [3, 4, 9]:
                index += 2
            else:
                index += 3

    def add_input(self, new_input: int):
        self.inputs.put(new_input)

    def get_output(self):
        return self.outputs.get()

    @staticmethod
    def parse_operation(operation: str):
        return (
            int(operation[-2:]),
            int(operation[-3]),
            int(operation[-4]),
            int(operation[-5]),
        )


class Tile(object):
    def __init__(self, x, y, tile_id):
        self.x = x
        self.y = y
        self.tile_id = tile_id


computer = Computer(computer_init)
computer.start()

tiles = []
while computer.is_alive():
    tiles.append(Tile(computer.get_output(), computer.get_output(), computer.get_output()))

print("Total number of block tiles is {}".format(len([tile for tile in tiles if tile.tile_id == 2])))
