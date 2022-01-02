from parser.lexer.lexer import Lexer
from parser.parser.expressions import Expression, Program
from parser.parser.parse import Parser
from parser.lexer.readers import StringReader


def test_arithmetic():
    code = "(begin (+ 5 6 7))"
    program = new_program(code)

    check_expression_type(program.values[0], "AddExp")

    for i in [5, 6, 7]:
        assert program.values[0].values[i - 5].value == i, f"Didn't get integer {i} from AddExp!"


def test_program_1():
    code = "(begin (print (- 8 3)))"
    program = new_program(code)

    check_expression_type(program.values[0], "PrintExp")
    check_expression_type(program.values[0].values[0], "SubExp")

    assert program.values[0].values[0].lval.value == 8, "Didn't get integer 8 from SubExp!"
    assert program.values[0].values[0].rval.value == 3, "Didn't get integer 3 from SubExp!"


def test_typecast():
    code = "(begin (define r 100.0) (assign r (+ r (float 200))))"
    program = new_program(code)

    check_expression_type(program.values[0], "DefExp")
    check_expression_type(program.values[1], "AssignExp")
    check_expression_type(program.values[1].value, "AddExp")
    check_expression_type(program.values[1].value.values[1], "FloatTypeCast")


def test_assignment():
    code = "(begin (define r 'Hello, World!') (get r) (define y 54.5) (assign y (/ y 2.0)))"
    program = new_program(code)

    check_expression_type(program.values[0], "DefExp")
    check_expression_type(program.values[1], "GetExp")
    check_expression_type(program.values[2], "DefExp")
    check_expression_type(program.values[3], "AssignExp")
    check_expression_type(program.values[3].value, "DivExp")


def test_boolean():
    code = "(begin (put true false))"
    program = new_program(code)

    check_expression_type(program.values[0], "PutExp")
    check_expression_type(program.values[0].values[0], "BoolExp")
    check_expression_type(program.values[0].values[1], "BoolExp")


def new_program(code: str) -> Program:
    program = Parser(Lexer(StringReader(code))).parse_program()
    check_expression_type(program, "Program")
    return program

def check_expression_type(exp: Expression, exp_type: str):
    assert exp.type == exp_type, f"Got expression of type {exp.type} instead of {exp_type}!"
