from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_03 import read_data, solve_part1, solve_part2


@pytest.mark.parametrize(
    'mock_file_content,expected',
    [
        (
            'a661,d62,f553,g444,e35\nf23,d44,e55,g66,r55',
            [
                ['a661', 'd62', 'f553', 'g444', 'e35'],
                ['f23', 'd44', 'e55', 'g66', 'r55'],
            ],
        ),
    ],
)
def test_read_data(mock_file_content: str, expected: list[list[str]]) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = read_data('dummy_path.txt')
    assert result == expected


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        [
            'R75,D30,R83,U83,L12,D49,R71,U7,L72\n'
            'U62,R66,U55,R34,D71,R55,D58,R83',
            159,
        ],
        [
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
            135,
        ],
    ],
)
def test_solution_part1(inputs: str, expected: int) -> None:
    data = [line.strip().split(',') for line in inputs.split('\n')]
    assert solve_part1(data) == expected


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        [
            'R75,D30,R83,U83,L12,D49,R71,U7,L72\n'
            'U62,R66,U55,R34,D71,R55,D58,R83',
            610,
        ],
        [
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
            410,
        ],
    ],
)
def test_solution_part2(inputs: str, expected: int) -> None:
    data = [line.strip().split(',') for line in inputs.split('\n')]
    assert solve_part2(data) == expected
