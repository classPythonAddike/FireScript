import sys
import inspect

from parser.lexer.tokens import Token


class Expression():
    def __init__(self, *args: 'Expression'):
        self.values = args

    def eval(self) -> str:
        """Outputs bytecode"""
        return "".join([exp.eval() for exp in self.values])

    @classmethod
    def keyword(cls) -> str:
        """Keyword that defines the expression type (if, lambda, print, etc)"""
        return ""

    @classmethod
    def atom_type(cls) -> str:
        """Keyword that defines the token type (int, float, bool, etc)"""
        return ""

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<Expression: {self.type}>"


"""
FireScript is Queue based - First In First Out
"""

# -------------------- Expressions --------------------
# Expressions can be broken down into a simpler form

class Program(Expression):
    @classmethod
    def keyword(cls) -> str:
        return "begin"


class PrintExp(Expression):
    def eval(self) -> str:
        return f"{''.join([exp.eval() for exp in reversed(self.values)])}PRINT\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "print"


class AddExp(Expression):
    def __init__(self, *args: Expression):
        self.lval = args[0]
        self.rval = args[1]

    def eval(self) -> str:
        return f"{self.rval.eval()}{self.lval.eval()}ADD\nPOP\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "+"

# -------------------- Atoms --------------------

class IntExp(Expression):
    def __init__(self, *args: Token):
        self.value = int(args[0].value)

    def eval(self) -> str:
        return f"PUSH INT {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Integer'


class FloatExp(Expression):
    def __init__(self, *args: Token):
        self.value = float(args[0].value)

    def eval(self) -> str:
        return f"PUSH FLOAT {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Float'

class BoolExp(Expression):
    def __init__(self, *args: Token):
        self.value = args[0].value

    def eval(self) -> str:
        return f"PUSH BOOL {self.value}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'Bool'

class StrExp(Expression):
    def __init__(self, *args: Token):
        self.value = args[0].value

    def eval(self) -> str:
        """Push an array containing ascii codes of the characters"""
        return f"PUSH STRING {' '.join([str(ord(i)) for i in self.value])}\n"

    @classmethod
    def atom_type(cls) -> str:
        return 'String'


# Get a map of all expressions' keywords to their class
def is_expression_type(c):
    return inspect.isclass(c) and c.__module__ == is_expression_type.__module__ and c.__name__ != "Expression"

expression_types = {
    exp[1].keyword(): exp[1]
    for exp in inspect.getmembers(sys.modules[__name__], is_expression_type)
    if exp[1].keyword()
}

# Get a map of all atoms to their token types
atom_types = {
    exp[1].atom_type(): exp[1]
    for exp in inspect.getmembers(sys.modules[__name__], is_expression_type)
    if exp[1].atom_type()
}
