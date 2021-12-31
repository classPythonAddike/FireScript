from typing import Dict
from parser.errors.errors import FTypeError

from parser.parser.expressions import Expression
from parser.lexer.tokens import Token

# -------------------- Atoms --------------------


class IntExp(Expression):
    def __init__(self, *args: Token):

        try:
            self.value = int(args[0].value)
        except:
            FTypeError(args[0].line, "Couldn't parse integer!").raise_error()

        self.line = args[0].line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()

    def eval(self, _: Dict[str, int]) -> str:
        return f"PUSH INT {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return "Integer"


class FloatExp(Expression):
    def __init__(self, *args: Token):

        try:
            self.value = float(args[0].value)
        except:
            FTypeError(args[0].line, "Couldn't parse float!").raise_error()

        self.line = args[0].line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    def eval(self, _: Dict[str, int]) -> str:
        return f"PUSH FLOAT {self.value}\n"

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()

    @classmethod
    def atom_type(cls) -> str:
        return "Float"


class BoolExp(Expression):
    def __init__(self, *args: Token):
        self.value = int(args[0].value == "true")
        self.line = args[0].line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    def eval(self, _: Dict[str, int]) -> str:
        return f"PUSH BOOL {self.value}\n"

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()

    @classmethod
    def atom_type(cls) -> str:
        return "Bool"


class StrExp(Expression):
    def __init__(self, *args: Token):
        self.value = args[0].value
        self.line = args[0].line

    def eval(self, _: Dict[str, int]) -> str:
        """Push an array containing ascii codes of the characters"""
        return f"PUSH STRING {' '.join([str(ord(i)) for i in self.value])}\n"

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    @classmethod
    def atom_type(cls) -> str:
        return "String"

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()


class VarExp(Expression):
    def __init__(self, *args: Token):
        self.value = args[0].value
        self.line = args[0].line

    def eval(self, variables: Dict[str, int]) -> str:
        return f"LOAD {variables[self.value]}\n"

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._value_type = variables[self.value]
        return variables

    @classmethod
    def atom_type(cls) -> str:
        return "Identifier"

