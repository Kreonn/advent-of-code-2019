from itertools import combinations

from utils.utils import load_input_file

starting_positions = load_input_file(12).read().splitlines()


class Moon(object):
    def __init__(self, x: int, y: int, z: int):
        self.position_vector = [x, y, z]
        self.velocity_vector = [0, 0, 0]

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

for _ in range(1000):
    for pair in combinations(moons, 2):
        pair[0].apply_gravity(pair[1])

    for moon in moons:
        moon.step()

total_energy = sum([moon.get_energy() for moon in moons])

print("Total energy in the system after 1000 steps is {}".format(total_energy))
