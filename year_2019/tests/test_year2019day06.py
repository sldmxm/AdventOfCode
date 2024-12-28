from year_2019.year_2019_day_06 import (
    solve_part1,
    solve_part2,
)

TEST_DATA_PART1 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

TEST_DATA_PART2 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""


def test_solve_part1() -> None:
    data = [line.strip() for line in TEST_DATA_PART1.strip().split('\n')]
    assert solve_part1(data) == 42


def test_solve_part2() -> None:
    data = [line.strip() for line in TEST_DATA_PART2.strip().split('\n')]
    assert solve_part2(data) == 4
