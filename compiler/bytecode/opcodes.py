from typing import Dict, Tuple


class Auto():
    counter = -1

    @classmethod
    def auto(cls) -> str:
        cls.counter += 1
        return str(cls.counter)


class OpCodes():
    PUSH = Auto.auto()
    STORE = Auto.auto()
    LOAD = Auto.auto()
    JUMP_IF_TRUE = Auto.auto()
    PUSH_DOCS = "Push a constant onto the stack. Args: Type, Value"
    STORE_DOCS = "Store the value from the top of the stack into a variable. Args: Variable ID"
    LOAD_DOCS = "Load the value of a variable onto the top of the stack. Args: Variable ID"
    JUMP_IF_TRUE_DOCS = "Pop the top of the stack. Skip the next `n` lines in a given direction if it is true. Args: n, direction"

    CAST = Auto.auto()
    CAST_DOCS = "Pop the top value from the stack, type cast it, and push it onto the stack. Args: Type"

    INT = Auto.auto()
    FLOAT = Auto.auto()
    STRING = Auto.auto()
    BOOL = Auto.auto()
    INT_DOCS = "Indicates that the next argument will be an integer. Takes one argument - the integer itself"
    FLOAT_DOCS = "Indicates that the next argument will be a float. Takes two arguments - the integer part, and decimal part"
    STRING_DOCS = "Indicates that the next argument will be a string. Takes `n` arguments - `n` integers representing the ascii codes of each char."
    BOOL_DOCS = "Indicates that the next argument will be a boolean. Takes one argument - 1 for true and 0 for false"

    ADD = Auto.auto()
    SUB = Auto.auto()
    MUL = Auto.auto()
    DIV = Auto.auto()
    ADD_DOCS = "Pop the top two values from the stack, and push their sum onto the stack"
    SUB_DOCS = "Pop the top two values from the stack,and push first - second onto the stack"
    MUL_DOCS = "Pop the top two values from the stack, and push their product onto the stack"
    DIV_DOCS = "Pop the top two values from the stack,and push first / second onto the stack"

    PRINT = Auto.auto()
    GET = Auto.auto()
    PRINT_DOCS = "Pop the top value from the stack and print it, without a trailing newline"
    GET_DOCS = "Get user input, and store it onto the stack"

    COMPARE = Auto.auto()
    COMPARE_DOCS = "Pop the top two values from the stack, and compare them. Takes one argument - 0/1/2. 0 for ==, 1 for >, 2 for >=."

    SEP = "\n"


operations: Dict[str, Tuple[str, str]] = {}
for inst in OpCodes.__dict__:
    if not inst.endswith("_DOCS") and not inst.endswith("__") and inst != "SEP":
        operations[inst] = getattr(OpCodes, inst), getattr(OpCodes, inst + "_DOCS")
