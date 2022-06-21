#!/usr/bin/python3

"""AM0 REPL"""

from itertools import repeat
from cmd import Cmd
from . import Instruction, Machine

__all__ = (
    "AM0Repl",
)


class AM0Repl(Cmd):
    """interactive REPL"""

    machine: Machine

    def __init__(self, machine: Machine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine = machine
        self.prompt = "AM0 >> "

    def emptyline(self) -> bool:
        """ignore empty lines"""
        return False

    def request_input(self, question: str) -> int:
        """request input from the user"""
        self.stdout.write(question)
        self.stdout.flush()
        return int(self.stdin.readline())

    def do_exec(self, arg: str) -> bool:
        """execute an instruction"""
        try:
            instruction = Instruction.parse(arg)
        except KeyError:
            self.stdout.write("Error: invalid instruction\n")
        except ValueError:
            self.stdout.write("Error: invalid payload\n")
        else:
            try:
                output = self.machine.execute_instruction(instruction, map(self.request_input, repeat("Input: ")))
            except KeyError:
                self.stdout.write("Error: invalid memory address\n")
            except ValueError:
                self.stdout.write("Error: invalid input\n")
            except IndexError:
                self.stdout.write("Error: invalid stack size\n")
            else:
                if output is not None:
                    self.stdout.write(f"Output: {output}\n")
        return False

    def do_reset(self, _) -> bool:
        """reset the machine"""
        self.machine.reset()
        return False

    def do_status(self, _) -> bool:
        """print the current status of the machine"""
        memory = "\n".join(f"\t{key} := {value}" for key, value in self.machine.memory.items())
        self.stdout.write(f"Counter: {self.machine.counter}\n")
        self.stdout.write(f"Stack: {self.machine.stack}\n")
        self.stdout.write(f"Memory:\n{memory}\n")
        return False

    def default(self, line: str) -> None:
        """print an error"""
        self.stdout.write(f"*** Unknown command: {line}\n")

    def do_EOF(self, arg: str) -> bool:
        """exit the repl"""
        return self.do_exit(arg)

    def do_exit(self, _) -> bool:
        """exit the repl"""
        self.stdout.write("Exiting REPL...\n")
        return True
