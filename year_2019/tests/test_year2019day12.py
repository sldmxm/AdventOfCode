from unittest.mock import mock_open, patch

from year_2019.year_2019_day_12 import (
    read_data,
    solve_part1,
    solve_part2,
)

TEST_DATA = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""


def test_part1() -> None:
    with patch('builtins.open', mock_open(read_data=TEST_DATA)):
        data = read_data('dummy_path.txt')
    assert solve_part1(data, 10) == 179


def test_part2() -> None:
    with patch('builtins.open', mock_open(read_data=TEST_DATA)):
        data = read_data('dummy_path.txt')
    assert solve_part2(data) == 2772
