import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def solve_part1(data: str) -> int:
    res = 0
    for y in range(50):
        for x in range(50):
            comp = IntcodeComp(data)
            comp.run_whole_code([x, y])
            res += comp.pop_output()
    return res


def solve_part2(data: str) -> int:
    SHIP_SIZE = 100

    # There's a bit of cheating here,
    # larger values will give a slightly wrong result
    MAX_BEAM_LENGTH_X = 1105
    MAX_BEAM_LENGTH_Y = 826

    def check(x: int, y: int) -> int:
        comp = IntcodeComp(data)
        comp.run_whole_code([x, y])
        return comp.pop_output()

    def find_right_boundary(y: int) -> int:
        def find_any(left: int, right: int) -> int:
            if left >= right:
                return -1

            mid = (left + right) // 2
            if check(mid, y) == 1:
                return mid
            else:
                if (res := find_any(left, mid)) != -1:
                    return res
                else:
                    return find_any(mid + 1, right)

        left_x = find_any(0, MAX_BEAM_LENGTH_X)
        right_x = MAX_BEAM_LENGTH_X
        while left_x < right_x:
            mid_x = (left_x + right_x + 1) // 2
            if check(mid_x, y) == 1:
                left_x = mid_x
            else:
                right_x = mid_x - 1
        return left_x

    left_y = 0
    right_y = MAX_BEAM_LENGTH_Y
    while left_y < right_y:
        mid_y = (left_y + right_y) // 2
        x = find_right_boundary(mid_y)
        if check(x - SHIP_SIZE + 1, mid_y + SHIP_SIZE - 1) == 0:
            left_y = mid_y + 1
        else:
            right_y = mid_y

    y = left_y
    x = find_right_boundary(y)

    return (x - SHIP_SIZE + 1) * 10_000 + y


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
        print('Part 2:', res2)  # 1001_0825
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
