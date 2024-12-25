import time


def read_data(file_path: str) -> list[list[int]]:
    with open(file_path) as f:
        rows = f.readlines()
    data = []
    for row in rows:
        data.append([int(n) for n in row.rstrip()])
    return data


def solve(data) -> (int, int):
    def _dfs(zeros: list[tuple[int, int]], is_part1: bool) -> int:
        total_res = 0
        while zeros:
            stack = [zeros.pop()]
            cur_zero_res = 0
            seen = set()
            while stack:
                y, x = stack.pop()
                if data[y][x] == 9:
                    cur_zero_res += 1
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    if (
                        0 <= x + dx < len(data[0])
                        and 0 <= y + dy < len(data)
                        and ((y + dy), (x + dx)) not in seen
                        and data[y + dy][x + dx] == data[y][x] + 1
                    ):
                        stack.append((y + dy, x + dx))
                        if is_part1:
                            seen.add((y + dy, x + dx))
            total_res += cur_zero_res
        return total_res

    zeros = [
        (y, x)
        for y in range(len(data))
        for x in range(len(data[0]))
        if data[y][x] == 0
    ]

    return _dfs(zeros[:], True), _dfs(zeros, False)


def main():
    data = read_data('data/10.txt')
    start = time.monotonic()
    res1, res2 = solve(data)
    print('Part 1:', res1)
    print('Part 2:', res2)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
