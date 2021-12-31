from typing import Dict, List
from parser.errors.errors import FNotDefinedError, FSyntaxError, FTypeError
from parser.parser.expression_models.atoms import VarExp

from parser.parser.expressions import Expression


# -------------------- Simple Expressions --------------------


class PrintExp(Expression):
    """Print an expression without a newline"""

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return sum(
            [[*exp.eval(variables)] + [["PRINT"], ["POP"]] for exp in self.values],
            []
        )

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "print"


class PutExp(Expression):
    """Print an expression, with a newline"""

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return sum(
            [
                [*exp.eval(variables)]
                + [['PUT' if pos == len(self.values) - 1 else 'PRINT'], ['POP']]
                for pos, exp in enumerate(self.values)
            ],
            []
        )

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "put"


class GetExp(Expression):
    """Get input from user into a specified variable"""
    def __init__(self, line: int, *args):
        self.line = line
        self.variable = args[0]

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        if not isinstance(self.variable, VarExp):
            FSyntaxError(
                self.line,
                "Argument to `get` must be a variable of type String!"
            ).raise_error()

        if self.variable.value not in variables:
            FNotDefinedError(
                self.line,
                f"Variable `{self.variable.value}` is not defined!"
            ).raise_error()

        variables = self.variable.load_type(variables)
       
        if self.variable.value_type != "String":
            FTypeError(
                self.line,
                f"`get` returns a String, but `{self.variable.value}` is of type {self.variable.value_type}!"
            ).raise_error()



        self._value_type = "None"
        return variables

    def eval(self, variables: Dict[str, int]) -> str:
        return f"GET\nSTORE {variables[self.variable.value]}\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "get"

    @classmethod
    def num_args(cls) -> int:
        return 1
