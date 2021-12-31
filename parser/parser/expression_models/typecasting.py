from parser.errors.errors import FArgsError
from parser.parser.expressions import Expression

from typing import Dict, List

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

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [*self.value.eval(variables)] + [["CAST", "INT"], ["POP"]]

    @classmethod
    def num_args(cls) -> int:
        return 1

    @classmethod
    def keyword(cls) -> str:
        return "int"


class FloatTypeCast(IntTypeCast):
    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [*self.value.eval(variables)] + [["CAST", "FLOAT"], ["POP"]]

    @classmethod
    def keyword(cls) -> str:
        return "float"

    @property
    def value_type(self) -> str:
        return "Float"


class StrTypeCast(IntTypeCast):
    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [*self.value.eval(variables)] + [["CAST", "STRING"], ["POP"]]

    @classmethod
    def keyword(cls) -> str:
        return "string"

    @property
    def value_type(self) -> str:
        return "String"


