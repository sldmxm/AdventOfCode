from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class OffsetMode(Enum):
    RELATIVE = 0
    ABSOLUTE = 1


class Channel(Enum):
    MEMORY = 'memory'
    OUTSIDE = 'outside'
    NONE = 'none'


class ProgramStatus(Enum):
    RESET = 0
    DONE = 99
    WAITING_INPUT = 3


@dataclass
class Program:
    memory: list[int]
    pointer: int
    input: deque[int]
    output: list[int]
    status: ProgramStatus


@dataclass(frozen=True)
class Instruction:
    name: str
    opcode: int
    parameters_num: int
    parameters_channel: Channel
    output_channel: Channel
    offset_mode: OffsetMode = OffsetMode.RELATIVE
    command: Optional[Callable[..., int]] = None

    def _write_output(self, program: Program, result: int) -> None:
        match self.output_channel:
            case Channel.MEMORY:
                result_position = program.memory[
                    program.pointer
                    + self.parameters_num
                    + 1
                    - (1 if self.parameters_channel == Channel.OUTSIDE else 0)
                ]
                program.memory[result_position] = result
            case Channel.OUTSIDE:
                program.output.append(result)

    def _get_parameters(
        self, program: Program
    ) -> tuple[int, ...] | tuple[int | None]:
        match self.parameters_channel:
            case Channel.MEMORY:
                instruction = str(program.memory[program.pointer])
                modes = instruction[-3::-1]
                modes += '0' * (self.parameters_num - len(modes))
                parameters: list[int] = []
                first_position = program.pointer + 1
                for i in range(self.parameters_num):
                    match int(modes[i]):
                        case ParameterMode.POSITION.value:
                            parameter_position = program.memory[
                                first_position + i
                            ]
                            parameters.append(
                                program.memory[parameter_position]
                            )
                        case ParameterMode.IMMEDIATE.value:
                            parameters.append(
                                program.memory[first_position + i]
                            )
                return tuple(parameters)
            case Channel.OUTSIDE:
                return (program.input.popleft(),)
        raise ValueError(f"Can't get parameters for {self.name} operation")

    def _get_instruction_len(self) -> int:
        result = 1
        result += self.parameters_num
        result -= 1 if self.parameters_channel == Channel.OUTSIDE else 0
        result += 1 if self.output_channel == Channel.MEMORY else 0
        return result

    def _move_pointer(self, program: Program) -> None:
        match self.offset_mode:
            case OffsetMode.RELATIVE:
                program.pointer += self._get_instruction_len()
            case OffsetMode.ABSOLUTE:
                parameters = self._get_parameters(program)
                if parameters and len(parameters) == 2:
                    parameter, new_pointer = parameters
                    result = self.command(parameter) if self.command else None
                    if result:
                        program.pointer = new_pointer
                    else:
                        program.pointer += self._get_instruction_len()
                else:
                    raise ValueError(
                        f'Insufficient parameters for {self.name} operation'
                    )

    def run(self, program: Program) -> None:
        if (
            self.parameters_channel != Channel.NONE
            and self.output_channel != Channel.NONE
            and self.command
        ):
            parameters = self._get_parameters(program)
            result = self.command(*parameters)
            self._write_output(program, result)
        self._move_pointer(program)


class IntcodeComp:
    _ADD = Instruction(
        name='ADD',
        opcode=1,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.MEMORY,
        command=lambda a, b: a + b,
    )
    _MUL = Instruction(
        name='MUL',
        opcode=2,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.MEMORY,
        command=lambda a, b: a * b,
    )
    _HLT = Instruction(
        name='HLT',
        opcode=99,
        parameters_num=0,
        parameters_channel=Channel.NONE,
        output_channel=Channel.NONE,
    )
    _INP = Instruction(
        name='INP',
        opcode=3,
        parameters_num=1,
        parameters_channel=Channel.OUTSIDE,
        output_channel=Channel.MEMORY,
        command=lambda a: a,
    )
    _OUT = Instruction(
        name='OUT',
        opcode=4,
        parameters_num=1,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.OUTSIDE,
        command=lambda a: a,
    )
    _JIT = Instruction(
        name='JIT',
        opcode=5,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.NONE,
        offset_mode=OffsetMode.ABSOLUTE,
        command=lambda a: a != 0,
    )
    _JIF = Instruction(
        name='JIF',
        opcode=6,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.NONE,
        offset_mode=OffsetMode.ABSOLUTE,
        command=lambda a: a == 0,
    )
    _LT = Instruction(
        name='LT',
        opcode=7,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.MEMORY,
        command=lambda a, b: 1 if a < b else 0,
    )
    _EQ = Instruction(
        name='EQ',
        opcode=8,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.MEMORY,
        command=lambda a, b: 1 if a == b else 0,
    )

    _OPERATIONS = {
        _ADD.opcode: _ADD,
        _MUL.opcode: _MUL,
        _HLT.opcode: _HLT,
        _INP.opcode: _INP,
        _OUT.opcode: _OUT,
        _JIT.opcode: _JIT,
        _JIF.opcode: _JIF,
        _LT.opcode: _LT,
        _EQ.opcode: _EQ,
    }

    def __init__(self, code: list[int]) -> None:
        self._program: Program = Program(
            memory=code,
            pointer=0,
            input=deque([]),
            output=[],
            status=ProgramStatus.RESET,
        )

    def run_whole_code(
        self, input_data: list[int] | None = None
    ) -> ProgramStatus:
        if input_data:
            self._program.input.extend(input_data)
        while True:
            op_code = int(
                str(self._program.memory[self._program.pointer])[-2:]
            )
            instruction = IntcodeComp._OPERATIONS[op_code]
            if (
                (done := instruction == IntcodeComp._HLT)
                or instruction == IntcodeComp._INP
                and not self._program.input
            ):
                self._program.status = (
                    ProgramStatus.DONE if done else ProgramStatus.WAITING_INPUT
                )
                return self._program.status
            instruction.run(self._program)

    def get_memory(self) -> list[int]:
        return self._program.memory

    def get_output(self) -> list[int]:
        return self._program.output

    def pop_output(self) -> int:
        return self._program.output.pop()

    def get_status(self) -> ProgramStatus:
        return self._program.status
