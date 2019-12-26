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
layered_pixels = list(zip(*layers))

decoded_image = [str(next(x for x in pixel if x < 2)) for pixel in layered_pixels]

# Print image (I switched colors because it looks better on my dark-themed console ;D)
print("Image decoded => ")
for line in [
    decoded_image[x : x + PX_WIDTH] for x in range(0, len(decoded_image), PX_WIDTH)
]:
    line = "".join(line)
    line = line.replace("0", " ")
    line = line.replace("1", "\u2588")
    print(line)
