from utils.utils import load_input_file

space_image = load_input_file(8).readline()

PX_WIDTH = 25
PX_HEIGHT = 6
LAYER_SIZE = PX_WIDTH * PX_HEIGHT


def parse_space_image(img: str):
    space_img_list = list(map(int, space_image))

    return list(
        [
            space_img_list[x : x + LAYER_SIZE]
            for x in range(0, len(space_img_list), LAYER_SIZE)
        ]
    )


layers = parse_space_image(space_image)

min_zeros = LAYER_SIZE
checksum = 0

for layer in layers:
    if layer.count(0) < min_zeros:
        min_zeros = layer.count(0)
        checksum = layer.count(1) * layer.count(2)

print("Image checksum is {}".format(checksum))
