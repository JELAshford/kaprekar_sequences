import matplotlib.pylab as plt
from functools import cache
import networkx as nx
from tqdm import tqdm
import numpy as np


@cache
def next_number(number: int) -> int:
    sorted_numbers = sorted(str(number).zfill(NUM_DIGITS))
    min_num = int("".join(sorted_numbers))
    max_num = int("".join(sorted_numbers[::-1]))
    return max_num - min_num


NUM_DIGITS = 7
MAX_SAMPLES = 10_000_000


# Generate graph
start_numbers = range(10**NUM_DIGITS)
if MAX_SAMPLES < len(start_numbers):
    start_numbers = np.random.choice(start_numbers, MAX_SAMPLES, replace=False)

graph = nx.DiGraph()
for start_number in tqdm(start_numbers):
    number = start_number
    history = [start_number]
    while history[-1] not in history[:-1]:
        new_number = next_number(number)
        graph.add_edge(
            number,
            new_number,
            weight=graph[number][new_number]["weight"] + 1
            if graph.has_edge(number, new_number)
            else 1,
        )
        history.append(new_number)
        number = new_number


# Remove single use edges
filtered_graph = graph.copy()
edges = list(filtered_graph.edges(data=True))
for edge in edges:
    if edge[2]["weight"] < 2:
        filtered_graph.remove_edge(edge[0], edge[1])

# Remove consquently unconnected nodes
isolated_nodes = list(nx.isolates(filtered_graph))
filtered_graph.remove_nodes_from(isolated_nodes)

# Identify cycles
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
sub_layout = nx.nx_agraph.graphviz_layout(
    filtered_graph,
    prog="dot",
    args="-Grankdir=LR",
)
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
