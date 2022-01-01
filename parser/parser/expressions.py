from typing import Dict, List


# -------------------- Expressions --------------------
# Expressions can be broken down into a simpler form


class Expression:
    def __init__(self, line: int, *args: "Expression"):
        self.values = args
        self.line = line

    def eval(self, variables: Dict[str, int]) -> List[List[int]]:
        """Outputs bytecode"""
        return sum([exp.eval(variables) for exp in self.values], [])

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        """
        Calculates the type of the expression's return value, and forces all child expressions to do the same
        `variables` is used to keep track of the type of variables
        In case a type does not match the required value (like (+ "A" 5)), a TypeError is raised
        Enforces static typing
        """
        for val in self.values:
            variables = val.load_type(variables)

        self._value_type = [val.value_type for val in self.values][0]
        return variables

    @property
    def value_type(self) -> str:
        """Returns the type of the expression's return value"""
        return self._value_type

    @classmethod
    def keyword(cls) -> str:
        """Keyword that defines the expression type (if, lambda, print, etc)"""
        return ""

    @classmethod
    def atom_type(cls) -> str:
        """Keyword that defines the token type (int, float, bool, etc)"""
        return ""

    @classmethod
    def num_args(cls) -> int:
        """
        Number of arguments expected to construct this expression
        0 means any number of  arguments can be passed
        """
        return 0

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<Expression: {self.type}>"


class Program(Expression):
    """(begin ...)"""

    @property
    def value_type(self) -> str:
        return "None"

    @classmethod
    def keyword(cls) -> str:
        return "begin"
