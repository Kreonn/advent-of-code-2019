from queue import SimpleQueue
from threading import Thread
import time
from utils.growing_list import GrowingList
from utils.utils import load_input_file

computer_init = [int(code) for code in load_input_file(11).readline().split(",")]


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


class PaintingRobot(object):
    def __init__(self, brain_init: list):
        self.brain = Computer(brain_init)

        self.current_x = 0
        self.current_y = 0

        self.direction = 0

        self.painted_panels = {(0, 0): 1}

        self.brain.start()
    
    def __str__(self):
        max_x = max(self.painted_panels.keys(), key=lambda key: key[0])[0]
        max_y = max(self.painted_panels.keys(), key=lambda key: key[1])[1]

        canvas = [
            [" "] * (max_x + 1)
            for y in range(max_y + 1)
        ]

        for pos, color in self.painted_panels.items():
            canvas[pos[1]][pos[0]] = "\u2588" if color == 1 else " "

        return "\n".join(["".join(canvas_line) for canvas_line in canvas])

    def step(self):
        current_pos = (self.current_x, self.current_y)

        # Send camera input to brain
        current_color = 0
        if current_pos in self.painted_panels:
            current_color = self.painted_panels[current_pos]
        self.brain.add_input(current_color)

        # Get new color
        new_color = self.brain.get_output()
        self.painted_panels[current_pos] = new_color

        # Move robot
        new_direction = self.brain.get_output()
        self.apply_direction(new_direction)
        self.move()

    def is_finished(self):
        return not self.brain.is_alive()

    def get_painted_count(self):
        return len(self.painted_panels.keys())

    def apply_direction(self, new_direction):
        if new_direction == 0:
            self.direction = (self.direction - 90) % 360
        else:
            self.direction = (self.direction + 90) % 360

    def move(self):
        if self.direction == 0:
            self.current_y -= 1
        elif self.direction == 90:
            self.current_x += 1
        elif self.direction == 180:
            self.current_y += 1
        else:
            self.current_x -= 1


robot = PaintingRobot(computer_init)
while not robot.is_finished():
    robot.step()

print("Painting finished => \n{}".format(robot))
