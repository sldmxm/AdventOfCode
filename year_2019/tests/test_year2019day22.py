from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_22 import (
    read_data,
    shuffle,
    # solve_part2,
)


@pytest.mark.parametrize(
    'mock_file_content, expected',
    [
        (
            """
                deal with increment 7
                deal into new stack
                deal into new stack
                """,
            '0 3 6 9 2 5 8 1 4 7',
        ),
        (
            """
                cut 6
                deal with increment 7
                deal into new stack
                """,
            '3 0 7 4 1 8 5 2 9 6',
        ),
        (
            """
                deal with increment 7
                deal with increment 9
                cut -2
                """,
            '6 3 0 7 4 1 8 5 2 9',
        ),
        (
            """
                deal into new stack
                cut -2
                deal with increment 7
                cut 8
                cut -4
                deal with increment 7
                cut 3
                deal with increment 9
                deal with increment 3
                cut -1
                """,
            '9 2 5 8 1 4 7 0 3 6',
        ),
    ],
)
def test_parse_portals(mock_file_content: str, expected: str) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert ' '.join(map(str, shuffle(data, 10))) == expected
