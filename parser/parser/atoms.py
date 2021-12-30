import sys
import inspect
from typing import Dict

from parser.parser.expressions import Expression
from parser.lexer.tokens import Token

# -------------------- Atoms --------------------

class IntExp(Expression):
    def __init__(self, *args: Token):
        self.value = int(args[0].value)

    def eval(self, _: Dict[str, int]) -> str:
        return f"PUSH INT {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Integer'


class FloatExp(Expression):
    def __init__(self, *args: Token):
        self.value = float(args[0].value)

    def eval(self, _: Dict[str, int]) -> str:
        return f"PUSH FLOAT {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Float'


class BoolExp(Expression):
    def __init__(self, *args: Token):
        self.value = int(args[0].value == "true")

    def eval(self, _: Dict[str, int]) -> str:
        return f"PUSH BOOL {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Bool'


class StrExp(Expression):
    def __init__(self, *args: Token):
        self.value = args[0].value

    def eval(self, _: Dict[str, int]) -> str:
        """Push an array containing ascii codes of the characters"""
        return f"PUSH STRING {' '.join([str(ord(i)) for i in self.value])}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'String'


class VarExp(Expression):
    def __init__(self, *args: Token):
        self.value = args[0].value

    def eval(self, variables: Dict[str, int]) -> str:
        return f"LOAD {variables[self.value]}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Identifier'



def is_expression_type(c):
    return inspect.isclass(c) and c.__module__ == is_expression_type.__module__ and c.__name__ != "Expression"

# Get a map of all atoms to their token types
atom_types = {
    exp[1].atom_type(): exp[1]
    for exp in inspect.getmembers(sys.modules[__name__], is_expression_type)
    if exp[1].atom_type()
}
