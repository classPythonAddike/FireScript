from compiler.lexer.lexer import Lexer
from compiler.lexer.tokens import Token
from compiler.parser.expression_models.comparison import GreaterThanOrEqualExp, LessThanOrEqualExp

from compiler.parser.expressions import Expression, Program
from compiler.parser.expression_models import atom_types, expression_types

from compiler.errors.errors import (
    FArgsError,
    FEOFError,
    FProgramError,
    FSyntaxError,
    FKeywordError,
    initialise_reader,
)

from typing import List, Union


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        initialise_reader(self.lexer.reader)

    def parse_program(self) -> Program:
        """Reads all tokens from the lexer, and parses them into a Program"""
        tokens: List[Token] = []

        while True:
            next_token = self.lexer.next_token()
            if next_token.type == "EOF":
                break
            
            tokens.append(next_token)

        program = self.parse(self.parse_raw(tokens))

        if not isinstance(program, Program):
            FProgramError(
                1, "All FireScript programs must be of the form `(begin ...)`!"
            ).raise_error()

        self.check_typing(program)

        return program

    def parse_raw(self, tokens: List[Token]):
        """
        Converts a list of tokens into a nested list of tokens
        Eg: (begin (+ 1 2)) would become [begin, [+, 1, 2]]
        """

        if len(tokens) <= 1:
            FEOFError(
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
        """Parses a nested list of tokens into an AST"""
        if isinstance(tokens, list):
            if tokens[0].value in expression_types:

                exp_type = expression_types[tokens[0].value]

                if exp_type.num_args() != 0 and len(tokens) - 1 != exp_type.num_args():
                    # Greater than / less than or equal to -
                    if tokens[0].value in [">", "<"] and len(tokens) - 1 == 3:
                        if tokens[1].type == "EqualTo":
                            return {
                                ">": GreaterThanOrEqualExp,
                                "<": LessThanOrEqualExp
                            }[tokens[0].value](
                                tokens[0].line,
                                *[self.parse(tok) for tok in tokens[2:]]
                            )
                    elif tokens[0].value in [">", "<"]:
                        FArgsError(
                            tokens[0].line,
                            f"Incorrect number of arguments provided to `<=` "
                            f"- expected 2 but got {len(tokens) - 2}!"
                        ).raise_error()

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
                    f"`{tokens[0].value}` is not a valid keyword!",
                ).raise_error()

        elif tokens.type in atom_types:
            return atom_types[tokens.type](tokens)
        else:
            FSyntaxError(
                tokens.line,
                f"Unexpected `{tokens.value}` on line {tokens.line}!",
            ).raise_error()

    def check_typing(self, program: Program):
        """
        Assert that static typing is followed.
        The method `load_type()` is called on every node of the AST
        """
        program.load_type({})
