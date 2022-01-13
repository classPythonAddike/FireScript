from compiler.bytecode.opcodes import OpCodes
from compiler.errors.errors import FTypeError
from compiler.parser.expressions import Expression

from typing import List, Dict


class EqualToExp(Expression):
    """
    Syntax: (= arg1 arg2)
    Argument Types: Any
    Return Type: Bool
    Check if two objects are equal
    """
    def __init__(self, line: int, *args: "Expression"):
        self.line = line
        self.lval = args[0]
        self.rval = args[1]

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return self.rval.eval(variables) + self.lval.eval(variables) + [[OpCodes.COMPARE, "0"]]

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        variables = self.lval.load_type(variables)
        variables = self.rval.load_type(variables)

        if self.lval.value_type != self.rval.value_type:
            FTypeError(
                self.line,
                f"Cannot compare objects of type {self.lval.value_type} and {self.rval.value_type}!"
            ).raise_error()

        self._value_type = "Bool"
        return variables

    @classmethod
    def keyword(cls) -> str:
        return "="

    @classmethod
    def num_args(cls) -> int:
        return 2


class GreaterThanExp(EqualToExp):
    """
    Syntax: (> arg1 arg2)
    Argument Types: Integer | Float
    Return Type: Bool
    Check if arg1 > arg2
    """

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        variables = self.lval.load_type(variables)
        variables = self.rval.load_type(variables)

        if self.lval.value_type != self.rval.value_type:
            FTypeError(
                self.line,
                f"Cannot compare objects of type {self.lval.value_type} and {self.rval.value_type}!"
            ).raise_error()

        if self.lval.value_type not in ["Integer", "Float"]:
            FTypeError(
                self.line,
                f"Cannot compare objects of type {self.lval.value_type}!"
            ).raise_error()

        self._value_type = "Bool"
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return self.rval.eval(variables) + self.lval.eval(variables) + [[OpCodes.COMPARE, "1"]]

    @classmethod
    def keyword(cls) -> str:
        return ">"


class LessThanExp(GreaterThanExp):
    """
    Syntax: (< arg1 arg2)
    Argument Types: Integer | Float
    Return Type: Bool
    Check if arg1 < arg2
    """
    def __init__(self, line: int, *args: "Expression"):
        self.line = line
        self.lval = args[1]
        self.rval = args[0]

    @classmethod
    def keyword(cls) -> str:
        return "<"


class GreaterThanOrEqualExp(GreaterThanExp):
    """
    Syntax: (>= arg1 arg2)
    Argument Types: Integer | Float
    Return Type: Bool
    Check if arg1 >= arg2
    """

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return self.rval.eval(variables) + self.lval.eval(variables) + [[OpCodes.COMPARE, "2"]]

    @classmethod
    def keyword(cls) -> str:
        return ">" # First identifier will be `>`

    @classmethod
    def num_args(cls) -> int:
        return 3 # 1 argument for the `=`


class LessThanOrEqualExp(GreaterThanOrEqualExp):
    def __init__(self, line: int, *args: "Expression"):
        self.line = line
        self.lval = args[1]
        self.rval = args[0]
