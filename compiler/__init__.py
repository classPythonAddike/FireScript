"""
FireScript Compiler

Written in Python, Compiled with Nuitka

- Converts FireScript code into cross platform pseudo bytecode, which will be interpreted later on

Syntax of FireScript:
(begin ...args) ; Very similar to scheme, and is a Lisp Language
Any block of code -> (keyword ...args) is a valid expression
FireScript code is converted into bytecode in the following format -

NUM_CODES_IN_INSTRUCTION INSTRUCTION [ID, (TYPE, ARGS)]

For example, `(+ 5 4)` would be converted to -

```
4 PUSH INT 1 5         -> The `1` denotes that the integer is positive (> 0)
4 PUSH INT 1 4
1 ADD
1 POP
1 POP
```

and `(print 8.0 "Hello!")` to -

```
5 PUSH FLOAT 1 8 0     -> 8 is the integral part, and 0 is the decimal part
1 PRINT
1 POP
8 PUSH STRING 72 101 108 108 111 33
1 PRINT
1 POP
```

And then, instructions like `PUSH`, `PRINT` and constants like `FLOAT` are translated, with predefined codes
So the resulting bytecode for `(+ 5 4)` might look like
```
4 1 6 1 5
4 1 6 1 4
1 10
1 2
1 2
```
"""
