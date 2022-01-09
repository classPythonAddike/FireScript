import click

from compiler.lexer.lexer import Lexer
from compiler.parser.parse import Parser
from compiler.lexer.readers import FileReader
from compiler.bytecode.bytecode import to_byte_code
from compiler.bytecode.opcodes import ls_operations

VERSION = "0.0.1-alpha"

@click.group()
def cli():
    pass

@cli.command(short_help="Compile a FireScript file")
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def build(file: str):
    """Parses a provided FireScript file, and outputs pseudo bytecode."""
    parser = Parser(Lexer(FileReader(file)))
    bytecode = to_byte_code(parser.parse_program().eval({}))

    out_file = ".".join(file.split(".")[:-1]) + ".fsc"

    with open(out_file, "w") as f:
        f.write(bytecode)


@cli.command(short_help="Display version info")
def version():
    """Display version information"""
    click.echo(f"Firescript v{VERSION}")


@cli.group()
def bytecode():
    pass


@bytecode.command(short_help="List valid bytecode instructions (for developers)")
def lsop():
    """List all valid bytecode instructions, along with their code (meant for developers)"""
    click.echo("Format of ByteCode: NUM_CODES INSTRUCTION [ARGS]+")

    for instruction, id in ls_operations().items():
        click.echo(f"{instruction}  {id}")


if __name__ == "__main__":
    cli()
