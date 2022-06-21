# Programming

## AM0

The AM0 package implements a simple virtual machine for the AM0 instructions set.

To use it, simply execute it with `python3 -m AM0 path/to/file.txt` to execute the instructions written in a file.

If you want an interactive console just type `python3 -m AM0`.

### Requirements

Python >= 3.10 is required to use the utility.

### Examples

The REPL (read eval print loop) in action:

```
python3 -m AM0
Welcome the the AM0 REPL, type 'help' for help
AM0 >> exec READ 0
Input: 8
AM0 >> exec READ 1
Input: 42
AM0 >> exec LOAD 0
AM0 >> exec LOAD 1
AM0 >> exec GT
AM0 >> exec JMC 24
AM0 >> status
Counter: 24
Stack: []
Memory:
    0 := 8
    1 := 42
AM0 >> exit
Exiting REPL...
```

Example program which outputs the biggest of two numbers:

```
READ 0
READ 1
LOAD 0
LOAD 1
GT
JMC 9
LOAD 0
STORE 2
JMP 11
LOAD 1
STORE 2
WRITE 2
```