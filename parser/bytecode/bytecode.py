from parser.bytecode.opcodes import OpCodes

from typing import List


def to_byte_code(codes: List[List[int]]) -> bytearray:

    bytecode = bytearray()

    for instruction in codes:
        for arg in instruction:
            bytecode.append(arg)
        bytecode.append(OpCodes.SEP)

    return bytecode
