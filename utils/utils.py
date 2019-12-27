import math
import os


def load_input_file(identifier: int):
    input_filepath = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data/input{0:02d}.txt".format(identifier),
    )

    if os.path.exists(input_filepath):
        return open(os.path.abspath(input_filepath))
    else:
        raise FileNotFoundError("File {} not found".format(input_filepath))


def get_angle(start: tuple, end: tuple):
    y = end[0] - start[0]
    x = start[1] - end[1]

    angle = math.atan2(y, x) * 180 / math.pi

    if angle < 0:
        angle = 360 + angle

    return angle

def get_distance(start: tuple, end: tuple):
    return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
