from typing import List, Union

from parser.lexer.lexer import Lexer
from parser.lexer.tokens import Token
from parser.lexer.readers import StringReader

from parser.parser.atoms import atom_types
from parser.parser.expressions import Expression, expression_types

from parser.errors.errors import FSyntaxError, initialise_reader

class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        initialise_reader(self.lexer.reader)

    def parse_program(self) -> Expression:
        tokens: List[Token] = []
       
        while True:
            next_token = self.lexer.next_token()
            
            if next_token.type == "EOF":
                break
            if next_token.type != 'NewLine':
                tokens.append(next_token)

        return self.parse(self.parse_raw(tokens))

    def parse_raw(self, tokens: List[Token]):
        if len(tokens) <= 1:
            FSyntaxError(len(self.lexer.reader.code.split("\n")), "Unexpected EOF!").raise_error()

        token = tokens.pop(0)

        if token.value == '(':
            L = []
            while tokens[0].value != ')':
                L.append(self.parse_raw(tokens))

            tokens.pop(0)
            return L
        else:
            return token

    def parse(self, tokens: Union[List, Token]) -> Expression:
        if isinstance(tokens, list):
            if tokens[0].value in expression_types:
                return expression_types[tokens[0].value](
                    tokens[0].line,
                    *[self.parse(tok) for tok in tokens[1:]]
                )
            else:
                # Undefined keyword
                # TODO: Proper error
                exit(-1)
        elif tokens.type in atom_types:
            return atom_types[tokens.type](tokens)
        else:
            FSyntaxError(
                tokens.line,
                f"Unexpected '{tokens.value}' on line {tokens.line}!",
            ).raise_error()


# Testing purposes

code = """
(begin
    (put 'Program to find volume of a sphere:')
    (define r (float 100) )
    (define pi 3.14 500)
    (put
        (+
            "Area is"
            (string (* (/ 4 3) pi r r r))
        )
    )
)
"""

p = Parser(Lexer(StringReader(code)))
print("Code:\n", p.lexer.reader.code, sep="", end="\n")
print("Compiled Output:\n\n", p.parse_program().eval({}), sep="")
