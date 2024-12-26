from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_02 import (
    IntcodeComp,
    read_data,
    solve_part1,
)


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
    ],
)
def test_solution_part1(inputs: str, expected: int) -> None:
    data = list(map(int, inputs.split(',')))
    assert solve_part1(data) == expected
