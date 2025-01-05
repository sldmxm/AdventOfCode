from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_16 import (
    read_data,
    solve_part1,
    solve_part2,
)


@pytest.mark.parametrize(
    'mock_file_content, phases, expected',
    [
        ('12345678', 4, '01029498'),
        ('80871224585914546619083218645595', 100, '24176176'),
        ('19617804207202209144916044189917', 100, '73745418'),
        ('69317163492948606335995924319873', 100, '52432133'),
    ],
)
def test_part1(mock_file_content: str, phases: int, expected: str) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert solve_part1(data, phases) == expected


@pytest.mark.parametrize(
    'mock_file_content, phases, expected',
    [
        ('03036732577212944063491565474664', 100, '84462026'),
        ('02935109699940807407585447034323', 100, '78725270'),
        ('03081770884921959731165446850517', 100, '53553731'),
    ],
)
def test_part2(mock_file_content: str, phases: int, expected: str) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert solve_part2(data, phases) == expected
