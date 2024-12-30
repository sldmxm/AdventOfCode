import time
import typing
from dataclasses import dataclass

from utils.download_data import download_data


@dataclass
class Instruction:
    opcode: int
    offset_after: int
    parameters_pos: tuple[int, int] | None = None
    output_pos: int | None = None
    command: typing.Callable[[int, int], int] | None = None


class IntcodeComp:
    _ADD = Instruction(
        opcode=1,
        parameters_pos=(1, 2),
        offset_after=4,
        output_pos=3,
        command=lambda a, b: a + b,
    )
    _MUL = Instruction(
        opcode=2,
        parameters_pos=(1, 2),
        offset_after=4,
        output_pos=3,
        command=lambda a, b: a * b,
    )
    _HALT = Instruction(
        opcode=99,
        offset_after=1,
    )
    _OPERATIONS = {
        _ADD.opcode: _ADD,
        _MUL.opcode: _MUL,
        _HALT.opcode: _HALT,
    }

    def __init__(self, code: list[int]) -> None:
        self._memory: list[int] = code
        self._pointer = 0

    def run_whole_code(self) -> list[int]:
        while self._memory[self._pointer] != IntcodeComp._HALT.opcode:
            instruction = IntcodeComp._OPERATIONS[self._memory[self._pointer]]
            if (
                instruction.parameters_pos is not None
                and instruction.command is not None
            ):
                parameters = (
                    self._memory[self._memory[self._pointer + pos]]
                    for pos in instruction.parameters_pos
                )
                result = instruction.command(*parameters)
                if instruction.output_pos is not None:
                    result_position = self._memory[
                        self._pointer + instruction.output_pos
                    ]
                    self._memory[result_position] = result
            self._pointer += instruction.offset_after
        return self._memory


def read_data(file_path: str) -> list[int]:
    with open(file_path) as f:
        line = f.read()
    data = [int(n) for n in line.strip().split(',')]
    return data


def solve_part1(data: list[int]) -> int:
    comp = IntcodeComp(code=data[:])
    return comp.run_whole_code()[0]


def solve_part2(data: list[int], goal: int) -> int | None:
    for noun in range(100):
        for verb in range(100):
            new_data = data[:]
            new_data[1:3] = [noun, verb]
            comp = IntcodeComp(code=new_data)
            if comp.run_whole_code()[0] == goal:
                return 100 * noun + verb
    return None


def main() -> None:
    data_file_path = None
    try:
        data_file_path = download_data(__file__)
    except Exception as e:
        print(f'ERROR: {e}')

    if data_file_path:
        data = read_data(data_file_path)

        start = time.monotonic()
        res = solve_part1(data)
        print('Part 1:', res)
        print(time.monotonic() - start)

        start = time.monotonic()
        res2 = solve_part2(data, goal=19690720)
        print('Part 2:', res2)
        print(time.monotonic() - start)


if __name__ == '__main__':
    main()
