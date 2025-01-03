import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp, ProgramStatus


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def solve_part1(data: str) -> int:
    DIRECTIONS = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    )
    comp = IntcodeComp(data)
    y, x = 0, 0
    direction = 0
    panels: dict[tuple[int, int], int] = {}
    while comp.get_status() != ProgramStatus.DONE:
        color = panels.get((y, x), 0)
        comp.run_whole_code(input_data=[color])
        new_color, new_direction_flag = comp.get_output()[-2:]
        panels[(y, x)] = new_color
        direction = (direction + (1 if new_direction_flag == 1 else -1)) % len(
            DIRECTIONS
        )
        dy, dx = DIRECTIONS[direction]
        y += dy
        x += dx
    return len(panels)


def solve_part2(data: str) -> None:
    DIRECTIONS = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    )
    comp = IntcodeComp(data)
    y, x = 0, 0
    direction = 0
    panels = {(0, 0): 1}
    while comp.get_status() != ProgramStatus.DONE:
        color = panels.get((y, x), 0)
        comp.run_whole_code(input_data=[color])
        new_color, new_direction_flag = comp.get_output()[-2:]
        panels[(y, x)] = new_color
        direction = (direction + (1 if new_direction_flag == 1 else -1)) % len(
            DIRECTIONS
        )
        dy, dx = DIRECTIONS[direction]
        y += dy
        x += dx
    min_x, min_y = min(x for (y, x) in panels), min(y for (y, x) in panels)
    max_x, max_y = max(x for (y, x) in panels), max(y for (y, x) in panels)

    picture = []
    for y in range(max_y - min_y + 1):
        line = []
        for x in range(max_x - min_x + 1):
            if panels.get((y + min_y, x + min_x), 0) == 1:
                line.append('#')
            else:
                line.append(' ')
        picture.append(''.join(line))
    print(*picture, sep='\n')


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
        solve_part2(data)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
