import math

from utils.utils import load_input_file

modules_list = load_input_file(1).readlines()

total_fuel_requirements = 0

for module in modules_list:
    fuel_req = float(module)

    while fuel_req > 0:
        fuel_req = math.floor(fuel_req / 3.0) - 2

        if fuel_req > 0:
            total_fuel_requirements += fuel_req

print("Total fuel requirements is {}".format(total_fuel_requirements))
