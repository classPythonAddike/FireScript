from compiler.bytecode.opcodes import OpCodes
from compiler.parser.expressions import Expression

from typing import Dict, List

# -------------------- TypeCasting --------------------


class IntTypeCast(Expression):
    """
    Syntax: (int value)
    Argument Types: Any
    Return Type: Int
    Type casts a provided value into an integer.
    """
    def __init__(self, line: int, *args: "Expression"):
        self.value = args[0]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return self.value.load_type(variables)

    @property
    def value_type(self) -> str:
        return "Integer"

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [*self.value.eval(variables)] + [
            [OpCodes.CAST, OpCodes.INT],
            [OpCodes.POP],
        ]

    @classmethod
    def num_args(cls) -> int:
        return 1

    @classmethod
    def keyword(cls) -> str:
        return "int"


class FloatTypeCast(IntTypeCast):
    """
    Syntax: (float value)
    Argument Types: Any
    Return Type: Float
    Type casts a provided value into an float.
    """
    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [*self.value.eval(variables)] + [
            [OpCodes.CAST, OpCodes.FLOAT],
            [OpCodes.POP],
        ]

    @classmethod
    def keyword(cls) -> str:
        return "float"

    @property
    def value_type(self) -> str:
        return "Float"


class StrTypeCast(IntTypeCast):
    """
    Syntax: (string value)
    Argument Types: Any
    Return Type: String
    Type casts a provided value into an string.
    """
    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [*self.value.eval(variables)] + [
            [OpCodes.CAST, OpCodes.STRING],
            [OpCodes.POP],
        ]

    @classmethod
    def keyword(cls) -> str:
        return "string"

    @property
    def value_type(self) -> str:
        return "String"
