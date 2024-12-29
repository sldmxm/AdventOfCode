from year_2019.year_2019_day_08 import (
    solve_part1,
    solve_part2,
)


def test_part1() -> None:
    assert solve_part1('123456789012', 3, 2) == 1


def test_part2() -> None:
    assert solve_part2('0222112222120000', 2, 2) == [[0, 1], [1, 0]]
