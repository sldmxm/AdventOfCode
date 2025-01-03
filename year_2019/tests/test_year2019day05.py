from unittest.mock import mock_open, patch

import pytest

from year_2019.intcode import IntcodeComp
from year_2019.year_2019_day_05 import read_data

TEST_DATA_DAY_2 = """
            1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,
            1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,
            2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,
            87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,
            5,115,1,115,2,119,1,119,6,0,99,2,0,14,0
            """
TEST_DATA_DAY_5 = """
            3,225,1,225,6,6,1100,1,238,225,104,0,1101,33,37,225,101,6,218,224,1001,224,
            -82,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1102,87,62,225,1102,
            75,65,224,1001,224,-4875,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,
            223,1102,49,27,225,1101,6,9,225,2,69,118,224,101,-300,224,224,4,224,102,8,
            223,223,101,6,224,224,1,224,223,223,1101,76,37,224,1001,224,-113,224,4,224,
            1002,223,8,223,101,5,224,224,1,224,223,223,1101,47,50,225,102,43,165,224,1001,
            224,-473,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1002,39,86,224,
            101,-7482,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,11,82,
            225,1,213,65,224,1001,224,-102,224,4,224,1002,223,8,223,1001,224,6,224,1,224,
            223,223,1001,14,83,224,1001,224,-120,224,4,224,1002,223,8,223,101,1,224,224,
            1,223,224,223,1102,53,39,225,1101,65,76,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,
            0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,
            1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,
            1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,
            1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,
            677,226,224,1002,223,2,223,1005,224,329,101,1,223,223,8,677,226,
            224,102,2,223,223,1006,224,344,1001,223,1,223,108,677,677,224,
            1002,223,2,223,1006,224,359,1001,223,1,223,1108,226,677,224,102,
            2,223,223,1006,224,374,1001,223,1,223,1008,677,226,224,102,2,223,
            223,1005,224,389,101,1,223,223,7,226,677,224,102,2,223,223,1005,
            224,404,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,
            419,101,1,223,223,107,677,226,224,102,2,223,223,1006,224,434,101,
            1,223,223,7,677,677,224,1002,223,2,223,1005,224,449,101,1,223,223,
            108,677,226,224,1002,223,2,223,1006,224,464,101,1,223,223,1008,226,
            226,224,1002,223,2,223,1006,224,479,101,1,223,223,107,677,677,224,
            1002,223,2,223,1006,224,494,1001,223,1,223,1108,677,226,224,102,2,
            223,223,1005,224,509,101,1,223,223,1007,226,677,224,102,2,223,223,
            1005,224,524,1001,223,1,223,1008,677,677,224,102,2,223,223,1005,224,
            539,1001,223,1,223,1107,677,677,224,1002,223,2,223,1006,224,554,
            1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,569,1001,
            223,1,223,7,677,226,224,1002,223,2,223,1006,224,584,1001,223,1,
            223,108,226,226,224,102,2,223,223,1005,224,599,1001,223,1,223,8,
            677,677,224,102,2,223,223,1005,224,614,1001,223,1,223,1107,226,
            677,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,677,224,
            102,2,223,223,1006,224,644,1001,223,1,223,1108,226,226,224,1002,
            223,2,223,1006,224,659,101,1,223,223,107,226,226,224,1002,223,2,
            223,1006,224,674,1001,223,1,223,4,223,99,226
            """
LARGER_EXAMPLE = """
            3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
            999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
            """


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
def test_base_intcode_comp(inputs: str, expected: str) -> None:
    data = list(map(int, inputs.split(',')))
    comp = IntcodeComp(data)
    comp.run_whole_code()
    assert comp.get_memory() == list(map(int, expected.split(',')))


def test_base_intcode_comp_data_day_2() -> None:
    data = list(map(int, TEST_DATA_DAY_2.split(',')))
    comp = IntcodeComp(data)
    comp.run_whole_code()
    assert comp.get_memory()[0] == 3516593


@pytest.mark.parametrize(
    ('data', 'inp_data', 'expected_code', 'expected_output'),
    [
        ['3,0,4,0,99', 157, '157,0,4,0,99', [157]],
        ['1002,4,3,4,33', None, '1002,4,3,4,99', []],
        ['1101,100,-1,4,0', None, '1101,100,-1,4,99', []],
    ],
)
def test_intcode_comp_inp_out(
    data: str, inp_data: int, expected_code: str, expected_output: list[int]
) -> None:
    code = list(map(int, data.split(',')))
    comp = IntcodeComp(code)
    comp.run_whole_code([inp_data])
    assert comp.get_memory() == list(map(int, expected_code.split(',')))
    assert comp.get_output() == expected_output


@pytest.mark.parametrize(
    ('data', 'expected_code'),
    [
        ['101,1,5,5,1105,-3,0,99', '101,1,5,5,1105,0,0,99'],
        ['101,1,5,5,1106,-1,0,99', '101,1,5,5,1106,1,0,99'],
        ['101,1,5,5,105,-3,8,99,0', '101,1,5,5,105,0,8,99,0'],
    ],
)
def test_v02_intcode_comp_jump_instructions(
    data: str, expected_code: str
) -> None:
    code = list(map(int, data.split(',')))
    comp = IntcodeComp(code)
    comp.run_whole_code()
    assert comp.get_memory() == list(map(int, expected_code.split(',')))


@pytest.mark.parametrize(
    ('data', 'input_data', 'output'),
    [
        ['3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 157, [1]],
        ['3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', 0, [0]],
        ['3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 157, [1]],
        ['3,3,1105,-1,9,1101,0,0,12,4,12,99,1', 0, [0]],
    ],
)
def est_v02_intcode_comp_jump_instructions_with_input(
    data: str, input_data: int, expected_output: list[int]
) -> None:
    code = list(map(int, data.split(',')))
    comp = IntcodeComp(code)
    comp.run_whole_code([input_data])
    assert comp.get_output() == expected_output


@pytest.mark.parametrize(
    ('data', 'input_data', 'expected_output'),
    [
        ['3,9,8,9,10,9,4,9,99,-1,8', 8, [1]],
        ['3,9,8,9,10,9,4,9,99,-1,8', 1, [0]],
        ['3,9,7,9,10,9,4,9,99,-1,8', 1, [1]],
        ['3,9,7,9,10,9,4,9,99,-1,8', 157, [0]],
        ['3,3,1108,-1,8,3,4,3,99', 8, [1]],
        ['3,3,1108,-1,8,3,4,3,99', 157, [0]],
        ['3,3,1107,-1,8,3,4,3,99', 1, [1]],
        ['3,3,1107,-1,8,3,4,3,99', 115, [0]],
        [LARGER_EXAMPLE, 0, [999]],
        [LARGER_EXAMPLE, 8, [1000]],
        [LARGER_EXAMPLE, 157, [1001]],
    ],
)
def test_intcode_comp_lt_eq_instructions(
    data: str, input_data: int, expected_output: list[int]
) -> None:
    code = list(map(int, data.split(',')))
    comp = IntcodeComp(code)
    comp.run_whole_code([input_data])
    assert comp.get_output() == expected_output


def test_solve_part1() -> None:
    code = list(map(int, TEST_DATA_DAY_5.split(',')))
    comp = IntcodeComp(code)
    comp.run_whole_code([1])
    assert comp.get_output()[-1] == 16209841


def test_solve_part2() -> None:
    code = list(map(int, TEST_DATA_DAY_5.split(',')))
    comp = IntcodeComp(code)
    comp.run_whole_code([5])
    assert comp.get_output()[-1] == 8834787
