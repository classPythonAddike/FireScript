import click

from compiler.lexer.lexer import Lexer
from compiler.parser.parse import Parser
from compiler.lexer.readers import FileReader
from compiler.bytecode.opcodes import operations
from compiler.bytecode.bytecode import to_byte_code

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
    click.echo("Format of ByteCode: INSTRUCTION [ARGS]+")
    click.echo()

    max_len = max([len(instruction) for instruction in operations])
    max_id_len = max([len(val[0]) for val in operations.values()])
    max_docs_len = max([len(val[1]) for val in operations.values()])

    click.echo("INSTRUCTION TYPE" + (max_len - 11) * " " + "ID" + " " * (max_id_len + 3) + "DESCRIPTION")
    click.echo((max_len + max_id_len + max_docs_len + 11) * "-")

    for num, instruction in enumerate(operations):
        sep = " -"[num % 2]
        click.echo(
            instruction \
            + " " \
            + sep * (max_len + 3 - len(instruction)) \
            + " " \
            + operations[instruction][0] \
            + " " \
            + sep * (max_id_len - len(operations[instruction][0]) + 3) \
            + " " \
            + operations[instruction][1]
        )

    click.echo()


@bytecode.command(short_help="Decompile bytecode into human readable format")
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def decompile(file: str):
    with open(file, "r") as f:
        bytecode = [line.split() for line in f.read().strip().split("\n")]

    code_instruction_map = {code[0]: inst for inst, code in operations.items()}

    for line in bytecode:
        inst = code_instruction_map[line[0]]
        click.echo(inst + " ", nl=False)

        if len(line) >= 2:
            if inst == "PUSH":
                _type = code_instruction_map[line[1]]
                args = line[1:]
                
                click.echo(_type + " ", nl=False)

                if _type == "BOOL":
                    click.echo(["FALSE", "TRUE"][int(args[0])] + " ", nl=False)
                if _type == "INT":
                    if args[0] == "0":
                        click.echo("-", nl=False)
                    click.echo(args[1], nl=False)
                if _type == "FLOAT":
                    if args[0] == "0":
                        click.echo("-", nl=False)
                    click.echo(args[1] + "." + args[2], nl=False)
                if _type == "STRING":
                    click.echo(" ".join(args), nl=False)
            elif inst == "COMPARE":
                _types = ["EQUAL_TO", "GREATER_THAN", "GREATER_THAN_OR_EQUAL"]
                click.echo(_types[int(line[1])], nl = False)
            else:
                click.echo(" ".join(line[1:]), nl=False)

        click.echo()


if __name__ == "__main__":
    cli()
