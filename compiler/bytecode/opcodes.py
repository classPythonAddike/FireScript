class Auto():
    counter = 0

    @classmethod
    def auto(cls) -> str:
        cls.counter += 1
        return str(cls.counter)


class OpCodes():
    PUSH = Auto.auto()
    POP = Auto.auto()
    STORE = Auto.auto()
    LOAD = Auto.auto()

    CAST = Auto.auto()

    INT = Auto.auto()
    FLOAT = Auto.auto()
    STRING = Auto.auto()
    BOOL = Auto.auto()

    ADD = Auto.auto()
    SUB = Auto.auto()
    MUL = Auto.auto()
    DIV = Auto.auto()

    PRINT = Auto.auto()
    GET = Auto.auto()

    SEP = "\n"
