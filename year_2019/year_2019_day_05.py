import time

from utils.download_data import check_and_download_data
from year_2019.intcode import IntcodeComp


def read_data(file_path: str) -> list[int]:
    with open(file_path) as f:
        line = f.read()
    data = [int(n) for n in line.strip().split(',')]
    return data


def solve(data: list[int], input_data: int) -> list[int]:
    comp = IntcodeComp(code=data[:])
    comp.run_whole_code(input_data=[input_data])
    return comp.get_output()


def main() -> None:
    data_file_path = None
    try:
        data_file_path = check_and_download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res1 = solve(data, 1)
        print('Part 1:', res1)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve(data, 5)
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
