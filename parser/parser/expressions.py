import sys
import inspect
from typing import Dict

from parser.errors.errors import FArgsError, FRedefineError, FTypeError


class Expression:
    def __init__(self, line: int, *args: "Expression"):
        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        """Outputs bytecode"""
        return "".join([exp.eval(variables) for exp in self.values])

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        """
        Calculates the type of the expression's return value, and forces all child expressions to do the same
        `variables` is used to keep track of the type of variables
        In case a type does not match the required value (like (+ "A" 5)), a TypeError is raised
        Enforces static typing
        """
        for val in self.values:
            variables = val.load_type(variables)

        self._value_type = [val.value_type for val in self.values][0]
        return variables

    @property
    def value_type(self) -> str:
        """Returns the type of the expression's return value"""
        return self._value_type

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
        0 means any number of  arguments can be passed
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

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "begin"


# -------------------- Simple Expressions --------------------


class PrintExp(Expression):
    """Print an expression without a newline"""

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join([exp.eval(variables) + "PRINT\nPOP\n" for exp in self.values])

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "print"


class PutExp(Expression):
    """Print an expression, with a newline"""

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [
                exp.eval(variables)
                + f"{'PUT' if pos == len(self.values) - 1 else 'PRINT'}\n"
                for pos, exp in enumerate(self.values)
            ]
        )

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "put"


class DefExp(Expression):
    def __init__(self, line: int, *args):

        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._load_type = "None"
        variables[self.variable.value] = self.value.value_type
        return variables

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

    @property
    def value_type(self) -> str:
        return "None"


# -------------------- Arithmetic Expressions --------------------


class AddExp(Expression):
    def __init__(self, line: int, *args: Expression):

        if len(args) == 0:
            FArgsError(
                line,
                f"Got 0 arguments to `({self.__class__.keyword()})`! Was expecting atleast 1!",
            ).raise_error()

        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [val.eval(variables) for val in self.values]
        ) + "ADD\nPOP\nPOP\n" * (len(self.values) - 1)

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        for val in self.values:
            variables = val.load_type(variables)

        val_types = [val.value_type for val in self.values]

        if len(set(val_types)) != 1:
            FTypeError(
                self.line, f"Mismatching types! Got {', '.join(val_types)}!"
            ).raise_error()

        self._value_type = val_types[0]
        return variables

    @classmethod
    def keyword(cls) -> str:
        return "+"


class SubExp(Expression):
    def __init__(self, line: int, *args: Expression):
        self.lval = args[0]
        self.rval = args[1]

        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:

        variables = self.lval.load_type(variables)
        variables = self.rval.load_type(variables)

        if self.lval.value_type != self.rval.value_type:
            FTypeError(
                self.line,
                f"Mismatching types! Got {self.lval.value_type} and {self.rval.value_type}!",
            ).raise_error()

        self._value_type = self.lval.value_type
        return variables

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
            [val.eval(variables) for val in self.values]
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
    def __init__(self, line: int, *args: "Expression"):

        if len(args) != 1:
            FArgsError(line, f"Expected 1 arguments, got {len(args)}!").raise_error()

        self.value = args[0]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return self.value.load_type(variables)

    @property
    def value_type(self) -> str:
        return "Integer"

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

    @property
    def value_type(self) -> str:
        return "Float"


class StrTypeCast(IntTypeCast):
    def eval(self, variables: Dict[str, int]) -> str:
        return self.value.eval(variables) + "CAST STRING\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "string"

    @property
    def value_type(self) -> str:
        return "String"


# Get a map of all expressions' keywords to their class
def is_expression_type(c):
    return (
        inspect.isclass(c)
        and c.__module__ == is_expression_type.__module__
        and c.__name__ != "Expression"
    )

expression_types = {
    exp[1].keyword(): exp[1]
    for exp in inspect.getmembers(sys.modules[__name__], is_expression_type)
    if exp[1].keyword()
}
