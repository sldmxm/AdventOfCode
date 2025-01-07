import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp

DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def get_maze(data: str) -> list[list[str]]:
    data = '1' + data[1:]
    comp = IntcodeComp(data)
    comp.run_whole_code()
    output = comp.get_output()
    maze = []
    line = []
    for char_code in output:
        if char_code != 10:
            line.append(chr(char_code))
        else:
            maze.append(line)
            line = []
    maze = maze[:-1]
    # print('\n'.join([''.join(line) for line in maze]))
    return maze


def solve_part1(data: str) -> int:
    maze = get_maze(data)
    res = 0
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (
                maze[y][x] == '#'
                and all(
                    0 <= y + dy < len(maze) and 0 <= x + dx < len(maze[0])
                    for dy, dx in DIRECTIONS
                )
                and all(maze[y + dy][x + dx] == '#' for dy, dx in DIRECTIONS)
            ):
                res += x * y
    return res


def get_path_commands(
    path: set[tuple[int, int]], start: tuple[int, int]
) -> list[str | int] | None:
    y, x = start
    direction = 0
    commands: list[str | int] = []
    while True:
        is_dead_end = True
        for new_direction in (
            direction,
            (direction + 1) % 4,
            (direction - 1) % 4,
        ):
            dy, dx = DIRECTIONS[new_direction]
            ny, nx = y + dy, x + dx
            if (ny, nx) in path:
                is_dead_end = False
                if new_direction == direction:
                    if isinstance(commands[-1], int):
                        commands[-1] += 1
                    else:
                        raise ValueError(
                            'Mypy wants this check, '
                            "and I'm surprised if this isn't an integer."
                        )
                else:
                    commands.append(
                        'R' if new_direction == (direction + 1) % 4 else 'L'
                    )
                    commands.append(1)
                y, x = ny, nx
                direction = new_direction
                break
        if is_dead_end:
            return commands


def compress_array(arr: list[str | int]) -> list[str] | None:
    def is_valid_pattern(pattern: list[str | int]) -> bool:
        return len(','.join(map(str, pattern))) <= 20

    def find_all_occurrences(
        pattern: list[str | int], arr: list[str | int]
    ) -> list[int]:
        n, m = len(arr), len(pattern)
        occurrences = []
        i = 0
        while i <= n - m:
            if (
                arr[i] == pattern[0]
                and arr[i + m - 1] == pattern[-1]
                and arr[i : i + m] == pattern
            ):
                occurrences.append(i)
                i += m
                continue
            i += 1
        return occurrences

    def remove_pattern(
        arr: list[str | int], pattern: list[str | int], occurrences: list[int]
    ) -> list[str | int]:
        if not occurrences:
            return arr
        result = []
        last_pos = 0
        for pos in occurrences:
            result.extend(arr[last_pos:pos])
            last_pos = pos + len(pattern)
        result.extend(arr[last_pos:])
        return result

    def try_compress(
        arr: list[str | int],
        patterns: list[list[str | int]] | None = None,
        depth: int = 0,
    ) -> list[list[str | int]] | None:
        if patterns is None:
            patterns = []
        if depth >= 3 or not arr:
            return patterns if not arr else None

        best_solution = None
        best_remaining_len = len(arr)

        for length in range(2, min(len(arr) + 1, 11), 2):
            pattern = arr[:length]

            if not is_valid_pattern(pattern):
                continue

            occurrences = find_all_occurrences(pattern, arr)
            remaining_arr = remove_pattern(arr, pattern, occurrences)
            remaining_len = len(remaining_arr)

            if best_solution and remaining_len >= best_remaining_len:
                continue

            result = try_compress(
                remaining_arr, patterns + [pattern], depth + 1
            )
            if result is not None:
                best_solution = result
                best_remaining_len = remaining_len

                if remaining_len == 0:
                    break

        return best_solution

    solution = try_compress(arr)
    return (
        [','.join(map(str, pattern)) for pattern in solution]
        if solution
        else None
    )


def solve_part2(data: str) -> int:
    maze = get_maze(data)
    path = set()
    start = None
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == '#':
                path.add((y, x))
            elif maze[y][x] == '^':
                start = (y, x)
    if not start:
        raise ValueError('No starting position.')

    commands = get_path_commands(path, start)
    if not commands:
        raise ValueError("Can't find the path commands.")

    commands_string = ','.join(map(str, commands))
    patterns = compress_array(commands)
    if not patterns:
        raise ValueError(
            "Can't see any correct patterns in the path commands."
        )

    for pattern, letter in zip(patterns, 'ABC', strict=False):
        commands_string = commands_string.replace(pattern, letter)

    comp = IntcodeComp(data)
    for input_string in (commands_string, *patterns, 'n'):
        inpt = [ord(c) for c in input_string]
        inpt.append(ord('\n'))
        comp.run_whole_code(inpt)

    return comp.pop_output()


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
