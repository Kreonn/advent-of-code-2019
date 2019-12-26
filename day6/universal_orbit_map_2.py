from treelib import Tree

from utils.utils import load_input_file

orbit_map = {
    line.rstrip().split(")")[1]: line.rstrip().split(")")[0]
    for line in load_input_file(6).readlines()
}

# Build the orbit tree
tree = Tree()
tree.create_node("COM", "COM")

to_treat_nodes = ["COM"]

while len(to_treat_nodes) != 0:
    current_node = to_treat_nodes.pop()

    for orbit, center in orbit_map.items():
        if center == current_node:
            tree.create_node(orbit, orbit, parent=center)
            to_treat_nodes.append(orbit)

pertinent_paths = [path for path in tree.paths_to_leaves() if path[-1] in ["YOU", "SAN"]]

# Get lowest common ancestor dsitance from COM
lowest_common_ancestor = 0
for idx, pair in enumerate(zip(*pertinent_paths)):
    if pair[0] != pair[1]:
        lowest_common_ancestor = idx
        break

# Calculate node distance between YOU and SAN
distance = len(pertinent_paths[0]) + len(pertinent_paths[1]) - 2 * lowest_common_ancestor - 2

print("The number of orbit jumps to join Santa is {0}".format(distance))
