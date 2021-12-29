from typing import List
from parser.lexer.lexer import Lexer
from parser.lexer.readers import FileReader
from parser.lexer.tokens import Token
from parser.parser.expressions import AddExp, Expression, IntExp


class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer


    def check_program_structure(self, tokens: List[Token]):
        for tok_num, req in enumerate([("Bracket", "("), ("Identifier", "begin")]):
            assert len(tokens) > tok_num, "Unexpected EOF!"
            assert tokens[tok_num].type == req[0] and tokens[tok_num].value == req[1], \
                f"Unexpected {tokens[tok_num].type}"

        assert len(tokens) > 4
        assert tokens[-1].type == "EOF", "No EOF found!"

        assert len(tokens) > 3
        assert tokens[-2].type == "Bracket" and tokens[-2].value == ")", \
        f"Program's beggining bracket was not closed!"


    def parse_program(self) -> List[Expression]:
        tokens: List[Token] = []
       
        while True:
            next_token = self.lexer.next_token()
            tokens.append(next_token)
            if next_token.type == "EOF":
                break

        self.check_program_structure(tokens)

        return self.parse(tokens[2:-2]) # We don't want the (begin and ) EOF

    def next_expression(self, tokens: List[Token]) -> List[Token]:
        current_position = 0
        if tokens[current_position].type == "Bracket":
            return [tokens[1]]
        else:
            return [tokens[current_position]]

    
    def parse(self, tokens: List[Token]) -> List:
        expressions: List = []
        current_position = 0

        while True:
            next_token = tokens[current_position]

            if next_token.type == "Bracket" and next_token.value == "(":
                open_brack_count = 1
                close_brack_count = 0
                open_brack_pos = current_position * 1

                while open_brack_count != close_brack_count:
                    current_position += 1
                    peek_token = tokens[current_position]

                    if peek_token.type == "Bracket":
                        if peek_token.value == "(":
                            open_brack_count += 1
                        else:
                            close_brack_count += 1

                expressions.extend(self.parse(tokens[open_brack_pos + 1: current_position]))
            
            elif next_token.type == "NewLine":
                current_position += 1

            elif next_token.type == "Operator":
                current_position += 1
                lval = self.parse(self.next_expression(tokens[current_position:]))[0]
                
                current_position += 1
                rval = self.parse(self.next_expression(tokens[current_position:]))[0]

                if next_token.value == "+":
                    expressions.append(AddExp(lval, rval))
                
                current_position += 1

            elif next_token.type == "Integer":
                expressions.append(IntExp(next_token.value))
                current_position += 1

            else:
                current_position += 1


            if current_position >= len(tokens) - 1:
                break

            

        return expressions



with open("code.txt", "w") as f:
    f.write("(begin\n   (+ 8 16)\n)")

p = Parser(Lexer(FileReader("code.txt")))
print("Code:\n\n", p.lexer.reader.code, sep="", end="\n\n")
print("Compiled Output:\n\n", p.parse_program()[0].eval(), sep="")
