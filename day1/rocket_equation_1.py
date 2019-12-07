import math

from utils.utils import load_input_file

modules_list = load_input_file(1).readlines()

total_fuel_requirements = 0

for module in modules_list:
    fuel_req = math.floor(float(module) / 3.0) - 2

    total_fuel_requirements += fuel_req

print("Total fuel requirements is {}".format(total_fuel_requirements))
