from compiler.bytecode.opcodes import OpCodes
from compiler.parser.expressions import Expression
from compiler.errors.errors import FNotDefinedError, FRedefineError, FTypeError

from typing import Dict, List


class DefExp(Expression):
    """
    Syntax: (define variable value)
    Argument Types: Variable, Any
    Return Type: None
    Define a variable with type = type(value), and initialise it with `value`.
    """
    def __init__(self, line: int, *args):

        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._load_type = "None"
        variables = self.value.load_type(variables)

        if self.variable.value in variables:
            # Ensure that the variable has not been defined before.
            FRedefineError(
                self.variable.line,
                f"Variable {self.variable.value} has been redefined!",
            ).raise_error()

        variables[self.variable.value] = self.value.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        variables[self.variable.value] = len(variables)
        return [*self.value.eval(variables)] + [
            [OpCodes.STORE, str(len(variables) - 1)],
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
    """
    Syntax: (assign variable value)
    Argument Types: Variable, Any
    Return Type: None
    Assign a value to a variable.
    """
    def __init__(self, line: int, *args):
        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._load_type = "None"
        variables = self.value.load_type(variables)

        if self.variable.value not in variables:
            # Ensure that the variable has been defined
            FNotDefinedError(
                self.line, f"Variable `{self.variable.value}` has not been defined!"
            ).raise_error()

        if self.value.value_type != (var_type := variables[self.variable.value]):
            # Ensure that type of variable == type of value
            FTypeError(
                self.line,
                f"Variable `{self.variable.value}` has been redefined from {var_type} to {self.value.value_type}!",
            ).raise_error()

        variables[self.variable.value] = self.value.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        # Load Value, Store <variable id>, Pop Value
        return [*self.value.eval(variables)] + [
            [OpCodes.STORE, str(variables[self.variable.value])],
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
