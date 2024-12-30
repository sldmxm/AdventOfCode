import time
from collections import defaultdict

from utils.download_data import download_data


def read_data(file_path: str) -> list[str]:
    with open(file_path) as f:
        lines = f.readlines()
    data = [line.strip() for line in lines]
    return data


def solve_part1(data: list[str]) -> int:
    orbits = defaultdict(set)
    for line in data:
        parent, kid = line.split(')')
        orbits[parent].add(kid)
    root = 'COM'
    stack = [(root, 0)]
    res = 0
    while stack:
        node, level = stack.pop()
        res += level
        if node in orbits:
            stack.extend([(kid, level + 1) for kid in orbits[node]])
    return res


def solve_part2(data: list[str]) -> int:
    orbits = defaultdict(set)
    for line in data:
        parent, kid = line.split(')')
        orbits[parent].add(kid)
    root = 'COM'
    stack: list[tuple[str, tuple[str, ...]]] = [(root, tuple())]
    res_paths = []
    while stack:
        node, path = stack.pop()
        path = tuple(list(path) + [node])
        if node in orbits:
            stack.extend([(kid, path) for kid in orbits[node]])
        if node in ('YOU', 'SAN'):
            res_paths.append(path)
    common_path = set(res_paths[0]) & set(res_paths[1])
    res = len(res_paths[0]) + len(res_paths[1]) - len(common_path) * 2 - 2
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
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
