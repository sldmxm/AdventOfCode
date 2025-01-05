import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp

DIRECTIONS = ((-1, 0, 1), (0, 1, 4), (1, 0, 2), (0, -1, 3))
RETURN_COMMAND = {1: 2, 2: 1, 3: 4, 4: 3}


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def print_map(maze: dict[tuple[int, int], str]) -> None:
    min_x, max_x = (
        min(col for (row, col) in maze),
        max(col for (row, col) in maze),
    )
    min_y, max_y = (
        min(row for (row, col) in maze),
        max(row for (row, col) in maze),
    )
    picture = []
    for row in range(max_y - min_y + 1):
        line = []
        for col in range(max_x - min_x + 1):
            line.append(maze.get((row + min_y, col + min_x), ' '))
        picture.append(''.join(line))
    print(*picture, sep='\n')


def solve_part1(data: str) -> int | None:
    comp = IntcodeComp(data)
    maze = {}
    y, x, step = 0, 0, 0
    stack = [(y, x, step, comp)]
    while stack:
        y, x, step, comp = stack.pop(0)
        maze[(y, x)] = '.'
        for dy, dx, command in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if (ny, nx) not in maze:
                comp.run_whole_code([command])
                output = comp.pop_output()
                match output:
                    case 0:
                        maze[(ny, nx)] = '█'
                    case 1:
                        new_comp = comp.clone()
                        stack.append((ny, nx, step + 1, new_comp))
                        comp.run_whole_code([RETURN_COMMAND[command]])
                    case 2:
                        maze[(ny, nx)] = '@'
                        print_map(maze)
                        return step + 1
    return None


def solve_part2(data: str) -> int | None:
    def crawl_maze() -> (
        tuple[dict[tuple[int, int], str], tuple[int, int] | None]
    ):
        comp = IntcodeComp(data)
        maze: dict[tuple[int, int], str] = {}
        oxygen_station = None
        y, x = 0, 0
        stack = [(y, x, comp)]
        while stack:
            y, x, comp = stack.pop(0)
            maze[(y, x)] = '.' if maze.get((y, x)) != '@' else '@'
            for dy, dx, command in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (ny, nx) not in maze:
                    comp.run_whole_code([command])
                    output = comp.pop_output()
                    match output:
                        case 0:
                            maze[(ny, nx)] = '█'
                        case 1:
                            new_comp = comp.clone()
                            stack.append((ny, nx, new_comp))
                            comp.run_whole_code([RETURN_COMMAND[command]])
                        case 2:
                            maze[(ny, nx)] = '@'
                            oxygen_station = (ny, nx)
                            new_comp = comp.clone()
                            stack.append((ny, nx, new_comp))
                            comp.run_whole_code([RETURN_COMMAND[command]])
        return maze, oxygen_station

    maze, oxygen_station = crawl_maze()
    if not oxygen_station:
        return None
    tick = 0
    stack = [(*oxygen_station, tick)]
    while stack:
        y, x, tick = stack.pop(0)
        maze[(y, x)] = '@'
        for dy, dx, _ in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if maze[(ny, nx)] == '.':
                stack.append((ny, nx, tick + 1))
    print_map(maze)
    return tick


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
