from typing import Dict, Tuple


class Auto():
    counter = -1

    @classmethod
    def auto(cls) -> str:
        cls.counter += 1
        return str(cls.counter)


class OpCodes():
    PUSH = Auto.auto(), "Push a constant onto the stack. Args: Type, Value"
    POP = Auto.auto(), "Pop a value from the stack. If the stack has more than 1 elements, pop the second item. Else, pop the first."
    STORE = Auto.auto(), "Store the value from the top of the stack into a variable. Args: Variable ID"
    LOAD = Auto.auto(), "Load the value of a variable onto the top of the stack. Args: Variable ID"
    JUMP_IF_TRUE_AND_POP = Auto.auto(), "Skip the next `n` lines if the top of the stack is true. Pop the value, regardless of it's value. Args: n"

    CAST = Auto.auto(), "Type cast the top of the stack, and push it onto the stack. Args: Type"

    INT = Auto.auto(), "Indicates that the next argument will be an integer"
    FLOAT = Auto.auto(), "Indicates that the next argument will be an float"
    STRING = Auto.auto(), "Indicates that the next argument will be an string"
    BOOL = Auto.auto(), "Indicates that the next argument will be an boolean"

    ADD = Auto.auto(), "Add the last two values from the stack, and push the result onto the stack"
    SUB = Auto.auto(), "Subtract the last two value from the stack from the previous value, and push the result onto the stack"
    MUL = Auto.auto(), "Multiply the last two values from the stack, and push the result onto the stack"
    DIV = Auto.auto(), "Divide the last value from the stack by the previous value, and push the result onto the stack"

    PRINT = Auto.auto(), "Print the last value from the stack, without a trailing newline"
    GET = Auto.auto(), "Get user input, and store it onto the stack"

    SEP = "\n"


operations: Dict[str, Tuple[str, str]] = {}
for inst in OpCodes.__dict__:
    if type(attr := getattr(OpCodes, inst)) == tuple:
        code, docs = attr
        setattr(OpCodes, inst, code)
        operations[inst] = code, docs
