from parser.lexer.lexer import Lexer
from parser.lexer.tokens import Token

from parser.parser.expressions import Expression, Program
from parser.parser.expression_models import atom_types, expression_types

from parser.errors.errors import FArgsError, FProgramError, FSyntaxError, FKeywordError, initialise_reader

from typing import List, Union

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        initialise_reader(self.lexer.reader)

    def parse_program(self) -> List:
        tokens: List[Token] = []

        while True:
            next_token = self.lexer.next_token()

            if next_token.type == "EOF":
                break
            if next_token.type != "NewLine":
                tokens.append(next_token)

        program = self.parse(self.parse_raw(tokens))

        if not isinstance(program, Program):
            FProgramError(
                1,
                "All FireScript programs must be of the form `(begin ...)`!"
            ).raise_error()

        self.check_typing(program)

        return program.eval({})

    def parse_raw(self, tokens: List[Token]):
        if len(tokens) <= 1:
            FSyntaxError(
                len(self.lexer.reader.code.split("\n")), "Unexpected EOF!"
            ).raise_error()

        token = tokens.pop(0)

        if token.value == "(":
            L = []
            while tokens[0].value != ")":
                L.append(self.parse_raw(tokens))

            tokens.pop(0)
            return L
        else:
            return token

    def parse(self, tokens: Union[List, Token]) -> Union[Program, Expression]:
        if isinstance(tokens, list):
            if tokens[0].value in expression_types:

                exp_type = expression_types[tokens[0].value]

                if exp_type.num_args() != 0 and len(tokens) - 1 != exp_type.num_args():
                    FArgsError(
                        tokens[0].line,
                        f"Incorrect number of arguments provided to `{exp_type.keyword()}` "
                        f"- expected {exp_type.num_args()}"
                        f" but got {len(tokens) - 1}!",
                    ).raise_error()

                return exp_type(
                    tokens[0].line, *[self.parse(tok) for tok in tokens[1:]]
                )
            else:
                FKeywordError(
                    tokens[0].line, 
                    f"`{tokens[0].value}` is neither a valid keyword nor a variable!"
                ).raise_error()

        elif tokens.type in atom_types:
            return atom_types[tokens.type](tokens)
        else:
            FSyntaxError(
                tokens.line,
                f"Unexpected `{tokens.value}` on line {tokens.line}!",
            ).raise_error()

    def check_typing(self, program: Program):
        program.load_type({})
