from parser.bytecode.opcodes import OpCodes
from parser.parser.expressions import Expression
from parser.errors.errors import FNotDefinedError, FRedefineError, FTypeError

from typing import Dict, List


class DefExp(Expression):
    def __init__(self, line: int, *args):

        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._load_type = "None"
        variables = self.value.load_type(variables)

        if self.variable.value in variables:
            FRedefineError(
                self.variable.line,
                f"Variable {self.variable.value} has been redefined!",
            ).raise_error()

        variables[self.variable.value] = self.value.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[int]]:
        variables[self.variable.value] = len(variables)
        return [*self.value.eval(variables)] + [
            [OpCodes.STORE, len(variables) - 1],
            [OpCodes.POP],
        ]

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "define"

    @property
    def value_type(self) -> str:
        return "None"


class AssignExp(Expression):
    def __init__(self, line: int, *args):
        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._load_type = "None"
        variables = self.value.load_type(variables)

        if self.variable.value not in variables:
            FNotDefinedError(
                self.line, f"Variable `{self.variable.value}` has not been defined!"
            ).raise_error()

        if self.value.value_type != (var_type := variables[self.variable.value]):
            FTypeError(
                self.line,
                f"Variable `{self.variable.value}` has been redefined from {var_type} to {self.value.value_type}!",
            ).raise_error()

        variables[self.variable.value] = self.value.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[int]]:
        return [*self.value.eval(variables)] + [
            [OpCodes.STORE, variables[self.variable.value]],
            [OpCodes.POP],
        ]

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "assign"

    @property
    def value_type(self) -> str:
        return "None"
