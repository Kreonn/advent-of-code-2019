from utils.utils import get_angle, load_input_file

asteroid_map = load_input_file(10).readlines()


def get_asteroids(asteroid_map: list):
    asteroids = []
    for y, line in enumerate(asteroid_map):
        for x, character in enumerate(line):
            if character == "#":
                asteroids.append((x, y))

    return asteroids


asteroids = get_asteroids(asteroid_map)

max_observable = 0
station = None

for asteroid in asteroids:
    others = [ast for ast in asteroids if ast != asteroid]

    visible_asteroids = {get_angle(asteroid, other): other for other in others}

    if len(visible_asteroids) > max_observable:
        max_observable = len(visible_asteroids)
        station = asteroid

print(
    "Maximum observable asteroids is {0} at position {1}".format(
        max_observable, station
    )
)
