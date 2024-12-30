import time

from utils.download_data import download_data


def read_data(file_path: str) -> list[list[str]]:
    with open(file_path) as f:
        lines = f.readlines()
    data = [line.strip().split(',') for line in lines]
    return data


def get_paths(data: list[list[str]]) -> list[dict[tuple[int, int], int]]:
    DIRECTIONS = {
        'R': (0, 1),
        'L': (0, -1),
        'U': (-1, 0),
        'D': (1, 0),
    }
    paths = []
    for wire in data:
        y, x, step = 0, 0, 0
        path = {}
        for move in wire:
            direction, steps = move[0], int(move[1:])
            dy, dx = DIRECTIONS[direction]
            for _ in range(steps):
                step += 1
                y, x = y + dy, x + dx
                if (y, x) not in path:
                    path[(y, x)] = step
        paths.append(path)
    return paths


def solve_part1(data: list[list[str]]) -> int:
    paths = get_paths(data)
    intersections = paths[0].keys() & paths[1].keys()
    return min(abs(x) + abs(y) for x, y in intersections)


def solve_part2(data: list[list[str]]) -> int:
    paths = get_paths(data)
    intersections = paths[0].keys() & paths[1].keys()
    return min(
        paths[0][intersection] + paths[1][intersection]
        for intersection in intersections
    )


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res = solve_part1(data)
        print('Part 1:', res)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data)
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
