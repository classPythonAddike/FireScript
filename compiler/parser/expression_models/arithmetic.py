from compiler.parser.expressions import Expression
from compiler.bytecode.opcodes import OpCodes
from compiler.errors.errors import FArgsError, FTypeError

from typing import Dict, List


# -------------------- Arithmetic Expressions --------------------


class AddExp(Expression):
    """
    Syntax: (+ val1 val2 val3 ...)
    Argument Types: Any
    Return Type: Any
    Add `n` values to each other
    """

    def __init__(self, line: int, *args: Expression):

        if len(args) == 0:
            FArgsError(
                line,
                f"Got 0 arguments to `({self.__class__.keyword()})`! Was expecting atleast 1!",
            ).raise_error()

        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return sum([val.eval(variables) for val in self.values], []) + [
            [OpCodes.ADD],
        ] * (len(self.values) - 1)

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        """
        First, make sure every object is of the same type.
        Then set the addition expression's type to that of the objects.
        """
        for val in self.values:
            variables = val.load_type(variables)

        val_types = [val.value_type for val in self.values]

        # Types are not the same
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
    """
    Syntax: (- val1 val2)
    Argument Types: Any
    Return Type: Any
    Subtract two values from each other
    """

    def __init__(self, line: int, *args: Expression):
        self.lval = args[0]
        self.rval = args[1]

        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        """Make sure both values are of same type, then set expression's type"""

        variables = self.lval.load_type(variables)
        variables = self.rval.load_type(variables)

        if self.lval.value_type != self.rval.value_type:
            FTypeError(
                self.line,
                f"Mismatching types! Got {self.lval.value_type} and {self.rval.value_type}!",
            ).raise_error()

        if self.lval.value_type not in ["Integer", "Float"]:
            FTypeError(
                self.line,
                f"Cannot multiply {self.lval.value_type}!"
            ).raise_error()

        self._value_type = self.lval.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return (
            [*self.rval.eval(variables)]
            + [*self.lval.eval(variables)]
            + [[OpCodes.SUB]]
        )

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "-"


class MulExp(AddExp):
    """
    Syntax: (* val1 val2 val3 ...)
    Argument Types: Any
    Return Type: Any
    Multiply `n` values with each other
    """

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        """
        First, make sure every object is of the same type.
        Then set the multiplication expression's type to that of the objects.
        """
        for val in self.values:
            variables = val.load_type(variables)

        val_types = [val.value_type for val in self.values]

        # Types are not the same
        if len(set(val_types)) != 1:
            FTypeError(
                self.line, f"Mismatching types! Got {', '.join(val_types)}!"
            ).raise_error()

        if val_types[0] not in ["Integer", "Float"]:
            FTypeError(
                self.line,
                f"Cannot multiply a {val_types[0]} with a {val_types[0]}!"
            ).raise_error()

        self._value_type = val_types[0]
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return sum([val.eval(variables) for val in self.values], []) + [
            [OpCodes.MUL],
        ] * (len(self.values) - 1)

    @classmethod
    def keyword(cls) -> str:
        return "*"


class DivExp(SubExp):
    """
    Syntax: (/ val1 val2)
    Argument Types: Any
    Return Type: Any
    Divide 1 value by another
    """
    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return (
            [*self.rval.eval(variables)]
            + [*self.lval.eval(variables)]
            + [[OpCodes.DIV]]
        )

    @classmethod
    def keyword(cls) -> str:
        return "/"
