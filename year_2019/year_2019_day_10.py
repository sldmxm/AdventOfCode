import time
from collections import defaultdict
from math import gcd

from utils.download_data import download_data


def read_data(file_path: str) -> set[tuple[int, int]]:
    with open(file_path) as f:
        lines = f.readlines()
    data = set()
    for y, line in enumerate(lines):
        data.update({(y, x) for x, char in enumerate(line) if char == '#'})
    return data


def find_best_position(data: set[tuple[int, int]]) -> tuple[int, int]:
    count = 0
    res = (-1, -1)
    for base_y, base_x in data:
        directions = set()
        for y, x in data - {(base_y, base_x)}:
            dy, dx = y - base_y, x - base_x
            divisor = gcd(dx, dy)
            dy, dx = dy // divisor, dx // divisor
            directions.add((dy, dx))
        if len(directions) > count:
            count = len(directions)
            res = (base_y, base_x)
    if res == (-1, -1):
        raise ValueError('No valid position found')
    return res


def get_directions(
    data: set[tuple[int, int]], point: tuple[int, int]
) -> set[tuple[int, int]]:
    base_y, base_x = point
    directions = set()
    for y, x in data - {(base_y, base_x)}:
        dy, dx = y - base_y, x - base_x
        divisor = gcd(dx, dy)
        dy, dx = dy // divisor, dx // divisor
        directions.add((dy, dx))
    return directions


def solve_part1(data: set[tuple[int, int]]) -> int:
    best = find_best_position(data)
    return len(get_directions(data, best))


def quadrant(y: int, x: int) -> int:
    if x >= 0 >= y:
        return 0
    elif x > 0 and y > 0:
        return 1
    elif x <= 0 < y:
        return 2
    else:
        return 3


def solve_part2(data: set[tuple[int, int]]) -> int:
    max_x, max_y = max(x for _, x in data), max(y for y, _ in data)
    best = find_best_position(data)

    directions = get_directions(data, best)
    quadrants = defaultdict(list)
    for y, x in directions:
        quadrants[quadrant(y, x)].append((y, x))
    directions_clockwise = []
    for i in range(4):
        sort_key = {
            0: lambda a: (a[1] / abs(a[0]) if a[0] != 0 else float('inf')),
            1: lambda a: (abs(a[0]) / a[1] if a[1] != 0 else float('inf')),
            2: lambda a: (-a[1] / a[0] if a[0] != 0 else float('inf')),
            3: lambda a: (a[0] / a[1] if a[1] != 0 else float('inf')),
        }
        directions_clockwise.extend(sorted(quadrants[i], key=sort_key[i]))

    asteroids = data.copy()
    counter = 0
    direction = 0
    y, x = best
    while True:
        dy, dx = directions_clockwise[direction]
        step = 1
        while (
            0 <= (ny := y + dy * step) <= max_y
            and 0 <= (nx := x + dx * step) <= max_x
        ):
            if (ny, nx) in asteroids:
                counter += 1
                asteroids.remove((ny, nx))
                if counter == 200:
                    return ny + 100 * nx
                break
            step += 1
        direction = (direction + 1) % len(directions_clockwise)


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
