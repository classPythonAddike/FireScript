from compiler.bytecode.opcodes import OpCodes
from compiler.errors.errors import FTypeError
from compiler.parser.expressions import Expression

from copy import deepcopy
from typing import List, Dict

class IfExp(Expression):
    """
    Syntax: (if condition body alternate)
    Argument Types: Bool, Any, Any
    Return Type: Any
    If `condition` is true, execute `body`, else, `alternate`
    """
    def __init__(self, line: int, *args: "Expression"):
        self.line = line

        self.condition = args[0]
        self.body = args[1]
        self.alternate = args[2]


    def eval(self, variables: Dict[str, int]) -> List[List[str]]:
        condition_eval = self.condition.eval(variables)
        body_eval = self.body.eval(variables)
        alternate_eval = self.alternate.eval(variables)

        return \
            condition_eval \
            + [[OpCodes.JUMP_IF_TRUE, "1", str(len(alternate_eval) + 2)]] \
            + alternate_eval \
            + [[OpCodes.PUSH, OpCodes.BOOL, "1"], [OpCodes.JUMP_IF_TRUE, "1", str(len(body_eval))]] \
            + body_eval

    def load_type(self, variables: Dict[str, str]) -> Dict[str, str]:
        variables = self.condition.load_type(variables)

        if self.condition.value_type != "Bool":
            FTypeError(
                self.line,
                f"Condition is of wrong type! Expected Bool, but got {self.condition.value_type}!"
            ).raise_error()

        self.body.load_type(deepcopy(variables))
        self.alternate.load_type(deepcopy(variables))

        self._value_type = "None"

        return variables

    @classmethod
    def keyword(cls) -> str:
        return "if"

    @classmethod
    def num_args(cls) -> int:
        return 3
