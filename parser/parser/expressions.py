import sys
import inspect
from typing import Dict

from parser.errors.errors import FArgsError, FRedefineError


class Expression():
    def __init__(self, line: int, *args: 'Expression'):
        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        """Outputs bytecode"""
        return "".join([exp.eval(variables) for exp in self.values])

    @classmethod
    def keyword(cls) -> str:
        """Keyword that defines the expression type (if, lambda, print, etc)"""
        return ""

    @classmethod
    def atom_type(cls) -> str:
        """Keyword that defines the token type (int, float, bool, etc)"""
        return ""

    @classmethod
    def num_args(cls) -> int:
        """
            Number of arguments expected to construct this expression
            0 means infinite
        """
        return 0

    @property
    def type(self) -> str:
        return self.__class__.__name__
    
    def __repr__(self) -> str:
        return f"<Expression: {self.type}>"


"""
FireScript's runtime uses something similar to a stack.
When an object is pushed/loaded, it is placed onto the stack.
But when an object is popped, it is popped from the second position from the top.
"""

# -------------------- Expressions --------------------
# Expressions can be broken down into a simpler form

class Program(Expression):
    """(begin ...)"""
    @classmethod
    def keyword(cls) -> str:
        return "begin"


# -------------------- Simple Expressions --------------------

class PrintExp(Expression):
    """Print an expression without a newline"""
    def eval(self, variables: Dict[str, int]) -> str:
        return ''.join(
                [
                    exp.eval(variables) + 'PRINT\nPOP\n'
                    for exp in self.values
                ]
            )

    @classmethod
    def keyword(cls) -> str:
        return "print"

class PutExp(Expression):
    """Print an expression, with a newline"""
    def eval(self, variables: Dict[str, int]) -> str:
        return ''.join(
            [
                exp.eval(variables) + f"{'PUT' if pos == len(self.values) - 1 else 'PRINT'}\n"
                for pos, exp in enumerate(self.values)
            ]
        )

    @classmethod
    def keyword(cls) -> str:
        return "put"


class DefExp(Expression):
    def __init__(self, line: int, *args):

        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:

        if self.variable.value in variables:
            FRedefineError(
                self.variable.line,
                f"Variable {self.variable.value} has been redefined!",
            ).raise_error()
        
        variables[self.variable.value] = len(variables)
        return f"{self.value.eval(variables)}STORE {len(variables) - 1}\nPOP\n"

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "define"


# -------------------- Arithmetic Expressions --------------------


class AddExp(Expression):
    def __init__(self, line: int, *args: Expression):
        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [
                val.eval(variables)
                for val in self.values
            ]
        ) + "ADD\nPOP\nPOP\n" * (len(self.values) - 1)

    @classmethod
    def keyword(cls) -> str:
        return "+"


class SubExp(Expression):
    def __init__(self, line: int, *args: Expression):
        self.lval = args[0]
        self.rval = args[1]

        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        return f"{self.rval.eval(variables)}{self.lval.eval(variables)}SUB\nPOP\nPOP\n"

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "-"


class MulExp(AddExp):
    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [
                val.eval(variables)
                for val in self.values
            ]
        ) + "MUL\nPOP\nPOP\n" * (len(self.values) - 1)

    @classmethod
    def keyword(cls) -> str:
        return "*"

class DivExp(SubExp):
    def eval(self, variables: Dict[str, int]) -> str:
        return f"{self.rval.eval(variables)}{self.lval.eval(variables)}DIV\nPOP\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "/"


# -------------------- TypeCasting --------------------


class IntTypeCast(Expression):
    def __init__(self, line: int, *args: 'Expression'):
        
        if len(args) != 1:
            FArgsError(
                line,
                f"Expected 1 arguments, got {len(args)}!"
            ).raise_error()

        self.value = args[0]
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        return self.value.eval(variables) + "CAST INT\nPOP\n"

    @classmethod
    def num_args(cls) -> int:
        return 1

    @classmethod
    def keyword(cls) -> str:
        return "int"


class FloatTypeCast(IntTypeCast):
    def eval(self, variables: Dict[str, int]) -> str:
        return self.value.eval(variables) + "CAST FLOAT\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "float"

class StrTypeCast(IntTypeCast):
    def eval(self, variables: Dict[str, int]) -> str:
        return self.value.eval(variables) + "CAST STRING\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "string"


# Get a map of all expressions' keywords to their class
def is_expression_type(c):
    return inspect.isclass(c) and c.__module__ == is_expression_type.__module__ and c.__name__ != "Expression"

expression_types = {
    exp[1].keyword(): exp[1]
    for exp in inspect.getmembers(sys.modules[__name__], is_expression_type)
    if exp[1].keyword()
}

