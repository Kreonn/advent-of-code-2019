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
