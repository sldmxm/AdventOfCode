import time


def read_data(file_path: str) -> list[list[int]]:
    with open(file_path) as f:
        lines = f.readlines()
    data = []
    for line in lines:
        line = line.strip()
        parts = line.split()
        p_part = parts[0].split('=')
        x, y = [int(n) for n in p_part[1].split(',')]
        v_part = parts[1].split('=')
        vx, vy = [int(n) for n in v_part[1].split(',')]
        data.append([x, y, vx, vy])
    return data


def solve_part1(data, steps, n_cols, n_rows):
    quadrants = [[0, 0], [0, 0]]
    cols_middle = n_cols // 2
    cols_even = n_cols % 2 == 0
    rows_middle = n_rows // 2
    rows_even = n_rows % 2 == 0
    for robot in data:
        x, y, vx, vy = robot
        nx = (x + vx * steps) % n_cols
        ny = (y + vy * steps) % n_rows
        if (not cols_even and nx == cols_middle) or (
            not rows_even and ny == rows_middle
        ):
            continue
        quadrants[ny >= rows_middle][nx >= cols_middle] += 1
    res = 1
    for r in quadrants:
        res *= r[0] * r[1]
    return res


def solve_part2(data, n_cols, n_rows):
    def get_max_in_row():
        res = 0
        for y in range(n_rows):
            left = None
            for x in range(n_cols):
                if (y, x) in cur:
                    if left is None:
                        left = x
                elif left:
                    res = max(res, x - left)
                    left = None
        return res

    quadrants = [[0, 0], [0, 0]]
    cols_middle = n_cols // 2
    cols_even = n_cols % 2 == 0
    rows_middle = n_rows // 2
    rows_even = n_rows % 2 == 0
    step = 0
    while True:
        cur = set()
        for robot in data:
            x, y, vx, vy = robot
            nx = (x + vx * step) % n_cols
            ny = (y + vy * step) % n_rows
            if (not cols_even and nx == cols_middle) or (
                not rows_even and ny == rows_middle
            ):
                continue
            cur.add((ny, nx))
            quadrants[ny >= rows_middle][nx >= cols_middle] += 1

        if get_max_in_row() > 10:
            tmp = [['.'] * n_cols for _ in range(n_rows)]
            for y, x in cur:
                tmp[y][x] = '*'
            tmp = [''.join(row) for row in tmp]
            print(step, *tmp, sep='\n')
            break
        step += 1


def main():
    start = time.monotonic()
    data = read_data('data/14.txt')
    res = solve_part1(data, 100, 101, 103)
    print('Part 1:', res)  # 218295000
    solve_part2(data, 101, 103)
    print(time.monotonic() - start)


if __name__ == '__main__':
    main()
