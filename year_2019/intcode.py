from abc import abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional, Type


class ProgramStatus(Enum):
    RESET = auto()
    RUNNING = auto()
    DONE = auto()
    WAITING_INPUT = auto()


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass
class InstructionResult:
    next_pointer: int
    status: ProgramStatus = ProgramStatus.RUNNING


@dataclass
class Memory:
    data: dict[int, int] = field(default_factory=lambda: {0: 0})
    relative_base: int = 0

    def _get_address_by_mode(self, address: int, mode: ParameterMode) -> int:
        match mode:
            case ParameterMode.POSITION:
                return self.data[address]
            case ParameterMode.IMMEDIATE:
                return address
            case ParameterMode.RELATIVE:
                return self.relative_base + self.data[address]
        raise ValueError(f'Unknown parameter mode: {mode}')

    def read(self, address: int, mode: ParameterMode) -> int:
        read_address = self._get_address_by_mode(address, mode)
        return self.data.get(read_address, 0)

    def write(self, address: int, value: int, mode: ParameterMode) -> None:
        write_address = self._get_address_by_mode(address, mode)
        self.data[write_address] = value

    def load_code(self, code: list[int]) -> None:
        self.data = {address: value for address, value in enumerate(code)}

    def read_all(self) -> dict[int, int]:
        return self.data.copy()


@dataclass
class ExecutionContext:
    pointer: int
    input_queue: deque[int] = field(default_factory=deque)
    output_list: list[int] = field(default_factory=list)
    status: ProgramStatus = ProgramStatus.RESET
    debug_mode: bool = False

    def read_input(self) -> Optional[int]:
        if not self.input_queue:
            self.status = ProgramStatus.WAITING_INPUT
            return None
        return self.input_queue.popleft()

    def write_output(self, value: int) -> None:
        self.output_list.append(value)

    def load_input(self, *values: int) -> None:
        self.input_queue.extend(values)
        if self.status == ProgramStatus.WAITING_INPUT:
            self.status = ProgramStatus.RUNNING

    def get_output(self) -> list[int]:
        return self.output_list

    def pop_output(self) -> int:
        return self.output_list.pop()

    def clear_output(self) -> None:
        self.output_list.clear()


class InstructionBase:
    @property
    @abstractmethod
    def parameter_count(self) -> int:
        pass

    @abstractmethod
    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        pass

    def _read_parameter_modes(
        self, memory: Memory, context: ExecutionContext
    ) -> list[ParameterMode]:
        instruction = memory.read(context.pointer, ParameterMode.IMMEDIATE)
        modes_int = instruction // 100
        modes = []
        while modes_int:
            modes.append(ParameterMode(modes_int % 10))
            modes_int //= 10
        return modes + [ParameterMode.POSITION] * (
            self.parameter_count - len(modes)
        )

    def execute(self, memory: Memory, context: ExecutionContext) -> None:
        modes = self._read_parameter_modes(memory, context)
        result = self._execute_with_modes(memory, context, modes)
        context.pointer = result.next_pointer
        if result.status != ProgramStatus.RUNNING:
            context.status = result.status


class InstructionFactory:
    _instructions: dict[int, Type[InstructionBase]] = {}

    @classmethod
    def register(
        cls, opcode: int
    ) -> Callable[[Type[InstructionBase]], Type[InstructionBase]]:
        def decorator(
            instruction_class: Type[InstructionBase],
        ) -> Type[InstructionBase]:
            cls._instructions[opcode] = instruction_class
            return instruction_class

        return decorator

    def create_instruction(self, opcode: int) -> InstructionBase:
        if opcode not in self._instructions:
            raise ValueError(f'Unknown opcode: {opcode}')
        return self._instructions[opcode]()


@InstructionFactory.register(opcode=1)
class AddInstruction(InstructionBase):
    parameter_count = 3

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value1 = memory.read(context.pointer + 1, modes[0])
        value2 = memory.read(context.pointer + 2, modes[1])
        memory.write(context.pointer + 3, value1 + value2, modes[2])
        return InstructionResult(
            next_pointer=context.pointer + self.parameter_count + 1
        )


@InstructionFactory.register(opcode=2)
class MulInstruction(InstructionBase):
    parameter_count = 3

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value1 = memory.read(context.pointer + 1, modes[0])
        value2 = memory.read(context.pointer + 2, modes[1])
        memory.write(context.pointer + 3, value1 * value2, modes[2])
        return InstructionResult(
            next_pointer=context.pointer + self.parameter_count + 1
        )


@InstructionFactory.register(opcode=99)
class HaltInstruction(InstructionBase):
    parameter_count = 0

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        return InstructionResult(
            next_pointer=context.pointer, status=ProgramStatus.DONE
        )


@InstructionFactory.register(opcode=3)
class InputInstruction(InstructionBase):
    parameter_count = 1

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value = context.read_input()
        status = context.status
        if value is not None:
            memory.write(context.pointer + 1, value, modes[0])
            next_pointer = context.pointer + self.parameter_count + 1
        else:
            next_pointer = context.pointer
        return InstructionResult(next_pointer=next_pointer, status=status)


@InstructionFactory.register(opcode=4)
class OutputInstruction(InstructionBase):
    parameter_count = 1

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value = memory.read(context.pointer + 1, modes[0])
        context.write_output(value)
        return InstructionResult(
            next_pointer=context.pointer + self.parameter_count + 1
        )


@InstructionFactory.register(opcode=5)
class JumpIfTrueInstruction(InstructionBase):
    parameter_count = 2

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value = memory.read(context.pointer + 1, modes[0])
        if value != 0:
            next_pointer = memory.read(context.pointer + 2, modes[1])
        else:
            next_pointer = context.pointer + self.parameter_count + 1
        return InstructionResult(next_pointer=next_pointer)


@InstructionFactory.register(opcode=6)
class JumpIfFalseInstruction(InstructionBase):
    parameter_count = 2

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value = memory.read(context.pointer + 1, modes[0])
        if value == 0:
            next_pointer = memory.read(context.pointer + 2, modes[1])
        else:
            next_pointer = context.pointer + self.parameter_count + 1
        return InstructionResult(next_pointer=next_pointer)


@InstructionFactory.register(opcode=7)
class LessInstruction(InstructionBase):
    parameter_count = 3

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value1 = memory.read(context.pointer + 1, modes[0])
        value2 = memory.read(context.pointer + 2, modes[1])
        result = 1 if value1 < value2 else 0
        memory.write(context.pointer + 3, result, modes[2])
        return InstructionResult(
            next_pointer=context.pointer + self.parameter_count + 1
        )


@InstructionFactory.register(opcode=8)
class EqualInstruction(InstructionBase):
    parameter_count = 3

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value1 = memory.read(context.pointer + 1, modes[0])
        value2 = memory.read(context.pointer + 2, modes[1])
        result = 1 if value1 == value2 else 0
        memory.write(context.pointer + 3, result, modes[2])
        return InstructionResult(
            next_pointer=context.pointer + self.parameter_count + 1
        )


@InstructionFactory.register(opcode=9)
class ChangeRelativeBaselInstruction(InstructionBase):
    parameter_count = 1

    def _execute_with_modes(
        self,
        memory: Memory,
        context: ExecutionContext,
        modes: list[ParameterMode],
    ) -> InstructionResult:
        value = memory.read(context.pointer + 1, modes[0])
        memory.relative_base += value
        return InstructionResult(
            next_pointer=context.pointer + self.parameter_count + 1
        )


class IntcodeComp:
    def __init__(
        self,
        code: list[int] | str,
    ) -> None:
        self.memory = Memory()
        self.context = ExecutionContext(
            pointer=0,
            status=ProgramStatus.RESET,
        )
        self.instruction_factory = InstructionFactory()

        if isinstance(code, str):
            code = list(map(int, code.split(',')))
        self.memory.load_code(code)

    def _execute_next(self) -> None:
        opcode = (
            self.memory.read(
                self.context.pointer, mode=ParameterMode.IMMEDIATE
            )
            % 100
        )
        instruction = self.instruction_factory.create_instruction(opcode)
        if self.context.debug_mode:
            print(
                f'Executing {instruction.__class__.__name__} '
                f'at pointer {self.context.pointer} \n'
                f'Before {self.context=}'
            )
        instruction.execute(memory=self.memory, context=self.context)
        if self.context.debug_mode:
            print(f'After {self.context=}')

    def run_whole_code(
        self,
        input_data: list[int] | None = None,
        debug_mode: bool = False,
    ) -> ProgramStatus:
        self.context.debug_mode = debug_mode
        if input_data:
            self.context.load_input(*input_data)
        while True:
            self._execute_next()
            if self.context.status in (
                ProgramStatus.DONE,
                ProgramStatus.WAITING_INPUT,
            ):
                return self.context.status

    def get_memory(self) -> list[int]:
        return [
            val
            for _, val in sorted(
                [(k, v) for k, v in self.memory.read_all().items()]
            )
        ]

    def get_output(self) -> list[int]:
        return self.context.get_output()

    def pop_output(self) -> int:
        return self.context.pop_output()

    def get_status(self) -> ProgramStatus:
        return self.context.status
