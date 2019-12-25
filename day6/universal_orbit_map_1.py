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

# Compute checksum
orbit_count = 0
for node_key in orbit_map.keys():
    orbit_count += tree.depth(node_key)

print("Orbit count checksum of the current orbit map is {0}".format(orbit_count))
