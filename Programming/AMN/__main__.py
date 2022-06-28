#!/usr/bin/python3

"""Execute the module"""

import sys
from typing import Type, TypeVar
from argparse import ArgumentParser, FileType, Namespace
from itertools import repeat
from . import __doc__, __version__, AbstractInstruction, AbstractMachine
from .am0 import Instruction as AM0Instruction, Machine as AM0Machine
from .am1 import Instruction as AM1Instruction, Machine as AM1Machine
from .repl import REPL


T = TypeVar("T")

MACHINES: dict[str, tuple[Type[AbstractInstruction], Type[AbstractMachine]]] = {
    "AM0": (AM0Instruction, AM0Machine),
    "AM1": (AM1Instruction, AM1Machine)
}


def main_repl(instruction: Type[AbstractInstruction[T]], machine: Type[AbstractMachine[T]], args: Namespace) -> int:
    """entry point for the repl subcommand"""
    repl = REPL(instruction, machine.default(map(int, map(input, repeat("Input: ")))))
    repl.cmdloop(f"Welcome the the {args.instructions.upper()} REPL, type 'help' for help")
    return 0


def main_exec(instruction: Type[AbstractInstruction[T]], machine: Type[AbstractMachine[T]], args: Namespace) -> int:
    """entry point for the exec subcommand"""
    program = tuple(instruction.parse_program(args.file.read()))
    for value in machine.default(map(int, map(input, repeat("Input: ")))).execute_program(program):
        if value is not None:
            print(f"Output: {value}")
    return 0


def main_trace(instruction: Type[AbstractInstruction[T]], machine: Type[AbstractMachine[T]], args: Namespace) -> int:
    """entry point for the trace subcommand"""
    program = tuple(instruction.parse_program(args.file.read()))
    output: list[int] = []
    _machine = machine.default(args.input.pop() for _ in reversed(args.input))
    sys.stderr.write(f"{_machine.state(args.input, output)}\n")
    for value in _machine.execute_program(program):
        if value is not None:
            output.append(value)
        sys.stderr.write(f"{_machine.state(args.input, output)}\n")
    return 0


ARGUMENT_PARSER = ArgumentParser(description=__doc__)
ARGUMENT_PARSER.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}"
)
ARGUMENT_PARSER.add_argument(
    "-i",
    "--instructions",
    type=str,
    default="AM0",
    help=f"Instruction set to use, possible selections: {', '.join(MACHINES.keys())}"
)

SUBCOMMANDS = ARGUMENT_PARSER.add_subparsers(required=True)

REPL_PARSER = SUBCOMMANDS.add_parser("repl", help="start the REPL (read evaluate print loop)")
REPL_PARSER.set_defaults(main=main_repl)

EXEC_PARSER = SUBCOMMANDS.add_parser("exec", help="execute a program")
EXEC_PARSER.add_argument(
    "file",
    nargs="?",
    type=FileType("r"),
    default=sys.stdin,
    help="file to read instructions from (omit for stdin)"
)
EXEC_PARSER.set_defaults(main=main_exec)

TRACE_PARSER = SUBCOMMANDS.add_parser("trace", help="trace the execution of a program")
TRACE_PARSER.add_argument(
    "--input",
    nargs="*",
    type=int,
    default=[],
    help="input values for the program"
)
TRACE_PARSER.add_argument(
    "file",
    nargs="?",
    type=FileType("r"),
    default=sys.stdin,
    help="file to read instructions from (omit for stdin)"
)
TRACE_PARSER.set_defaults(main=main_trace)

if __name__ == "__main__":
    args = ARGUMENT_PARSER.parse_args()
    Instruction, Machine = MACHINES[args.instructions.upper()]
    sys.exit(args.main(Instruction, Machine, args))
