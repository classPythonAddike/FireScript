from typing import Tuple
from parser.errors.errors import FParsingError, FEOFError

from parser.lexer.tokens import *
from parser.lexer.readers import Reader


class Lexer:
    def __init__(self, reader: Reader):
        self.reader = reader

    def lex_identifier(self) -> str:
        """Grab an identifier"""
        ident = self.reader.current_character()
        while True:
            self.reader.advance_pointer()
            current = self.reader.current_character()
            if not current.isalnum() or current == "EOF":
                self.reader.retreat_pointer()
                return ident
            else:
                ident += current

    def lex_numeric(self) -> Tuple[str, str]:
        """Parse a number, and return the type (float/int), value"""
        is_int = True
        numeric = self.reader.current_character()

        while True:
            self.reader.advance_pointer()
            current = self.reader.current_character()

            if (
                not (current.isdigit() or (current == "." and is_int))
                or current == "EOF"
            ):
                self.reader.retreat_pointer()
                return ["float", "int"][is_int], numeric
            else:
                numeric += current
                if current == ".":
                    is_int = False

    def lex_string(self) -> str:
        quote = self.reader.current_character()
        string = ""
        line = self.reader.current_line_number()
        while True:

            self.reader.advance_pointer()
            current = self.reader.current_character()

            # TODO: Raise error on finding newline/EOF
            if current == quote:
                return string
            elif current == '\n' or current == 'EOF':
                FEOFError(
                    line,
                    'EOF while scanning string!'
                ).raise_error()
            else:
                string += current

    def next_token(self) -> Token:
        """Lex, and return the next token from a reader"""
        while True:
            self.reader.advance_pointer()

            current = self.reader.current_character()

            if current == "EOF":
                return EOF("", self.reader.current_line_number())

            if current.isspace() or current == "\n":
                continue

            elif current in "+-*/":
                return Operator(current, self.reader.current_line_number())
            elif current == "=":
                return EqualTo(current, self.reader.current_line_number())

            elif current in "()":
                return Bracket(current, self.reader.current_line_number())
            elif current in "[]":
                return SquareBracket(current, self.reader.current_line_number())
            elif current in "<>":
                return AngleBracket(current, self.reader.current_line_number())

            elif current.isalpha():
                ident = self.lex_identifier()
                if ident in ["true", "false"]:
                    return Bool(ident, self.reader.current_line_number())
                return Identifier(ident, self.reader.current_line_number())

            elif current.isdigit():
                numeric_type, value = self.lex_numeric()
                return [Float, Integer][numeric_type == "int"](
                    value, self.reader.current_line_number()
                )

            elif current in "\"'":
                return String(self.lex_string(), self.reader.current_line_number())

            else:
                line = self.reader.current_line_number()
                FParsingError(
                    line,
                    f"Unexpected '{current}' on line {line}!",
                ).raise_error()
