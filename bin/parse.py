import sys

filename = sys.argv[1] if len(sys.argv) > 1 else ""

if not filename:
    print("Fatal: No FireScript file specified!")
    exit(-1)

from parser.lexer.readers import FileReader
from parser.lexer.lexer import Lexer
from parser.parser.parse import Parser

parser = Parser(Lexer(FileReader(filename)))
print(parser.parse_program().eval({}))
