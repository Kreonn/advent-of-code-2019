from utils.utils import load_input_file
from collections import Counter

password_range = load_input_file(4).readline().split("-")

good_candidates = 0

for candidate in range(int(password_range[0]), int(password_range[1])):
    counter = Counter(str(candidate))
    if 2 not in counter.values():
        continue

    if not all(int(i) <= int(j) for i, j in zip(str(candidate), str(candidate)[1:])):
        continue

    good_candidates += 1

print("Number of password candidates is {0}".format(good_candidates))
