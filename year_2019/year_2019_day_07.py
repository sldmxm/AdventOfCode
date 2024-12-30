import itertools
import time

from utils.download_data import download_data
from year_2019.intcode import IntcodeComp, ProgramStatus


def read_data(file_path: str) -> list[int]:
    with open(file_path) as f:
        line = f.read()
    data = [int(n) for n in line.strip().split(',')]
    return data


def solve_part1(
    data: list[int], combination: tuple[int, ...] | None = None
) -> int:
    combinations: (
        itertools.permutations[tuple[int, ...]] | tuple[tuple[int, ...]]
    )
    if not combination:
        combinations = itertools.permutations(range(0, 5))
    else:
        combinations = (combination,)
    res = 0
    for combination in combinations:
        output = None
        for n in combination:
            comp = IntcodeComp(code=data[:])
            comp.run_whole_code([n, output or 0])
            output = comp.pop_output()
        if output:
            res = max(res, output)
    return res


def solve_part2(
    data: list[int], combination: tuple[int, ...] | None = None
) -> int:
    combinations: (
        itertools.permutations[tuple[int, ...]] | tuple[tuple[int, ...]]
    )
    if not combination:
        combinations = itertools.permutations((range(5, 10)))
    else:
        combinations = (combination,)
    res = 0
    for combination in combinations:
        comps = []
        output = None
        for n in combination:
            comps.append(IntcodeComp(code=data[:]))
            comps[-1].run_whole_code([n, output or 0])
            output = comps[-1].pop_output()
        cur_comp_num = 0
        while comps[-1].get_status() != ProgramStatus.DONE:
            comp = comps[cur_comp_num]
            comp.run_whole_code([output or 0])
            output = comp.pop_output()
            cur_comp_num = (cur_comp_num + 1) % len(comps)

        if output:
            res = max(res, output)
    return res


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
        print('Part 1:', res1, res1 == 14902)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data)
        print('Part 2:', res2, res2 == 6489132)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
