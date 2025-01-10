import heapq
import time
from collections import defaultdict, deque
from typing import Any

from utils.download_data import download_data

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def read_data(file_path: str) -> list[list[str]]:
    with open(file_path) as f:
        data = [
            [char for char in line.replace('\n', '')] for line in f.readlines()
        ]
    return data


def parse_portals(data: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    def get_cell(
        arr: list[list[str]] | list[tuple[Any]], row: int, col: int
    ) -> str:
        if 0 <= row < len(arr) and 0 <= col < len(arr[0]):
            return arr[row][col]
        return ''

    def add_portals(
        arr: list[list[str]] | list[tuple[Any]], is_rotated: bool
    ) -> None:
        for y in range(len(arr)):
            for x in range(len(arr[0])):
                if arr[y][x].isupper() and get_cell(arr, y, x - 1).isupper():
                    portal = ''.join(arr[y][x - 1 : x + 1])
                    for dx in (1, -2):
                        if get_cell(arr, y, x + dx) == '.':
                            portals[portal].append(
                                (y, x + dx) if not is_rotated else (x + dx, y)
                            )

    portals: dict[str, list[tuple[int, int]]] = defaultdict(list)
    add_portals(data, False)
    add_portals(list(zip(*data, strict=False)), True)
    return portals


def build_graph(
    data: list[list[str]], portals: dict[str, list[tuple[int, int]]]
) -> dict[tuple[int, int], set[tuple[int, tuple[int, int]]]]:
    graph = defaultdict(set)
    all_portals = {node for nodes in portals.values() for node in nodes}
    for points in portals.values():
        if len(points) > 1:
            graph[points[0]].add((1, points[1]))
            graph[points[1]].add((1, points[0]))

        for y, x in points:
            pre_vertex = (y, x)
            step = 0
            seen = set()
            queue = deque([(step, y, x, pre_vertex)])
            while queue:
                step, y, x, pre_vertex = queue.popleft()
                for dy, dx in DIRECTIONS:
                    ny, nx = y + dy, x + dx
                    if not (0 <= ny < len(data) and 0 <= nx < len(data[0])):
                        continue
                    if data[ny][nx] != '.':
                        continue
                    if pre_vertex == (ny, nx) or (pre_vertex, ny, nx) in seen:
                        continue

                    seen.add((pre_vertex, ny, nx))

                    if (ny, nx) in all_portals:
                        graph[pre_vertex].add((step + 1, (ny, nx)))
                        graph[(ny, nx)].add((step + 1, pre_vertex))
                    else:
                        queue.append((step + 1, ny, nx, pre_vertex))

    return graph


def solve_part1(data: list[list[str]]) -> int | float:
    portals = parse_portals(data)
    graph = build_graph(data, portals)
    start = portals['AA'][0]
    finish = portals['ZZ'][0]

    node_costs = {node: float('inf') for node in graph}
    node_costs[start] = 0

    queue: list[tuple[float | int, tuple[int, int]]] = [(0, start)]
    seen = {}
    res = float('inf')
    while queue:
        cur_costs, node = heapq.heappop(queue)
        if node == finish:
            res = min(res, cur_costs)
        else:
            seen[node] = cur_costs
        for costs, neighbor in graph[node]:
            node_costs[neighbor] = min(node_costs[neighbor], cur_costs + costs)
            if neighbor not in seen or seen[neighbor] > node_costs[neighbor]:
                heapq.heappush(queue, (node_costs[neighbor], neighbor))
                seen[neighbor] = node_costs[neighbor]
    return res


def solve_part2(data: list[list[str]]) -> int | float:
    def get_level_change(portal: tuple[int, int]) -> int:
        y, x = portal
        if len(data) - y == 3 or y == 2 or x == 2 or len(data[0]) - x == 3:
            return -1
        return 1

    portals = parse_portals(data)
    MAX_DEPTH = len(portals) * 2

    graph = build_graph(data, portals)
    start = portals['AA'][0]
    finish = portals['ZZ'][0]

    level, direction = 0, 0
    node_costs: dict[tuple[tuple[int, int], int, int], int | float] = dict()
    node_costs[(start, level, direction)] = 0
    queue: list[tuple[float | int, int, int, tuple[int, int]]] = [
        (0, level, direction, start)
    ]
    seen = {}
    res = float('inf')
    while queue:
        cur_costs, level, direction, node = heapq.heappop(queue)

        if level == 0 and node == finish:
            res = min(res, cur_costs)
        else:
            seen[(node, level, direction)] = cur_costs

        for costs, neighbor in graph[node]:
            new_level = level
            new_direction = direction
            if costs == 1:
                new_direction = get_level_change(neighbor)

                # only down from 0-level
                if level == 0 and new_direction == 1:
                    continue

                new_level += new_direction
                if abs(new_level) > MAX_DEPTH:
                    continue

            node_costs[(neighbor, new_level, new_direction)] = min(
                node_costs.get(
                    (neighbor, new_level, new_direction), float('inf')
                ),
                cur_costs + costs,
            )
            if (neighbor, new_level, new_direction) not in seen or seen[
                (neighbor, new_level, new_direction)
            ] > node_costs[(neighbor, new_level, new_direction)]:
                heapq.heappush(
                    queue,
                    (
                        node_costs[(neighbor, new_level, new_direction)],
                        new_level,
                        new_direction,
                        neighbor,
                    ),
                )
                seen[(neighbor, new_level, new_direction)] = node_costs[
                    (neighbor, new_level, new_direction)
                ]

    return res


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve_part1(data)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data)
        print('Part 2:', res2)  # 7114
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
