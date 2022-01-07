from typing import Any, List, Tuple

from compiler.errors.errors import initialise_reader
from compiler.lexer.lexer import Lexer
from compiler.lexer.readers import StringReader


def test_lexer_string():
    code = '"Hello, \' World!"'
    
    tokens = [
        ("Hello, ' World!", "String"),
        ("", "EOF")
    ]

    compare_tokens(code, tokens)


def test_lexer_numeric():
    code = "123\n-123.45\n"
    
    tokens = [
        (123, "Integer"),
        (-123.45, "Float"),
        ("", "EOF")
    ]

    compare_tokens(code, tokens)


def test_lexer_arithmetic_expression():
    code = "54 - (8.88 / 5) * 56 + 'Hello'[1]"

    tokens = [
        (54, "Integer"),
        ("-", "Operator"),
        ("(", "Bracket"),
        (8.88, "Float"),
        ("/", "Operator"),
        (5, "Integer"),
        (")", "Bracket"),
        ("*", "Operator"),
        (56, "Integer"),
        ("+", "Operator"),
        ("Hello", "String"),
        ("[", "SquareBracket"),
        (1, "Integer"),
        ("]", "SquareBracket"),
        ("", "EOF")
    ]

    compare_tokens(code, tokens)


def test_lexer_program():
    code = """(begin
    ; Print a line
    (print "Hello, World!" '\\n')
    (put (< 8 5))
)"""

    tokens = [
        ("(", "Bracket"),
        ("begin", "Identifier"),
        ("(", "Bracket"),
        ("print", "Identifier"),
        ("Hello, World!", "String"),
        ("\\n", "String"),
        (")", "Bracket"),
        ("(", "Bracket"),
        ("put", "Identifier"),
        ("(", "Bracket"),
        ("<", "AngleBracket"),
        (8, "Integer"),
        (5, "Integer"),
        (")", "Bracket"),
        (")", "Bracket"),
        (")", "Bracket")
    ]

    compare_tokens(code, tokens)


def test_unterminated_string():
    code = "(print 'Hello!\n')"

    tokens = [
        ("(", "Bracket"),
        ("print", "Identifier"),
    ]

    check_error(code, tokens)


def test_unknown_character():
    code = "(begin &)"
    tokens = [
        ("(", "Bracket"),
        ("begin", "Identifier")
    ]

    check_error(code, tokens)


def check_error(code, tokens: List[Tuple[Any, str]]):
    _ex = exit
    globals()["exit"] = lambda _: None
    compare_tokens(code, tokens)
    globals()["exit"] = _ex

def compare_tokens(code: str, tokens: List[Tuple[Any, str]]):
    lexer = Lexer(StringReader(code))
    initialise_reader(lexer.reader)

    for tok in tokens:
        next_tok = lexer.next_token()

        assert next_tok.type == tok[1], f"Got unexpected token - {next_tok.type} (Expected {tok[1]})"
        assert next_tok.value == tok[0], f"Got unexpected {tok[1]} - {next_tok.value} (Expected {tok[0]})"
