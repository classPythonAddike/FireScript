import os

from parser.lexer.tokens import *
from parser.lexer.lexer import Lexer
from parser.lexer.readers import FileReader

dummy_file = "code.txt"


def delete_file(file):
    os.remove(file)


def test_lexer_string():
    with open(dummy_file, "w") as f:
        f.write('"Hello, \' World!"')

    lexer = Lexer(FileReader(dummy_file))

    str_token = lexer.next_token()
    assert str_token.type == "String", f"Got unexpected token - {str_token.type}!"
    assert (
        str_token.value == "Hello, ' World!"
    ), f"Got unexpected string - {str_token.value}"

    assert lexer.next_token().type == "EOF", f"Got unexpected token instead of EOF!"


def test_lexer_numeric():
    with open(dummy_file, "w") as f:
        f.write("123\n123.45\n")

    lexer = Lexer(FileReader(dummy_file))

    int_token = lexer.next_token()
    assert int_token.type == "Integer", f"Got unexpected token - {int_token.type}!"
    assert int_token.value == 123, f"Got unexpected integer - {int_token.value}"

    float_token = lexer.next_token()
    assert float_token.type == "Float", f"Got unexpected token - {float_token.type}!"
    assert float_token.value == 123.45, f"Got unexpected float - {float_token.value}"

    assert lexer.next_token().type == "EOF", f"Got unexpected token instead of EOF!"
