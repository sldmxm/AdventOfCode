from unittest.mock import mock_open, patch

import pytest

from year_2019.year_2019_day_18 import (
    read_data,
    solve_part1,
    solve_part2,
)

TEST_DATA1 = """#########
#b.A.@.a#
#########
"""
TEST_DATA2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""
TEST_DATA3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""
TEST_DATA4 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
TEST_DATA5 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""
TEST_DATA2_1 = """#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#.b#
#######
"""
TEST_DATA2_2 = """###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
"""
TEST_DATA2_3 = """#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
"""
TEST_DATA2_4 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
"""


@pytest.mark.parametrize(
    'mock_file_content, expected',
    [
        (TEST_DATA1, 8),
        (TEST_DATA2, 86),
        (TEST_DATA3, 132),
        (TEST_DATA5, 81),
        (TEST_DATA4, 136),
    ],
)
def test_part1(mock_file_content: str, expected: int) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert solve_part1(data) == expected


@pytest.mark.parametrize(
    'mock_file_content, expected',
    [
        (TEST_DATA2_1, 8),
        (TEST_DATA2_2, 24),
        (TEST_DATA2_3, 32),
        (TEST_DATA2_4, 72),
    ],
)
def test_part2(mock_file_content: str, expected: int) -> None:
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        data = read_data('dummy_path.txt')
    assert solve_part2(data) == expected
