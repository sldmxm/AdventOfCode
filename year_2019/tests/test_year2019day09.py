from year_2019.intcode import IntcodeComp

# from year_2019.year_2019_day_09 import (
#     solve_part1,
#     solve_part2,
# )


def test_solve_new_intcode_same_code() -> None:
    data = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    comp = IntcodeComp(data)
    comp.run_whole_code()
    output = ','.join(map(str, comp.get_output()))
    assert output == data


def test_solve_new_intcode2() -> None:
    data = '1102,34915192,34915192,7,4,7,99,0'
    comp = IntcodeComp(data)
    comp.run_whole_code()
    output = str(comp.pop_output())
    assert len(output) == 16


def test_solve_new_intcode3() -> None:
    data = '104,1125899906842624,99'
    comp = IntcodeComp(data)
    comp.run_whole_code()
    output = comp.pop_output()
    assert output == 1125899906842624
