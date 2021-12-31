from typing import Dict

from parser.parser.expressions import Expression
from parser.errors.errors import FRedefineError



# -------------------- Simple Expressions --------------------


class PrintExp(Expression):
    """Print an expression without a newline"""

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join([exp.eval(variables) + "PRINT\nPOP\n" for exp in self.values])

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "print"


class PutExp(Expression):
    """Print an expression, with a newline"""

    def eval(self, variables: Dict[str, int]) -> str:
        return "".join(
            [
                exp.eval(variables)
                + f"{'PUT' if pos == len(self.values) - 1 else 'PRINT'}\n"
                for pos, exp in enumerate(self.values)
            ]
        )

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "put"


class DefExp(Expression):
    def __init__(self, line: int, *args):

        self.variable = args[0]
        self.value: Expression = args[1]
        self.line = line

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        self._load_type = "None"
        variables[self.variable.value] = self.value.value_type
        return variables

    def eval(self, variables: Dict[str, int]) -> str:

        if self.variable.value in variables:
            FRedefineError(
                self.variable.line,
                f"Variable {self.variable.value} has been redefined!",
            ).raise_error()

        variables[self.variable.value] = len(variables)
        return f"{self.value.eval(variables)}STORE {len(variables) - 1}\nPOP\n"

    @classmethod
    def num_args(cls) -> int:
        return 2

    @classmethod
    def keyword(cls) -> str:
        return "define"

    @property
    def value_type(self) -> str:
        return "None"

