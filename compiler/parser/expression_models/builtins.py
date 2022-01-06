from typing import Dict, List

from compiler.bytecode.opcodes import OpCodes
from compiler.parser.expressions import Expression
from compiler.parser.expression_models.atoms import VarExp
from compiler.errors.errors import FNotDefinedError, FSyntaxError, FTypeError


# -------------------- Simple Expressions --------------------


class PrintExp(Expression):
    """
    Syntax: (print arg1 arg2 arg3 ...)
    Argument Types: Any
    Return Type: None
    Print an expression without a newline
    """

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        """Load each argument onto the stack, and print it manually"""
        return sum(
            [
                [*exp.eval(variables)] + [[OpCodes.PRINT], [OpCodes.POP]]
                for exp in self.values
            ],
            [],
        )

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "print"


class PutExp(Expression):
    """
    Syntax: (put arg1 arg2 arg3 ...)
    Argument Types: Any
    Return Type: None
    Print an expression with a newline
    """

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        """Load each arg, and then print it. Then, print a newline"""
        return sum(
            [
                [*exp.eval(variables)]
                + [
                    [OpCodes.PRINT],
                    [OpCodes.POP],
                ]
                for exp in self.values
            ],
            [],
        ) + [[OpCodes.PUSH, OpCodes.STRING, str(ord("\n"))], [OpCodes.PRINT], [OpCodes.POP]]


    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "put"


class GetExp(Expression):
    """
    Syntax: (get variable)
    Argument Types: Variable of type String
    Return Type: None
    Store user input into `variable`
    """ 

    def __init__(self, line: int, *args):
        self.line = line
        self.variable = args[0]

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        # Ensure that the the argument is a variable
        if not isinstance(self.variable, VarExp):
            FSyntaxError(
                self.line, "Argument to `get` must be a variable of type String!"
            ).raise_error()

        if self.variable.value not in variables:
            # Ensure that the variable is defined
            FNotDefinedError(
                self.line, f"Variable `{self.variable.value}` is not defined!"
            ).raise_error()

        variables = self.variable.load_type(variables)

        if self.variable.value_type != "String":
            # Ensure that the variable is of type string
            FTypeError(
                self.line,
                f"`get` returns a String, but `{self.variable.value}` is of type {self.variable.value_type}!",
            ).raise_error()

        self._value_type = "None"
        return variables

    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        return [
            [OpCodes.GET],
            [OpCodes.STORE, str(variables[self.variable.value])],
            [OpCodes.POP],
        ]

    @classmethod
    def keyword(cls) -> str:
        return "get"

    @classmethod
    def num_args(cls) -> int:
        return 1
