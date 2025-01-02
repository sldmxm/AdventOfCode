from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_10 import (
    read_data,
    solve_part1,
    solve_part2,
)

TEST_DATA = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""


@pytest.mark.parametrize(
    'mock_file_content,expected',
    [
        ('.#..#\n.....\n#####\n....#\n...##', 8),
        (
            """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""",
            33,
        ),
        (
            """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""",
            35,
        ),
        (
            """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""",
            41,
        ),
        (TEST_DATA, 210),
    ],
)
def test_part1(mock_file_content: str, expected: int) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert solve_part1(data) == expected


@pytest.mark.parametrize(
    'mock_file_content,expected',
    [
        (TEST_DATA, 802),
    ],
)
def test_part2(mock_file_content: str, expected: int) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert solve_part2(data) == expected
