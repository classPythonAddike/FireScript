from parser.lexer.readers import Reader


class Colors:
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CLEAR = "\033[0m"


_r: Reader


def initialise_reader(reader: Reader):
    global _r
    _r = reader


class FException:
    def __init__(self, line_number: int, message: str):
        self.line_number = line_number
        self.message = message

        self.line = _r.from_line_number(self.line_number)

    def raise_error(self):
        line_nos = [self.line_number - 1, self.line_number, self.line_number + 1]
        margin_width = max(map(lambda a: len(str(a)), line_nos))

        print(f"{Colors.RED}{self.prefix}{Colors.YELLOW}")

        if self.line_number != 1:
            print(
                f"   {str(line_nos[0]).rjust(margin_width, ' ')}. | {_r.from_line_number(self.line_number - 1)}"
            )
        print(f"-> {str(line_nos[1]).rjust(margin_width, ' ')}. | {self.line}")
        print(f"   {str(line_nos[2]).rjust(margin_width, ' ')}. | {_r.from_line_number(self.line_number + 1)}")
        print(f"{Colors.RED}{self.type}: {self.message}{Colors.CLEAR}")

        exit(-1)

    @property
    def type(self) -> str:
        return self.__class__.__name__[1:]

    @property
    def prefix(self) -> str:
        return "Error encountered!"


# -------------------- Error Types --------------------


class FSyntaxError(FException):
    @property
    def prefix(self) -> str:
        return "Syntax error encountered!"


class FParsingError(FException):
    @property
    def prefix(self) -> str:
        return "Error while parsing program!"


class FProgramError(FException):
    @property
    def prefix(self) -> str:
        return "Program did not start with a `(begin ...)`!"


class FNotDefinedError(FException):
    @property
    def prefix(self) -> str:
        return "Error encountered - Variable has not been defined!"


class FRedefineError(FException):
    @property
    def prefix(self) -> str:
        return "Error encountered - Variable has been redefined!"


class FTypeError(FException):
    @property
    def prefix(self) -> str:
        return "Error encountered - Object is of wrong type!"


class FArgsError(FException):
    @property
    def prefix(self) -> str:
        return "Error encountered - Incorrect number of arguments provided!"
