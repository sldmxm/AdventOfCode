from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_02 import (
    IntcodeComp,
    read_data,
    solve_part1,
    solve_part2,
)

TEST_DATA = """
            1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,
            1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,
            2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,
            87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,
            5,115,1,115,2,119,1,119,6,0,99,2,0,14,0
            """


@pytest.mark.parametrize(
    'mock_file_content,expected',
    [
        ('661,62,553,444,35', [661, 62, 553, 444, 35]),
    ],
)
def test_read_data(mock_file_content: str, expected: list[int]) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = read_data('dummy_path.txt')
    assert result == expected


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        ['1,9,10,3,2,3,11,0,99,30,40,50', '3500,9,10,70,2,3,11,0,99,30,40,50'],
        ['1,0,0,0,99', '2,0,0,0,99'],
        ['2,3,0,3,99', '2,3,0,6,99'],
        ['2,4,4,5,99,0', '2,4,4,5,99,9801'],
        ['1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99'],
    ],
)
def test_intcode_comp(inputs: str, expected: str) -> None:
    data = list(map(int, inputs.split(',')))
    comp = IntcodeComp(data)
    assert comp.run_whole_code() == list(map(int, expected.split(',')))


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        ['1,9,10,3,2,3,11,0,99,30,40,50', 3500],
        ['1,0,0,0,99', 2],
        ['2,3,0,3,99', 2],
        ['2,4,4,5,99,0', 2],
        ['1,1,1,4,99,5,6,0,99', 30],
        [TEST_DATA, 3516593],
    ],
)
def test_solution_part1(inputs: str, expected: int) -> None:
    data = list(map(int, inputs.split(',')))
    assert solve_part1(data) == expected


def test_solution_part2() -> None:
    data = list(map(int, TEST_DATA.split(',')))
    assert solve_part2(data, goal=19690720) == 7749
