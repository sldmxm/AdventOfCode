from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class OffsetAfterInstruction(Enum):
    STANDARD = 0
    GO_TO = 1


class Channel(Enum):
    MEMORY = 10
    OUTSIDE = 20
    PROGRAM_RELATIVE_BASE = 21
    NONE = 0


class ProgramStatus(Enum):
    RESET = 0
    RUNNING = 1
    DONE = 99
    WAITING_INPUT = 3


@dataclass
class Parameter:
    address: int
    value: int


@dataclass
class Program:
    memory: dict[int, int]
    pointer: int
    input: deque[int]
    output: list[int]
    status: ProgramStatus
    relative_base: int
    debug_mode: bool = False


def _log(message: str, program: Program) -> None:
    if program.debug_mode:
        print(message)


@dataclass(frozen=True)
class Instruction:
    name: str
    opcode: int
    parameters_num: int
    parameters_channel: Channel
    output_channel: Channel
    offset_mode: OffsetAfterInstruction = OffsetAfterInstruction.STANDARD
    command: Optional[Callable[..., int]] = None

    def _get_parameter_offset(
        self, parameter_number: int, program: Program
    ) -> int:
        def read_offset_modes() -> str:
            instruction = str(program.memory[program.pointer])
            modes = instruction[-3::-1]
            modes += '0' * (self.parameters_num - len(modes))
            modes += '0' if self.output_channel == Channel.MEMORY else ''
            _log(
                f'Instruction: {instruction}. Parameter modes: {modes}',
                program,
            )
            return modes

        offset_modes = read_offset_modes()
        first_position = program.pointer + 1
        mode = int(offset_modes[parameter_number])
        match mode:
            case ParameterMode.POSITION.value:
                _log(
                    f'Parameter offset via POSITION mode'
                    f' {program.memory.get(
                        first_position + parameter_number)}',
                    program,
                )
                return program.memory[first_position + parameter_number]
            case ParameterMode.IMMEDIATE.value:
                _log(
                    f'Parameter offset via IMMEDIATE mode'
                    f' {first_position + parameter_number}',
                    program,
                )
                return first_position + parameter_number
            case ParameterMode.RELATIVE.value:
                _log(
                    f'Parameter offset via RELATIVE mode'
                    f' {program.relative_base
                        + program.memory[
                            first_position + parameter_number
                            ]}',
                    program,
                )
                return (
                    program.relative_base
                    + program.memory[first_position + parameter_number]
                )
        raise ValueError(f'Unknown parameter mode: {mode}')

    def _get_parameters(self, program: Program) -> tuple[int, ...]:
        match self.parameters_channel:
            case Channel.MEMORY:
                parameters = []
                for i in range(self.parameters_num):
                    offset = self._get_parameter_offset(i, program)
                    parameters.append(program.memory.get(offset, 0))
                _log(f'Params: {parameters}', program)
                return tuple(parameters)
            case Channel.OUTSIDE:
                _log(f'Param from inputs: {program.input[0]}', program)
                return (program.input.popleft(),)
        raise ValueError(
            f'Unknown channel for parameter: {self.parameters_channel}'
        )

    def _write_output(self, program: Program, result: int) -> None:
        _log(f'Writing output: {result} to {self.output_channel}', program)
        match self.output_channel:
            case Channel.MEMORY:
                output_parameter_position = self.parameters_num - (
                    1 if self.parameters_channel == Channel.OUTSIDE else 0
                )

                output_offset = self._get_parameter_offset(
                    output_parameter_position, program
                )
                _log(
                    f'Mem {output_offset}: '
                    f'{program.memory.get(output_offset)} -> {result}',
                    program,
                )
                program.memory[output_offset] = result
            case Channel.OUTSIDE:
                program.output.append(result)
                _log(f'Program output: {program.output}', program)
            case Channel.PROGRAM_RELATIVE_BASE:
                program.relative_base += result
                _log(
                    f'Program relative base: {program.relative_base}', program
                )

    def _get_instruction_len(self) -> int:
        result = 1
        result += self.parameters_num
        result -= 1 if self.parameters_channel == Channel.OUTSIDE else 0
        result += 1 if self.output_channel == Channel.MEMORY else 0
        return result

    def _move_pointer(self, program: Program) -> None:
        old_pointer = program.pointer
        match self.offset_mode:
            case OffsetAfterInstruction.STANDARD:
                program.pointer += self._get_instruction_len()
            case OffsetAfterInstruction.GO_TO:
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
        _log(
            f'Pointer after {self.name}: '
            f'{old_pointer} -> {program.pointer} \n',
            program,
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
        offset_mode=OffsetAfterInstruction.GO_TO,
        command=lambda a: a != 0,
    )
    _JIF = Instruction(
        name='JIF',
        opcode=6,
        parameters_num=2,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.NONE,
        offset_mode=OffsetAfterInstruction.GO_TO,
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
    _CRB = Instruction(
        name='CRB',
        opcode=9,
        parameters_num=1,
        parameters_channel=Channel.MEMORY,
        output_channel=Channel.PROGRAM_RELATIVE_BASE,
        command=lambda a: a,
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
        _CRB.opcode: _CRB,
    }

    def __init__(self, code: list[int] | str) -> None:
        self._program: Program = Program(
            memory={},
            pointer=0,
            input=deque([]),
            output=[],
            status=ProgramStatus.RESET,
            relative_base=0,
        )
        if isinstance(code, str):
            code = list(map(int, code.split(',')))
        self._program.memory = {
            address: value for address, value in enumerate(code)
        }

    def _log(self, message: str) -> None:
        if self._program.debug_mode:
            print(message)

    def run_whole_code(
        self, input_data: list[int] | None = None, debug_mode: bool = False
    ) -> ProgramStatus:
        self._program.debug_mode = debug_mode
        if input_data:
            self._program.input.extend(input_data)
        self._program.status = ProgramStatus.RUNNING
        while True:
            op_code = int(
                str(self._program.memory[self._program.pointer])[-2:]
            )
            instruction = IntcodeComp._OPERATIONS[op_code]
            self._log(
                f'Executing instruction: '
                f'{instruction.name} at pointer {self._program.pointer}'
            )
            self._log(
                f'Code: {
                self.get_memory()[
                self._program.pointer:self._program.pointer + 4]}'
            )
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
        return [
            val
            for _, val in sorted(
                [(k, v) for k, v in self._program.memory.items()]
            )
        ]

    def get_memory_as_dict(self) -> dict[int, int]:
        return self._program.memory

    def get_output(self) -> list[int]:
        return self._program.output

    def pop_output(self) -> int:
        return self._program.output.pop()

    def get_status(self) -> ProgramStatus:
        return self._program.status
