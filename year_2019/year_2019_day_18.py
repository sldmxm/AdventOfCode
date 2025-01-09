import heapq
import time
from collections import defaultdict, deque

from utils.download_data import download_data

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def read_data(file_path: str) -> list[list[str]]:
    with open(file_path) as f:
        data = [[char for char in line.strip()] for line in f.readlines()]
    return data


def solve_part1(data: list[list[str]]) -> int:
    keys_count = 0
    start = None
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == '@':
                start = (row, col)
            elif data[row][col].islower():
                keys_count += 1

    keys: frozenset[str] = frozenset()
    step = 0
    if not start:
        return -1
    y, x = start
    seen = set()
    queue = deque([(step, y, x, keys)])
    while queue:
        step, y, x, keys = queue.popleft()
        if len(keys) == keys_count:
            return step
        for dy, dx in DIRECTIONS:
            ny, nx = y + dy, x + dx
            if (ny, nx, keys) in seen:
                continue
            next_step = data[ny][nx]
            if (
                next_step == '#'
                or next_step.isupper()
                and next_step.lower() not in keys
            ):
                continue
            new_keys = keys | {next_step} if next_step.islower() else keys
            if (ny, nx, new_keys) in seen:
                continue
            queue.append((step + 1, ny, nx, new_keys))
            seen.add((ny, nx, new_keys))
    return -1


def build_graph(
    data: list[list[str]], starts: list[tuple[int, int]]
) -> dict[tuple[int, int], set[tuple[tuple[int, int], int, frozenset[str]]]]:
    graph = defaultdict(set)
    for start in starts:
        y, x = start
        pre_vertex = (y, x)
        step = 0
        doors: frozenset[str] = frozenset()
        seen = set()
        queue = deque([(step, y, x, pre_vertex, doors)])
        while queue:
            step, y, x, pre_vertex, doors = queue.popleft()
            for dy, dx in DIRECTIONS:
                ny, nx = y + dy, x + dx
                if not (0 <= ny < len(data) and 0 <= nx < len(data[0])):
                    continue
                next_step = data[ny][nx]
                if next_step == '#':
                    continue
                if pre_vertex == (ny, nx) or (pre_vertex, ny, nx) in seen:
                    continue

                seen.add((pre_vertex, ny, nx))
                if next_step.isupper():
                    new_doors = doors | {next_step}
                    queue.append((step + 1, ny, nx, pre_vertex, new_doors))
                elif next_step.islower():
                    graph[(ny, nx)].add((pre_vertex, step + 1, doors))
                    graph[pre_vertex].add(((ny, nx), step + 1, doors))
                    new_step = 0
                    new_pre_vertex = (ny, nx)
                    queue.append((new_step, ny, nx, new_pre_vertex, doors))
                else:
                    queue.append((step + 1, ny, nx, pre_vertex, doors))
    return graph


def solve_part2(data: list[list[str]]) -> int:
    def patch_start(y: int, x: int) -> list[tuple[int, int]]:
        res = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if abs(dy) == abs(dx) and dy != 0:
                    res.append((y + dy, x + dx))
                    data[y + dy][x + dx] = '@'
                else:
                    data[y + dy][x + dx] = '#'
        return res

    starts = []
    keys_count = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == '@':
                starts.append((row, col))
            elif data[row][col].islower():
                keys_count += 1

    if len(starts) == 1:
        starts = patch_start(*starts[0])

    graph = build_graph(data, starts)

    keys: frozenset[str] = frozenset()
    state = (frozenset(keys), tuple(start for start in starts))
    queue = [(0, state)]
    states = {state: 0}
    while queue:
        total_steps, (keys, robots_positions) = heapq.heappop(queue)
        if len(keys) == keys_count:
            return total_steps

        for robot_idx, robot in enumerate(robots_positions):
            for neighbor, cost, doors in graph[robot]:
                if doors - keys:
                    continue
                new_robots_positions = (
                    *robots_positions[:robot_idx],
                    neighbor,
                    *robots_positions[robot_idx + 1 :],
                )
                new_keys = keys
                y, x = neighbor
                if data[y][x].islower():
                    new_keys |= {data[y][x].upper()}
                new_state = (frozenset(new_keys), new_robots_positions)
                new_steps = total_steps + cost

                if states.get(new_state, float('inf')) > new_steps:
                    states[new_state] = new_steps
                    heapq.heappush(queue, (new_steps, new_state))
    return -1


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
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
