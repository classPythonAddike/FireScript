from typing import List

from compiler.bytecode.opcodes import OpCodes


def to_byte_code(codes: List[List[str]]) -> str:
    """
    Takes a list of instruction codes, and converts them into a pseudo bytecode string
    Format of bytecode:
    INSTRUCTION ([ARGUMENT] | [TYPE, *ARGUMENTS])
    """

    bytecode = ""

    for instruction in codes:

        for arg in instruction:
            bytecode += arg + " "

        bytecode = bytecode.strip() + OpCodes.SEP

    return bytecode
