#!/usr/bin/python3

"""Execute the module"""

from argparse import ArgumentParser, FileType
from . import Instruction, Machine, __doc__, __version__
from .repl import AM0Repl

ARGUMENT_PARSER = ArgumentParser(description=__doc__)
ARGUMENT_PARSER.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}"
)
ARGUMENT_PARSER.add_argument(
    "file",
    nargs="?",
    type=FileType("r"),
    default=None,
    help="path to program which shall be executed, omit for interactive REPL"
)

if __name__ == "__main__":
    args = ARGUMENT_PARSER.parse_args()
    machine = Machine.default()
    if args.file is None:
        AM0Repl(machine).cmdloop("Welcome the the AM0 REPL, type 'help' for help")
    else:
        program = tuple(Instruction.parse_program(args.file.read()))
        machine.execute_interactive(program)
