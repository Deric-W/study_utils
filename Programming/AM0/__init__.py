#!/usr/bin/python3

"""Simple virtual machine for the AM0 instruction set"""

from __future__ import annotations
from collections.abc import Sequence, Iterator
from itertools import repeat
from enum import Enum, unique


__version__ = "0.3.0"
__author__  = "Eric Niklas Wolf"
__email__   = "eric_niklas.wolf@mailbox.tu-dresden.de"
__all__ = (
    "Instruction",
    "Machine",
    "repl"
)


@unique
class Instruction(Enum):
    """AM0 instruction"""
    ADD   = 1
    MUL   = 2
    SUB   = 3
    DIV   = 4
    MOD   = 5
    EQ    = 6
    NE    = 7
    LT    = 8
    GT    = 9
    LE    = 10
    GE    = 11
    LOAD  = 12
    STORE = 13
    LIT   = 14
    JMP   = 15
    JMC   = 16
    WRITE = 17
    READ  = 18

    @classmethod
    def parse(cls, line: str) -> tuple[Instruction, int]:
        """parse an instance from a line like '<Name> <payload>' or '<Name>'"""
        name, seperator, payload = line.partition(" ")
        if seperator == "":
            return (cls[name], 0)
        else:
            return (cls[name], int(payload))

    @classmethod
    def parse_program(cls, source: str) -> Iterator[tuple[Instruction, int]]:
        """parse a program consisting of multiple lines"""
        for number, line in enumerate(source.split("\n"), start=1):
            try:
                if not line or line.isspace():
                    continue
                yield cls.parse(line)
            except KeyError as error:
                raise ValueError(f"invalid instruction at line {number}") from error
            except ValueError as error:
                raise ValueError(f"invalid payload at line {number}") from error

    def is_jump(self) -> bool:
        """check if the instruction is a jump"""
        return 14 < self.value < 17

    def has_payload(self) -> bool:
        """check if the instruction uses its payload"""
        return self.value > 11


class Machine:
    """machine for executing AM0 instructions"""

    __slots__ = ("counter", "stack", "memory")

    counter: int

    stack: list[int]

    memory: dict[int, int]

    def __init__(self, counter: int, stack: list[int], memory: dict[int, int]) -> None:
        self.counter = counter
        self.stack = stack
        self.memory = memory

    @classmethod
    def default(cls) -> Machine:
        """create an instance with default values"""
        return cls(0, [], {})

    def execute_instruction(self, instruction: tuple[Instruction, int], input: Iterator[int]) -> int | None:
        """execute an instruction, returning the output if produced"""
        value = None
        match instruction:
            case (Instruction.ADD, _):
                self.stack[-2] = self.stack[-2] + self.stack[-1]
                self.stack.pop()
            case (Instruction.MUL, _):
                self.stack[-2] = self.stack[-2] * self.stack[-1]
                self.stack.pop()
            case (Instruction.SUB, _):
                self.stack[-2] = self.stack[-2] - self.stack[-1]
                self.stack.pop()
            case (Instruction.DIV, _):
                self.stack[-2] = self.stack[-2] // self.stack[-1]
                self.stack.pop()
            case (Instruction.MOD, _):
                self.stack[-2] = self.stack[-2] % self.stack[-1]
                self.stack.pop()
            case (Instruction.EQ, _):
                self.stack[-2] = self.stack[-2] == self.stack[-1]
                self.stack.pop()
            case (Instruction.NE, _):
                self.stack[-2] = self.stack[-2] != self.stack[-1]
                self.stack.pop()
            case (Instruction.LT, _):
                self.stack[-2] = self.stack[-2] < self.stack[-1]
                self.stack.pop()
            case (Instruction.GT, _):
                self.stack[-2] = self.stack[-2] > self.stack[-1]
                self.stack.pop()
            case (Instruction.LE, _):
                self.stack[-2] = self.stack[-2] <= self.stack[-1]
                self.stack.pop()
            case (Instruction.GE, _):
                self.stack[-2] = self.stack[-2] >= self.stack[-1]
                self.stack.pop()
            case (Instruction.LOAD, n):
                self.stack.append(self.memory[n])
            case (Instruction.STORE, n):
                self.memory[n] = self.stack.pop()
            case (Instruction.LIT, n):
                self.stack.append(n)
            case (Instruction.JMP, n):
                self.counter = n - 1
            case (Instruction.JMC, n):
                if self.stack.pop() == 0:
                    self.counter = n - 1
            case (Instruction.WRITE, n):
                value = self.memory[n]
            case (Instruction.READ, n):
                self.memory[n] = next(input)
            case i:
                raise ValueError(f"invalid instruction: '{i}'")
        self.counter += 1
        return value

    def execute_program(self, program: Sequence[tuple[Instruction, int]], input: Iterator[int]) -> Iterator[int]:
        """execute a program, yielding occuring output"""
        self.counter = 0
        while self.counter < len(program):
            output = self.execute_instruction(program[self.counter], input)
            if output is not None:
                yield output

    def execute_interactive(self, program: Sequence[tuple[Instruction, int]]) -> None:
        """execute a program with interactive input and output"""
        for output in self.execute_program(program, map(int, map(input, repeat("Input: ")))):
            print(f"Output: {output}")

    def reset(self) -> None:
        """reset the machine to the default state"""
        self.counter = 0
        self.stack.clear()
        self.memory.clear()
