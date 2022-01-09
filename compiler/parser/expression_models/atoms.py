from typing import Dict, List
from compiler.errors.errors import FNotDefinedError, FTypeError

from compiler.bytecode.opcodes import OpCodes
from compiler.parser.expressions import Expression
from compiler.lexer.tokens import Token

# -------------------- Atoms --------------------


class IntExp(Expression):
    r"""
    Syntax: [\-][0-9]+
    Return Type: Integer
    Integer data type
    """
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

    def eval(self, _: Dict[str, int]) -> List[List[str]]:
        """PUSH, INT, +ve / -ve, integer"""
        return [[OpCodes.PUSH, OpCodes.INT, f"{int(self.value >= 0)}",str(abs(self.value))]]

    @classmethod
    def atom_type(cls) -> str:
        return "Integer"


class FloatExp(Expression):
    r"""
    Syntax: [\-][0-9]+\.[0-9]+
    Return Type: Float
    Float data type
    """
    def __init__(self, *args: Token):
        try:
            self.value = float(args[0].value)
        except:
            FTypeError(args[0].line, "Couldn't parse float!").raise_error()

        self.line = args[0].line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    def eval(self, _: Dict[str, int]) -> List[List[str]]:
        """PUSH, FLOAT, +ve / -ve, integer part, decimal part"""
        integer, decimal = str(abs(self.value)).split(".")
        return [[OpCodes.PUSH, OpCodes.FLOAT, f"{int(self.value >= 0)}", integer, decimal]]

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()

    @classmethod
    def atom_type(cls) -> str:
        return "Float"


class BoolExp(Expression):
    """
    Syntax: [true, false]
    Return Type: Bool
    Bool data type
    """
    def __init__(self, *args: Token):
        self.value = int(args[0].value == "true")
        self.line = args[0].line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    def eval(self, _: Dict[str, int]) -> List[List[str]]:
        """PUSH, BOOL, 1 / 0"""
        return [[OpCodes.PUSH, OpCodes.BOOL, str(self.value)]]

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()

    @classmethod
    def atom_type(cls) -> str:
        return "Bool"


class StrExp(Expression):
    """
    Syntax: "..." or '...'
    Return Type: String
    String data type
    """
    
    def __init__(self, *args: Token):
        self.value = args[0].value
        self.line = args[0].line

    def eval(self, _: Dict[str, int]) -> List[List[str]]:
        """Push an array containing ascii codes of the characters"""
        return [[OpCodes.PUSH, OpCodes.STRING] + [str(ord(i)) for i in self.value]]

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        return variables

    @classmethod
    def atom_type(cls) -> str:
        return "String"

    @property
    def value_type(self) -> str:
        return self.__class__.atom_type()


class VarExp(Expression):
    """
    Syntax: variable_name
    Return Type: Any
    Atom to represent a variable.
    """
    def __init__(self, *args: Token):
        self.value = args[0].value
        self.line = args[0].line

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        """
        Variables are given ids in the bytecode, when they are defined.
        So we just tell the VM to load the value stored in our unique id

        LOAD, <ID>
        """
        return [[OpCodes.LOAD, str(variables[self.value])]]

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        """Variable's type is the type stated when defining it."""

        if self.value not in variables:
            FNotDefinedError(
                self.line,
                f"Variable `{self.value}` was not defined!"
            ).raise_error()

        self._value_type = variables[self.value]
        return variables

    @classmethod
    def atom_type(cls) -> str:
        return "Identifier"
