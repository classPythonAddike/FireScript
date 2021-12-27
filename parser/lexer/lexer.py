from typing import Tuple

from parser.lexer.tokens import *
from parser.lexer.readers import Reader

class Lexer():
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
            if not (current.isdigit() or (current == "." and is_int)) or current == "EOF":
                self.reader.retreat_pointer()
                return ["float", "int"][is_int], numeric
            else:
                numeric += current
                if current == ".":
                    is_int = False

    def lex_string(self) -> str:
        quote = self.reader.current_character()
        string = ""

        while True:

            self.reader.advance_pointer()
            current = self.reader.current_character()

            # TODO: Raise error on finding newline/EOF
            if current == quote:
                return string
            else:
                string += current

    def next_token(self) -> Token:
        """Lex, and return the next token from a reader"""
        while True:
            self.reader.advance_pointer()

            current = self.reader.current_character()

            if current == "EOF":
                return EOF("")

            if current == "\n":
                return NewLine(current)

            if current.isspace():
                continue

            elif current in "+-*/":
                return Operator(current)
            elif current == "=":
                return EqualTo(current)

            elif current in "()":
                return Bracket(current)
            elif current in "[]":
                return SquareBracket(current)
            elif current in "{}":
                return CurlyBracket(current)
            elif current in "<>":
                return AngleBracket(current)

            elif current.isalpha():
                return Identifier(self.lex_identifier())
            elif current.isdigit():
                numeric_type, value = self.lex_numeric()
                return [Float, Integer][numeric_type == "int"](value)
            elif current in "\"'":
                return String(self.lex_string())


