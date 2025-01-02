import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp


def read_data(file_path: str) -> str:
    with open(file_path) as f:
        data = f.read().strip()
    return data


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        comp = IntcodeComp(data)
        comp.run_whole_code(input_data=[1])
        res1 = comp.pop_output()
        print('Part 1:', res1, res1 == 2738720997)
        print(time.monotonic() - start)

        start = time.monotonic()
        comp = IntcodeComp(data)
        comp.run_whole_code(input_data=[2])
        res2 = comp.pop_output()
        print('Part 2:', res2, res2 == 50894)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
