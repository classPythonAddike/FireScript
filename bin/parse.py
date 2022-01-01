import os
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else ""

if not filename:
    print("Fatal: No FireScript file specified!")
    exit(-1)

if not os.path.exists(filename):
    print("Fatal: Could not open file", filename)
    exit(-1)

from parser.bytecode.bytecode import to_byte_code
from parser.lexer.lexer import Lexer
from parser.parser.parse import Parser
from parser.lexer.readers import FileReader

parser = Parser(Lexer(FileReader(filename)))
bytecode = to_byte_code(parser.parse_program())

out_file = ".".join(filename.split(".")[:-1]) + ".fsc"

with open(out_file, "w") as f:
    f.write(bytecode)
