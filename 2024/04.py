def count_xmas_part1(data: list[str]) -> int:
    PATTERN = 'XMAS'
    PATHS = (
        ((1, 0), (2, 0), (3, 0)),
        ((1, 1), (2, 2), (3, 3)),
        ((0, 1), (0, 2), (0, 3)),
        ((-1, 1), (-2, 2), (-3, 3)),
        ((-1, 0), (-2, 0), (-3, 0)),
        ((-1, -1), (-2, -2), (-3, -3)),
        ((0, -1), (0, -2), (0, -3)),
        ((1, -1), (2, -2), (3, -3)),
    )
    res = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == PATTERN[0]:
                cur_x_count = 0
                for path in PATHS:
                    is_ok = True
                    for i in range(len(path)):
                        dy, dx = path[i]
                        if not (
                                0 <= row + dy < len(data)
                                and 0 <= col + dx < len(data[0])
                                and data[row + dy][col + dx] == PATTERN[i + 1]
                        ):
                            is_ok = False
                            break
                    cur_x_count += 1 if is_ok else 0
                res += cur_x_count
    return res

def count_xmas_part2(data: list[str]) -> int:
    PATTERN = set('MAS')
    PATHS = (
        ((-1, -1), (1, 1)),
        ((-1, 1), (1, -1)),
    )
    res = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == 'A':
                diagonals = 0
                for path in PATHS:
                    cur_pattern = {'A',}
                    for i in range(len(path)):
                        dy, dx = path[i]
                        if (
                                0 <= row + dy < len(data)
                                and 0 <= col + dx < len(data[0])
                        ):
                            cur_pattern.add(data[row + dy][col + dx])
                    diagonals += cur_pattern == PATTERN
                res += 1 if diagonals == 2 else 0
    return res


def read_data(file_path: str) -> list[str]:
    with open(file_path) as f:
        res = [row.rstrip() for row in f]
    return res


if __name__ == '__main__':
    print(count_xmas_part1(read_data('data/04_input.txt')))
    print(count_xmas_part2(read_data('data/04_input.txt')))
