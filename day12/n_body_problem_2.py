from itertools import combinations

from utils.utils import get_least_common_multiple, load_input_file

starting_positions = load_input_file(12).read().splitlines()


class Moon(object):
    def __init__(self, x: int, y: int, z: int):
        self.position_vector = [x, y, z]
        self.velocity_vector = [0, 0, 0]

        self.initial_state = [(x, 0), (y, 0), (z, 0)]

    def get_cycle(self):
        current_state = list(zip(self.position_vector, self.velocity_vector))

        return [
            current_state[i] == self.initial_state[i]
            for i in range(len(self.initial_state))
        ]

    def apply_gravity(self, other: list):
        for index, dimension in enumerate(self.position_vector):
            if dimension < other.position_vector[index]:
                self.velocity_vector[index] += 1
                other.velocity_vector[index] -= 1
            elif dimension > other.position_vector[index]:
                self.velocity_vector[index] -= 1
                other.velocity_vector[index] += 1

    def step(self):
        for index, velocity in enumerate(self.velocity_vector):
            self.position_vector[index] += velocity

    def get_energy(self):
        potential_energy = sum([abs(val) for val in self.position_vector])
        kinetic_energy = sum([abs(val) for val in self.velocity_vector])

        return potential_energy * kinetic_energy


def parse_moon(moon_str: str):
    moon_vector = [int(val.split("=")[1]) for val in moon_str[1:-1].split(", ")]
    return Moon(*moon_vector)


moons = list(map(parse_moon, starting_positions))
step_count = 0
cycles = [0, 0, 0]

while True:
    for pair in combinations(moons, 2):
        pair[0].apply_gravity(pair[1])

    for moon in moons:
        moon.step()

    step_count += 1

    has_cycles = map(all, zip(*[moon.get_cycle() for moon in moons]))
    for index, is_cycle in enumerate(has_cycles):
        if is_cycle and cycles[index] == 0:
            cycles[index] = step_count

    if all([cycle != 0 for cycle in cycles]):
        break

total_step = get_least_common_multiple(
    cycles[0], get_least_common_multiple(cycles[1], cycles[2])
)
print("Total number of steps before a full cycle of the moons is {}".format(total_step))
