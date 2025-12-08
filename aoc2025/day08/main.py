import operator
from pathlib import Path
from math import dist
from itertools import combinations
from functools import reduce

import networkx as nx

Point = tuple[int, int, int]


def parse_input(input_text: str) -> list[Point]:
    return [
        tuple(int(coord) for coord in line.split(","))
        for line in input_text.splitlines()
    ]


def main(input_path: Path):
    input_text = input_path.read_text()
    points = parse_input(input_text)

    is_example = len(points) == 20
    max_attempts_part1 = 10 if is_example else 1000

    connections = []
    for p1, p2 in combinations(points, r=2):
        connections.append(((p1, p2), dist(p1, p2)))

    shortest_connections = sorted(connections, key=lambda x: x[1])

    G = nx.Graph()
    G.add_nodes_from(points)

    for attempt, ((p1, p2), _) in enumerate(shortest_connections):
        if attempt == max_attempts_part1:
            clusters = list(nx.connected_components(G))
            top_3_clusters = sorted(clusters, key=len, reverse=True)[:3]
            top_3_cluster_sizes = [len(cluster) for cluster in top_3_clusters]
            print(f"Part 1: {reduce(operator.mul, top_3_cluster_sizes)}")

        if nx.has_path(G, source=p1, target=p2):
            continue

        G.add_edge(p1, p2)

        if nx.is_connected(G):
            part2_result = p1[0] * p2[0]
            print(f"Part 2: {part2_result}")
            break
