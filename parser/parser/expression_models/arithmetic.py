from parser.errors.errors import FArgsError, FTypeError
from parser.parser.expressions import Expression

from typing import Dict


# -------------------- Arithmetic Expressions --------------------


class AddExp(Expression):
    def __init__(self, line: int, *args: Expression):

        if len(args) == 0:
            FArgsError(
                line,
                f"Got 0 arguments to `({self.__class__.keyword()})`! Was expecting atleast 1!",
            ).raise_error()

        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [val.eval(variables) for val in self.values]
        ) + "ADD\nPOP\nPOP\n" * (len(self.values) - 1)

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        for val in self.values:
            variables = val.load_type(variables)

        val_types = [val.value_type for val in self.values]

        if len(set(val_types)) != 1:
            FTypeError(
                self.line, f"Mismatching types! Got {', '.join(val_types)}!"
            ).raise_error()

        self._value_type = val_types[0]
        return variables

    @classmethod
    def keyword(cls) -> str:
        return "+"


class SubExp(Expression):
    def __init__(self, line: int, *args: Expression):
        self.lval = args[0]
        self.rval = args[1]

        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:

        variables = self.lval.load_type(variables)
        variables = self.rval.load_type(variables)

        if self.lval.value_type != self.rval.value_type:
            FTypeError(
                self.line,
                f"Mismatching types! Got {self.lval.value_type} and {self.rval.value_type}!",
            ).raise_error()

        self._value_type = self.lval.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> str:
        return f"{self.rval.eval(variables)}{self.lval.eval(variables)}SUB\nPOP\nPOP\n"

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "-"


class MulExp(AddExp):
    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [val.eval(variables) for val in self.values]
        ) + "MUL\nPOP\nPOP\n" * (len(self.values) - 1)

    @classmethod
    def keyword(cls) -> str:
        return "*"


class DivExp(SubExp):
    def eval(self, variables: Dict[str, int]) -> str:
        return f"{self.rval.eval(variables)}{self.lval.eval(variables)}DIV\nPOP\nPOP\n"

    @classmethod
    def keyword(cls) -> str:
        return "/"


