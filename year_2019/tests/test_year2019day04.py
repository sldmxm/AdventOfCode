import pytest

from year_2019.year_2019_day_04 import (
    is_number_ok_part1,
    is_number_ok_part2,
    solve,
)


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        [122345, True],
        [111123, True],
        [111111, True],
        [223450, False],
        [123789, False],
    ],
)
def test_is_number_ok_part1(inputs: int, expected: bool) -> None:
    assert is_number_ok_part1(inputs) == expected


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        [112233, True],
        [123444, False],
        [111122, True],
        [111111, False],
        [113444, True],
    ],
)
def test_is_number_ok_part2(inputs: int, expected: bool) -> None:
    assert is_number_ok_part2(inputs) == expected


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        ['372037-905157', 481],
    ],
)
def test_solution_part1(inputs: str, expected: int) -> None:
    assert solve(inputs)[0] == expected


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        ['372037-905157', 299],
    ],
)
def test_solution_part2(inputs: str, expected: int) -> None:
    assert solve(inputs)[1] == expected
