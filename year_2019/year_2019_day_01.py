import time


def read_data(file_path: str) -> list[int]:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        data.append(int(line.strip()))
    return data


def solve_part1(data: list[int]) -> int:
    res = 0
    for n in data:
        res += n // 3 - 2
    return res


def solve_part2(data: list[int]) -> int:
    res = 0
    for n in data:
        while n:
            n = (n // 3 - 2) if (n // 3 - 2) > 0 else 0
            res += n
    return res


def main() -> None:
    data = read_data('data/01.txt')
    # data = read_data('data/test.txt')

    start = time.monotonic()
    res = solve_part1(data)
    print('Part 1:', res)
    print(time.monotonic() - start)

    start = time.monotonic()
    res = solve_part2(data)
    print('Part 2:', res)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
