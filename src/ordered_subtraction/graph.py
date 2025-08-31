from itertools import combinations_with_replacement
import matplotlib.pylab as plt
from functools import cache
import networkx as nx
from math import comb
from tqdm import tqdm


NUM_DIGITS = 15


def generate_canonical_representatives(num_digits=NUM_DIGITS):
    """Generate all unique digit combinations as canonical numbers"""
    for combo in combinations_with_replacement(range(10), num_digits):
        yield int("".join(map(str, combo)))


def to_canonical(number, num_digits=NUM_DIGITS):
    """Convert any number to its canonical (sorted digits) form"""
    return int("".join(sorted(str(number).zfill(num_digits))))


@cache
def next_number(number: int) -> int:
    sorted_numbers = sorted(str(number).zfill(NUM_DIGITS))
    min_num = int("".join(sorted_numbers))
    max_num = int("".join(sorted_numbers[::-1]))
    return to_canonical(max_num - min_num)


# Generate graph edges
edges, nodes = set(), set()
num_starts = comb(NUM_DIGITS + 9, 9)
for start_number in tqdm(
    generate_canonical_representatives(NUM_DIGITS), total=num_starts
):
    sorted_start = to_canonical(start_number)
    current, next = sorted_start, next_number(sorted_start)
    nodes.add(next)
    while current not in nodes:
        current, next = (next, next_number(next))
        nodes.add(next)
    edges.add((current, next))


# Create graph and filter to cycle + feed nodes
full_graph = nx.DiGraph()
full_graph.add_edges_from(edges)
cycles = list(nx.simple_cycles(full_graph))
cycle_nodes = set(node for cycle in cycles for node in cycle)

# Find nodes that lead directly into cycle nodes (one step away)
feeder_nodes = set()
for node in cycle_nodes:
    for node_before in full_graph.predecessors(node):
        if node_before not in cycle_nodes:
            feeder_nodes.add(node_before)

# Create subgraph with cycles + feeders, and filter edges
edges_to_keep = set()
subgraph = full_graph.subgraph(cycle_nodes | feeder_nodes)
for u, v in full_graph.edges():
    if (u in cycle_nodes or u in feeder_nodes) and v in cycle_nodes:
        edges_to_keep.add((u, v))


# Create filtered graph
filtered_graph = nx.DiGraph()
filtered_graph.add_edges_from(edges_to_keep)
cycles = list(nx.simple_cycles(filtered_graph))
cycle_nodes = set(node for cycle in cycles for node in cycle)
cycle_edges = set((c[i], c[(i + 1) % len(c)]) for c in cycles for i in range(len(c)))

# Create styling based on cycles
node_colours = [
    "red" if node in cycle_nodes else "lightgrey" for node in filtered_graph.nodes()
]
edge_colors = [
    "red" if (u, v) in cycle_edges else "lightgrey" for u, v in filtered_graph.edges()
]
cycle_labels = {node: str(node).zfill(NUM_DIGITS) for node in cycle_nodes}


# Visualise
fig, ax = plt.subplots(1, 1, figsize=(24, 24))
sub_layout = nx.nx_agraph.graphviz_layout(filtered_graph, prog="neato")
nx.draw(
    ax=ax,
    G=filtered_graph,
    pos=sub_layout,
    node_size=20,
    node_color=node_colours,
    edge_color=edge_colors,
    width=1,
    arrowsize=15,
    # font_size=6,
    font_color="black",
    labels=cycle_labels,
)
plt.savefig(f"../../out/{NUM_DIGITS}-long_numbers.png")
plt.show()
