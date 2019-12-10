from utils.utils import load_input_file


class Wire(object):
    def __init__(self, directions_list: list):
        self.coordinates = [(0, 0)]

        for code in directions_list:
            self.parse_direction(code)

    def parse_direction(self, code: str):
        direction = code[0]
        steps = int(code[1:])
        last_coordinates = self.coordinates[-1]

        if direction == "D":
            self.coordinates.extend(
                [
                    (last_coordinates[0], last_coordinates[1] - step)
                    for step in range(1, steps + 1)
                ]
            )
        elif direction == "U":
            self.coordinates.extend(
                [
                    (last_coordinates[0], last_coordinates[1] + step)
                    for step in range(1, steps + 1)
                ]
            )
        elif direction == "L":
            self.coordinates.extend(
                [
                    (last_coordinates[0] - step, last_coordinates[1])
                    for step in range(1, steps + 1)
                ]
            )
        elif direction == "R":
            self.coordinates.extend(
                [
                    (last_coordinates[0] + step, last_coordinates[1])
                    for step in range(1, steps + 1)
                ]
            )

    def get_intersections(self, other):
        intersections = set(self.coordinates).intersection(set(other.coordinates))
        intersections.remove((0, 0))
        return intersections


input_file = load_input_file(3)
wire1 = Wire(input_file.readline().split(","))
wire2 = Wire(input_file.readline().split(","))

crossings = wire1.get_intersections(wire2)
distances = map(lambda tup: abs(tup[0]) + abs(tup[1]), crossings)

print("Closest distance to an intersection is {0}".format(min(distances)))
