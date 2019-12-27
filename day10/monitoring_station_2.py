from utils.utils import get_angle, get_distance, load_input_file

asteroid_map = load_input_file(10).readlines()


def get_asteroids(asteroid_map: list):
    asteroids = []
    for y, line in enumerate(asteroid_map):
        for x, character in enumerate(line):
            if character == "#":
                asteroids.append((x, y))

    return asteroids


def get_asteroids_by_angle(asteroid: tuple, asteroids: list):
    asteroids_by_angle = {}
    others = [ast for ast in asteroids if ast != asteroid]

    for other in others:
        angle = get_angle(asteroid, other)
        distance = get_distance(asteroid, other)

        if angle not in asteroids_by_angle:
            asteroids_by_angle[angle] = {}

        asteroids_by_angle[angle][distance] = other

    return asteroids_by_angle


asteroids = get_asteroids(asteroid_map)

max_observable = 0
station = None

for asteroid in asteroids:
    visible_asteroids = get_asteroids_by_angle(asteroid, asteroids)

    if len(visible_asteroids) > max_observable:
        max_observable = len(visible_asteroids)
        station = asteroid

awaited_vaporized = None
last_vaporized = (0, 0)
vaporized_count = 0

remaining_asteroids = get_asteroids_by_angle(station, asteroids)

while awaited_vaporized is None:
    for angle in sorted(remaining_asteroids.keys()):
        if remaining_asteroids[angle]:
            last_vaporized = remaining_asteroids[angle].pop(
                min(remaining_asteroids[angle])
            )
            vaporized_count += 1

            if vaporized_count == 200:
                awaited_vaporized = last_vaporized

print(
    "The 200th vaporized asteroid was located at coordinates {}".format(
        awaited_vaporized[0] * 100 + awaited_vaporized[1]
    )
)
