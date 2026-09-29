"""Shortest indoor route on a nonnegative weighted graph, without sensor inputs."""
import argparse
import heapq
import json
import math
from pathlib import Path


def shortest_path(graph, start, end):
    if start not in graph or end not in graph:
        raise ValueError('Start and end must be graph nodes')
    for neighbors in graph.values():
        for node, distance in neighbors.items():
            if node not in graph or isinstance(distance, bool) or not isinstance(distance, (float, int)) or not math.isfinite(distance) or distance < 0:
                raise ValueError('Edges require known nodes and finite nonnegative distances')
    costs, previous, queue = {start: 0}, {}, [(0, start)]
    while queue:
        cost, node = heapq.heappop(queue)
        if cost != costs[node]:
            continue
        if node == end:
            path = [node]
            while path[-1] != start:
                path.append(previous[path[-1]])
            return {'distance': cost, 'path': path[::-1]}
        for neighbor, distance in graph[node].items():
            candidate = cost + distance
            if candidate < costs.get(neighbor, math.inf):
                costs[neighbor], previous[neighbor] = candidate, node
                heapq.heappush(queue, (candidate, neighbor))
    raise ValueError(f'No route from {start} to {end}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('graph', type=Path)
    parser.add_argument('start')
    parser.add_argument('end')
    args = parser.parse_args()
    try:
        print(json.dumps(shortest_path(json.loads(args.graph.read_text()), args.start, args.end), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Error: {exc}\n')
