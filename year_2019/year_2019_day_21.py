import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def solve_part1(data: str) -> int:
    PROGRAM = [
        'NOT A J',
        'NOT C T',
        'AND D T',
        'OR T J',
        'WALK',
    ]
    comp = IntcodeComp(data)
    input_string = [ord(char) for char in '\n'.join(PROGRAM)] + [ord('\n')]
    comp.run_whole_code(input_string)
    output = comp.get_output()
    return int(output[-1])


def solve_part2(data: str) -> int:
    PROGRAM = [
        # |   @@@ @@@       |
        # |  @   @   @      |
        # |#####.##.##.#.###|
        # |     CD   H      |
        'NOT C J',
        'AND D J',
        'AND H J',
        # |       @@@       |
        # |      @   @      |
        # |#####.##.##.#.###|
        # |        B D      |
        'NOT B T',
        'AND D T',
        'OR T J',
        # |           @@@   |
        # |          @   @  |
        # |#####.##.##.#.###|
        # |           A     |
        'NOT A T',
        'OR T J',
        'RUN',
    ]
    comp = IntcodeComp(data)
    input_string = [ord(char) for char in '\n'.join(PROGRAM)] + [ord('\n')]
    comp.run_whole_code(input_string)
    output = comp.get_output()
    output_text = ''.join([chr(c) for c in output[:-1]])
    print(output_text)
    return int(output[-1])


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
