from compiler.lexer.lexer import Lexer
from compiler.parser.expressions import Expression, Program
from compiler.parser.parse import Parser
from compiler.lexer.readers import StringReader


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


def test_comparison():
    code = "(begin (< 5 0) (> 6 9) (<-9 0))"
    program = new_program(code)

    check_expression_type(program.values[0], "LessThanExp")
    check_expression_type(program.values[1], "GreaterThanExp")
    check_expression_type(program.values[2], "LessThanExp")


def test_if_statements():
    code = "(begin (if (< 5 6) (print '5 is less than 6!') (print '5 is not less than 6!')))"
    program = new_program(code)

    check_expression_type(program.values[0], "IfExp")
    check_expression_type(program.values[0].condition, "LessThanExp")
    check_expression_type(program.values[0].body, "PrintExp")
    check_expression_type(program.values[0].alternate, "PrintExp")


def new_program(code: str) -> Program:
    program = Parser(Lexer(StringReader(code))).parse_program()
    check_expression_type(program, "Program")
    return program

def check_expression_type(exp: Expression, exp_type: str):
    assert exp.type == exp_type, f"Got expression of type {exp.type} instead of {exp_type}!"
