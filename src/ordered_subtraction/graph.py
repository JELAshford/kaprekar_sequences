import matplotlib.pylab as plt
from functools import cache
from tqdm import trange
import networkx as nx


@cache
def next_number(number: int) -> int:
    sorted_numbers = sorted(str(number).zfill(NUM_DIGITS))
    min_num = int("".join(sorted_numbers))
    max_num = int("".join(sorted_numbers[::-1]))
    return max_num - min_num


NUM_DIGITS = 4

# Generate graph edges
edges, nodes = set(), set()
for start_number in trange(10**NUM_DIGITS):
    current, next = start_number, next_number(start_number)
    nodes.add(next)
    while current not in nodes:
        current, next = (next, next_number(next))
        nodes.add(next)
    edges.add((current, next))

# Create graph
filtered_graph = nx.DiGraph()
filtered_graph.add_edges_from(edges)
cycles = list(nx.simple_cycles(filtered_graph))
cycle_nodes = set(node for cycle in cycles for node in cycle)
cycle_edges = set(
    (cycle[i], cycle[(i + 1) % len(cycle)]) for cycle in cycles for i in range(len(cycle))
)

# Create styling based on cycles
node_colours = ["red" if node in cycle_nodes else "lightgrey" for node in filtered_graph.nodes()]
edge_colors = ["red" if (u, v) in cycle_edges else "lightgrey" for u, v in filtered_graph.edges()]
cycle_labels = {node: str(node) for node in cycle_nodes}


# Visualise
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
sub_layout = nx.nx_agraph.graphviz_layout(filtered_graph, prog="dot", args="-Grankdir=LR")
nx.draw(
    ax=ax,
    G=filtered_graph,
    pos=sub_layout,
    node_size=20,
    node_color=node_colours,
    edge_color=edge_colors,
    width=1,
    arrowsize=20,
    font_size=14,
    font_color="black",
    labels=cycle_labels,
)
plt.savefig(f"../../out/{NUM_DIGITS}-long_numbers.png")
plt.show()
