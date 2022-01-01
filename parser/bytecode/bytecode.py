from typing import List

from parser.bytecode.opcodes import OpCodes


def to_byte_code(codes: List[List[str]]) -> str:

    bytecode = ""

    for instruction in codes:
        for arg in instruction:
            bytecode += arg + " "
        bytecode += OpCodes.SEP + " "

    return bytecode.strip() + "\n"
