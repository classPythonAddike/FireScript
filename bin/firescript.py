import click

from parser.bytecode.bytecode import to_byte_code
from parser.lexer.lexer import Lexer
from parser.parser.parse import Parser
from parser.lexer.readers import FileReader

@click.group()
def cli():
    pass

@cli.command(short_help="Compile a FireScript file")
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def build(file: str):
    """Parses a provided FireScript file, and outputs pseudo bytecode."""
    parser = Parser(Lexer(FileReader(file)))
    bytecode = to_byte_code(parser.parse_program())

    out_file = ".".join(file.split(".")[:-1]) + ".fsc"

    with open(out_file, "w") as f:
        f.write(bytecode)

if __name__ == "__main__":
    cli()
